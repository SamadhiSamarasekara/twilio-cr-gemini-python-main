from __future__ import annotations

from dataclasses import dataclass
from typing import Any


FREE_SHIPPING_THRESHOLD = 30000

DISTRICT_SHIPPING: dict[str, dict[str, Any]] = {
    "Colombo": {"fee": 0, "eta": "Same day via concierge dispatch"},
    "Gampaha": {"fee": 900, "eta": "1-2 working days"},
    "Kalutara": {"fee": 950, "eta": "1-2 working days"},
    "Kandy": {"fee": 1100, "eta": "2 working days"},
    "Galle": {"fee": 1200, "eta": "2-3 working days"},
    "Matara": {"fee": 1250, "eta": "2-3 working days"},
    "Hambantota": {"fee": 1350, "eta": "3 working days"},
    "Jaffna": {"fee": 1600, "eta": "3-4 working days"},
    "Kurunegala": {"fee": 1100, "eta": "2 working days"},
    "Anuradhapura": {"fee": 1350, "eta": "3 working days"},
    "Polonnaruwa": {"fee": 1350, "eta": "3 working days"},
    "Badulla": {"fee": 1450, "eta": "3 working days"},
    "Monaragala": {"fee": 1500, "eta": "3-4 working days"},
    "Ratnapura": {"fee": 1200, "eta": "2-3 working days"},
    "Kegalle": {"fee": 1150, "eta": "2 working days"},
    "Puttalam": {"fee": 1300, "eta": "2-3 working days"},
    "Nuwara Eliya": {"fee": 1400, "eta": "3 working days"},
    "Trincomalee": {"fee": 1450, "eta": "3 working days"},
    "Batticaloa": {"fee": 1500, "eta": "3-4 working days"},
    "Ampara": {"fee": 1500, "eta": "3-4 working days"},
    "Mullaitivu": {"fee": 1600, "eta": "4 working days"},
    "Vavuniya": {"fee": 1500, "eta": "3-4 working days"},
    "Mannar": {"fee": 1550, "eta": "3-4 working days"},
    "Kilinochchi": {"fee": 1550, "eta": "3-4 working days"},
}


def lkr(value: int) -> str:
    return f"Rs. {value:,.0f}"


@dataclass(frozen=True)
class Category:
    slug: str
    name: str
    aura: str
    eyebrow: str
    hero_title: str
    hero_copy: str
    highlight: str
    video_url: str


CATEGORIES: dict[str, Category] = {
    "men": Category(
        slug="men",
        name="Men",
        aura="Noir Motion",
        eyebrow="Tailored presence",
        hero_title="Sharp silhouettes cut through the city after dark.",
        hero_copy="Modern tailoring, quiet confidence, and precise layering built for Sri Lanka's premium menswear customer.",
        highlight="Clean structure, tonal depth, and understated gold accents.",
        video_url="https://assets.mixkit.co/videos/preview/mixkit-young-man-walking-in-the-city-4077-large.mp4",
    ),
    "women": Category(
        slug="women",
        name="Women",
        aura="Halo Drift",
        eyebrow="Fluid elegance",
        hero_title="Light catches every fold, every turn, every refined detail.",
        hero_copy="Elevated dresses, sculpted separates, and luminous textures for statement moments without excess.",
        highlight="Airy drape, cinematic movement, and polished minimal glamour.",
        video_url="https://assets.mixkit.co/videos/preview/mixkit-woman-model-walking-in-an-urban-setting-34451-large.mp4",
    ),
    "accessories": Category(
        slug="accessories",
        name="Accessories",
        aura="Golden Echo",
        eyebrow="Finishing language",
        hero_title="The smallest details carry the longest impression.",
        hero_copy="Curated accessories designed to complete the look with luxury restraint, tactile finishes, and gift-ready polish.",
        highlight="Leather, metal, and fine textures in a restrained gold-black palette.",
        video_url="https://assets.mixkit.co/videos/preview/mixkit-close-up-shot-of-a-person-adjusting-a-watch-32808-large.mp4",
    ),
}


PRODUCTS: list[dict[str, Any]] = [
    {
        "slug": "obsidian-drape-blazer",
        "category": "men",
        "name": "Obsidian Drape Blazer",
        "price": 18500,
        "eyebrow": "Men / Signature Tailoring",
        "subtitle": "A softly structured blazer with satin-finished lapels and a feather-light hand feel.",
        "description": "Cut for evening definition with breathable lining and a crisp shoulder line that stays elegant in tropical weather.",
        "materials": ["Italian suiting blend", "Breathable cupro lining", "Gold-pin collar tab"],
        "sizes": ["S", "M", "L", "XL"],
        "fit_profile": "tailored",
        "fit_tip": "Runs true with a neat shoulder. Size up for relaxed layering.",
        "colors": {
            "Obsidian": "https://images.unsplash.com/photo-1592878904946-b3cd5f0e7c4c?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Stone": "https://images.unsplash.com/photo-1593032465171-8bd75b5d1c2d?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Quiet Luxury", "Breathable"],
        "complete_the_look": ["lumina-signature-watch", "atelier-leather-loafer"],
    },
    {
        "slug": "prism-resort-shirt",
        "category": "men",
        "name": "Prism Resort Shirt",
        "price": 9200,
        "eyebrow": "Men / Relaxed Edit",
        "subtitle": "Open-collar polish in a fluid cotton-silk blend for day-to-night dressing.",
        "description": "A refined resort shirt with a soft sheen and elevated drape, designed for heat and ease.",
        "materials": ["Cotton silk blend", "Mother-of-pearl buttons", "French seams"],
        "sizes": ["S", "M", "L", "XL"],
        "fit_profile": "relaxed",
        "fit_tip": "Relaxed through the chest. Stay true to size for fluid fit.",
        "colors": {
            "Prism White": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Midnight": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Smart Casual", "Limited Run"],
        "complete_the_look": ["obsidian-weekender", "auric-frame-sunglasses"],
    },
    {
        "slug": "atelier-leather-loafer",
        "category": "men",
        "name": "Atelier Leather Loafer",
        "price": 14500,
        "eyebrow": "Men / Footwear",
        "subtitle": "Hand-finished loafers with cushioned insoles and a refined pointed silhouette.",
        "description": "A polished leather loafer built for sharp movement between office, dinner, and occasion wear.",
        "materials": ["Full-grain leather", "Cushioned footbed", "Rubberized leather sole"],
        "sizes": ["40", "41", "42", "43", "44"],
        "fit_profile": "structured",
        "fit_tip": "Narrow through the toe. Choose one size up if between sizes.",
        "colors": {
            "Noir": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Espresso": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Hand Finished", "Cushioned"],
        "complete_the_look": ["obsidian-drape-blazer", "lumina-signature-watch"],
    },
    {
        "slug": "halo-satin-slip",
        "category": "women",
        "name": "Halo Satin Slip Dress",
        "price": 16800,
        "eyebrow": "Women / Occasion",
        "subtitle": "Bias-cut satin with a light-catching finish and elegant floor-skimming movement.",
        "description": "An evening dress engineered for quiet drama, with adjustable straps and a sculpted back line.",
        "materials": ["Liquid satin", "Silk touch lining", "Invisible side zip"],
        "sizes": ["XS", "S", "M", "L"],
        "fit_profile": "slim",
        "fit_tip": "Bias cut skims the body. Size up for extra ease at the hip.",
        "colors": {
            "Champagne": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Black Pearl": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Event Ready", "Best Seller"],
        "complete_the_look": ["lumina-clutch", "auric-drop-earrings"],
    },
    {
        "slug": "lumina-tailored-set",
        "category": "women",
        "name": "Lumina Tailored Set",
        "price": 21200,
        "eyebrow": "Women / Modern Suiting",
        "subtitle": "Wide-leg tailoring and a softly sculpted vest for confident day-to-night dressing.",
        "description": "A coordinated set that balances architectural lines with breathable fabric and fluid motion.",
        "materials": ["Premium suiting twill", "Soft matte lining", "Hidden waist adjusters"],
        "sizes": ["XS", "S", "M", "L"],
        "fit_profile": "tailored",
        "fit_tip": "Tailored at the waist with fluid trousers. Stay true to size.",
        "colors": {
            "Ivory": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Obsidian": "https://images.unsplash.com/photo-1495385794356-15371f348c31?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Power Edit", "Office to Evening"],
        "complete_the_look": ["lumina-signature-watch", "auric-frame-sunglasses"],
    },
    {
        "slug": "quiet-luxe-knit",
        "category": "women",
        "name": "Quiet Luxe Knit Top",
        "price": 8500,
        "eyebrow": "Women / Essentials",
        "subtitle": "A second-skin rib knit with refined stretch and subtle gold hardware.",
        "description": "Designed as an elevated essential with polished proportions for layering and stand-alone wear.",
        "materials": ["Viscose rib knit", "Soft stretch blend", "Gold logo tab"],
        "sizes": ["XS", "S", "M", "L"],
        "fit_profile": "slim",
        "fit_tip": "Close fit. Choose your usual size or size up for a softer silhouette.",
        "colors": {
            "Cream": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Mink": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Wardrobe Staple", "Soft Touch"],
        "complete_the_look": ["lumina-clutch", "auric-drop-earrings"],
    },
    {
        "slug": "lumina-signature-watch",
        "category": "accessories",
        "name": "Lumina Signature Watch",
        "price": 15800,
        "eyebrow": "Accessories / Timepieces",
        "subtitle": "A slim profile timepiece with brushed gold casing and a black leather strap.",
        "description": "Designed to pair with tailoring or occasion wear, balancing modern restraint with jewelry-like polish.",
        "materials": ["Mineral glass", "Gold-plated bezel", "Italian leather strap"],
        "sizes": ["One Size"],
        "fit_profile": "universal",
        "fit_tip": "Universal fit with adjustable strap.",
        "colors": {
            "Gold Noir": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Silver White": "https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Gift Ready", "Signature Piece"],
        "complete_the_look": ["obsidian-drape-blazer", "lumina-tailored-set"],
    },
    {
        "slug": "lumina-clutch",
        "category": "accessories",
        "name": "Lumina Clutch",
        "price": 11200,
        "eyebrow": "Accessories / Evening",
        "subtitle": "Structured mini clutch with mirror-finish hardware and soft suede lining.",
        "description": "An occasion-ready accessory sized for essentials, with a detachable chain for versatility.",
        "materials": ["Structured vegan leather", "Suede lining", "Detachable chain strap"],
        "sizes": ["One Size"],
        "fit_profile": "universal",
        "fit_tip": "Compact event silhouette that fits phone, cards, and lipstick.",
        "colors": {
            "Gold Sand": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Black Onyx": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Evening Edit", "Occasion Essential"],
        "complete_the_look": ["halo-satin-slip", "quiet-luxe-knit"],
    },
    {
        "slug": "auric-drop-earrings",
        "category": "accessories",
        "name": "Auric Drop Earrings",
        "price": 6800,
        "eyebrow": "Accessories / Jewelry",
        "subtitle": "Minimal sculptural drops in a soft brushed gold finish.",
        "description": "The finishing accent for occasionwear and modern evening styling.",
        "materials": ["Brushed alloy", "Hypoallergenic post", "Soft matte finish"],
        "sizes": ["One Size"],
        "fit_profile": "universal",
        "fit_tip": "Lightweight enough for all-evening wear.",
        "colors": {
            "Lumina Gold": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Pearl Glow": "https://images.unsplash.com/photo-1635767798638-3e25273a8236?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Lightweight", "Giftable"],
        "complete_the_look": ["halo-satin-slip", "quiet-luxe-knit"],
    },
    {
        "slug": "obsidian-weekender",
        "category": "accessories",
        "name": "Obsidian Weekender",
        "price": 19800,
        "eyebrow": "Accessories / Travel",
        "subtitle": "A structured travel bag with smart compartments and gold-finish hardware.",
        "description": "A premium weekender sized for quick escapes, overnight business trips, and elevated carry-on style.",
        "materials": ["Pebbled vegan leather", "Twill interior", "Laptop sleeve"],
        "sizes": ["One Size"],
        "fit_profile": "universal",
        "fit_tip": "Fits 48-hour travel essentials with dedicated accessory pockets.",
        "colors": {
            "Black": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Cocoa": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["Travel Edit", "New Arrival"],
        "complete_the_look": ["prism-resort-shirt", "atelier-leather-loafer"],
    },
    {
        "slug": "auric-frame-sunglasses",
        "category": "accessories",
        "name": "Auric Frame Sunglasses",
        "price": 7800,
        "eyebrow": "Accessories / Eyewear",
        "subtitle": "Slim metal frames with gradient lenses and a lightweight premium feel.",
        "description": "A clean, modern frame designed to add polish without visual noise.",
        "materials": ["UV400 lenses", "Lightweight alloy frame", "Microfiber case"],
        "sizes": ["One Size"],
        "fit_profile": "universal",
        "fit_tip": "Comfort-fit nose bridge with universal frame width.",
        "colors": {
            "Gold Smoke": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=1200&q=80&fm=webp",
            "Silver Ice": "https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=1200&q=80&fm=webp",
        },
        "badges": ["UV Protected", "Best Seller"],
        "complete_the_look": ["lumina-tailored-set", "prism-resort-shirt"],
    },
]


PRODUCT_INDEX = {product["slug"]: product for product in PRODUCTS}


def build_product(product: dict[str, Any]) -> dict[str, Any]:
    primary_image = next(iter(product["colors"].values()))
    category = CATEGORIES[product["category"]]
    return {
        **product,
        "price_display": lkr(product["price"]),
        "primary_image": primary_image,
        "category_name": category.name,
        "aura": category.aura,
    }


def all_products() -> list[dict[str, Any]]:
    return [build_product(product) for product in PRODUCTS]


def products_for_category(slug: str) -> list[dict[str, Any]]:
    return [build_product(product) for product in PRODUCTS if product["category"] == slug]


def get_product(slug: str) -> dict[str, Any] | None:
    product = PRODUCT_INDEX.get(slug)
    if product is None:
        return None
    built = build_product(product)
    built["complete_the_look_items"] = [
        build_product(PRODUCT_INDEX[related_slug])
        for related_slug in product["complete_the_look"]
        if related_slug in PRODUCT_INDEX
    ]
    return built


def featured_products() -> list[dict[str, Any]]:
    featured_slugs = [
        "obsidian-drape-blazer",
        "halo-satin-slip",
        "lumina-signature-watch",
        "obsidian-weekender",
    ]
    return [build_product(PRODUCT_INDEX[slug]) for slug in featured_slugs]

