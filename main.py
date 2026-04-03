import os
import json
import uvicorn
from google import genai
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.catalog import (
    CATEGORIES,
    DISTRICT_SHIPPING,
    FREE_SHIPPING_THRESHOLD,
    all_products,
    featured_products,
    get_product,
    products_for_category,
)

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
PORT = int(os.getenv("PORT", "8080"))
DOMAIN = os.getenv("NGROK_URL") 
WS_URL = f"wss://{DOMAIN}/ws" if DOMAIN else None

# Updated greeting to reflect the new model
WELCOME_GREETING = "Hi! I am a voice assistant powered by Twilio and Google Gemini. Ask me anything!"

# System prompt for Gemini
# Gemini works well with a direct instruction like this.
SYSTEM_PROMPT = """You are a helpful and friendly voice assistant. This conversation is happening over a phone call, so your responses will be spoken aloud. 
Please adhere to the following rules:
1. Provide clear, concise, and direct answers.
2. Spell out all numbers (e.g., say 'one thousand two hundred' instead of 1200).
3. Do not use any special characters like asterisks, bullet points, or emojis.
4. Keep the conversation natural and engaging."""

# --- Gemini API Initialization ---
# Get your Google API key from https://aistudio.google.com/app/apikey
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None

# Store active chat sessions
# We will now store Gemini's chat session objects
sessions = {}

# Create FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def storefront_home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "categories": list(CATEGORIES.values()),
            "featured_products": featured_products(),
            "all_products": all_products(),
            "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        },
    )


@app.get("/category/{slug}", response_class=HTMLResponse)
async def category_page(request: Request, slug: str):
    category = CATEGORIES.get(slug)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return templates.TemplateResponse(
        request,
        "category.html",
        {
            "category": category,
            "categories": list(CATEGORIES.values()),
            "products": products_for_category(slug),
            "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        },
    )


@app.get("/product/{slug}", response_class=HTMLResponse)
async def product_page(request: Request, slug: str):
    product = get_product(slug)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        request,
        "product.html",
        {
            "product": product,
            "categories": list(CATEGORIES.values()),
            "shipping_options": DISTRICT_SHIPPING,
            "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        },
    )


@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    return templates.TemplateResponse(
        request,
        "cart.html",
        {
            "categories": list(CATEGORIES.values()),
            "shipping_options": DISTRICT_SHIPPING,
            "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        },
    )


@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse(
        request,
        "checkout.html",
        {
            "categories": list(CATEGORIES.values()),
            "shipping_options": DISTRICT_SHIPPING,
            "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        },
    )


@app.get("/api/shipping/{district}", response_class=JSONResponse)
async def shipping_quote(district: str):
    shipping = DISTRICT_SHIPPING.get(district)
    if shipping is None:
        raise HTTPException(status_code=404, detail="District not found")
    return JSONResponse({"district": district, **shipping})


@app.get("/api/fit/{slug}", response_class=JSONResponse)
async def fit_recommendation(slug: str, height_cm: int, weight_kg: int, preference: str = "regular"):
    product = get_product(slug)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    sizes = product["sizes"]
    if len(sizes) == 1:
        size = sizes[0]
    else:
        score = 0
        if height_cm >= 175:
            score += 1
        if height_cm >= 185:
            score += 1
        if weight_kg >= 72:
            score += 1
        if weight_kg >= 84:
            score += 1
        if preference == "relaxed":
            score += 1
        if preference == "slim":
            score -= 1
        score = max(0, min(score, len(sizes) - 1))
        size = sizes[score]

    return JSONResponse(
        {
            "size": size,
            "message": f"We recommend {size} for a {preference} {product['fit_profile']} fit.",
            "fit_tip": product["fit_tip"],
        }
    )

def gemini_response(chat_session, user_prompt):
    """Get a response from the Gemini API."""
    response = chat_session.send_message(user_prompt)
    return response.text

@app.post("/twiml")
@app.get("/twiml")
async def twiml_endpoint():
    """Endpoint that returns TwiML for Twilio to connect to the WebSocket"""
    if not WS_URL:
        return Response(
            content="Twilio voice mode is unavailable until NGROK_URL is configured.",
            media_type="text/plain",
            status_code=503,
        )
    # Note: Twilio ConversationRelay has built-in TTS. We specify a provider and voice.
    # You can change 'ElevenLabs' to 'Amazon' or 'Google' if you prefer their TTS.
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
    <Connect>
    <ConversationRelay url="{WS_URL}" welcomeGreeting="{WELCOME_GREETING}" ttsProvider="ElevenLabs" voice="FGY2WhTYpPnrIDTdsKH5" />
    </Connect>
    </Response>"""
    
    return Response(content=xml_response, media_type="text/xml")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    if client is None:
        await websocket.close(code=1011)
        return
    await websocket.accept()
    call_sid = None
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "setup":
                call_sid = message["callSid"]
                print(f"Setup for call: {call_sid}")
                # Start a new chat session for this call using the new SDK
                sessions[call_sid] = client.chats.create(
                    model="gemini-2.5-flash",
                    config={"system_instruction": SYSTEM_PROMPT}
                )
                
            elif message["type"] == "prompt":
                if not call_sid or call_sid not in sessions:
                    print(f"Error: Received prompt for unknown call_sid {call_sid}")
                    continue

                user_prompt = message["voicePrompt"]
                print(f"Processing prompt: {user_prompt}")
                
                chat_session = sessions[call_sid]
                response_text = gemini_response(chat_session, user_prompt)
                
                # The chat_session object automatically maintains history.
                
                # Send the complete response back to Twilio.
                # Twilio's ConversationRelay will handle the text-to-speech conversion.
                await websocket.send_text(
                    json.dumps({
                        "type": "text",
                        "token": response_text,
                        "last": True  # Indicate this is the full and final message
                    })
                )
                print(f"Sent response: {response_text}")
                
            elif message["type"] == "interrupt":
                print(f"Handling interruption for call {call_sid}.")
                
            else:
                print(f"Unknown message type received: {message['type']}")
                
    except WebSocketDisconnect:
        print(f"WebSocket connection closed for call {call_sid}")
        if call_sid in sessions:
            sessions.pop(call_sid)
            print(f"Cleared session for call {call_sid}")

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    print(f"WebSocket URL for Twilio: {WS_URL}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
