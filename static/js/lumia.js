const CART_KEY = "lumia-cart";

const formatLkr = (value) =>
  `Rs. ${Number(value || 0).toLocaleString("en-LK", { maximumFractionDigits: 0 })}`;

const readCart = () => {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY) || "[]");
  } catch {
    return [];
  }
};

const writeCart = (cart) => {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
};

const cartSubtotal = (cart) =>
  cart.reduce((sum, item) => sum + Number(item.price) * Number(item.quantity), 0);

const triggerHaptic = () => {
  if ("vibrate" in navigator) {
    navigator.vibrate(16);
  }
};

const renderCartItem = (item) => `
  <article class="cart-item">
    <img src="${item.image}" alt="${item.name}">
    <div>
      <h4>${item.name}</h4>
      <p>${item.category}</p>
      <p>${formatLkr(item.price)} x ${item.quantity}</p>
    </div>
    <button class="ghost-button" type="button" data-remove-cart-item="${item.slug}">Remove</button>
  </article>
`;

const refreshCartUi = () => {
  const cart = readCart();
  const subtotal = cartSubtotal(cart);
  const threshold = Number(document.body.dataset.freeShippingThreshold || 30000);
  const progress = Math.min((subtotal / threshold) * 100, 100);

  document.querySelectorAll("[data-cart-count]").forEach((node) => {
    node.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
  });

  document.querySelectorAll("[data-cart-subtotal], [data-cart-subtotal-page]").forEach((node) => {
    node.textContent = formatLkr(subtotal);
  });

  document.querySelectorAll("[data-mini-cart-items], [data-cart-page-items]").forEach((node) => {
    if (!cart.length) {
      node.innerHTML = `<div class="shipping-result">Your cart is still empty. Add a few signature pieces to begin.</div>`;
      return;
    }
    node.innerHTML = cart.map(renderCartItem).join("");
  });

  document.querySelectorAll("[data-shipping-progress]").forEach((node) => {
    node.style.width = `${progress}%`;
  });

  document.querySelectorAll("[data-shipping-message]").forEach((node) => {
    if (subtotal >= threshold) {
      node.textContent = "You unlocked free shipping across Sri Lanka.";
    } else {
      node.textContent = `${formatLkr(threshold - subtotal)} away from free shipping.`;
    }
  });
};

const addToCart = (button) => {
  const cart = readCart();
  const slug = button.dataset.slug;
  const existing = cart.find((item) => item.slug === slug);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      slug,
      name: button.dataset.name,
      price: Number(button.dataset.price),
      image: button.dataset.image,
      category: button.dataset.category,
      quantity: 1,
    });
  }

  writeCart(cart);
  triggerHaptic();
  refreshCartUi();
  openMiniCart();
};

const removeFromCart = (slug) => {
  const cart = readCart().filter((item) => item.slug !== slug);
  writeCart(cart);
  refreshCartUi();
};

const miniCart = document.querySelector("[data-mini-cart]");
const overlay = document.querySelector("[data-page-overlay]");

const openMiniCart = () => {
  miniCart?.classList.add("is-open");
  overlay?.classList.add("is-open");
};

const closeMiniCart = () => {
  miniCart?.classList.remove("is-open");
  overlay?.classList.remove("is-open");
};

const updatePreview = (button) => {
  const imageId = button.dataset.previewTarget;
  const image = document.getElementById(imageId);
  if (!image) return;
  image.src = button.dataset.previewImage;
  image.closest(".product-card, .product-shell")?.querySelector("[data-add-to-cart]")?.setAttribute("data-image", button.dataset.previewImage);
};

const attachShippingLogic = () => {
  document.querySelectorAll("[data-shipping-select]").forEach((select) => {
    const output = select.parentElement?.querySelector("[data-shipping-result]");
    const sync = async () => {
      if (!output) return;
      try {
        const response = await fetch(`/api/shipping/${encodeURIComponent(select.value)}`);
        const data = await response.json();
        output.innerHTML = `<strong>${formatLkr(data.fee)}</strong> delivery fee<br>${data.eta}`;
      } catch {
        output.textContent = "Delivery estimate unavailable right now.";
      }
    };
    sync();
    select.addEventListener("change", sync);
  });
};

const attachFitModal = () => {
  const modal = document.querySelector("[data-fit-modal]");
  const openButton = document.querySelector("[data-open-fit-modal]");
  const submitButton = document.querySelector("[data-submit-fit]");
  const form = document.querySelector("[data-fit-form]");
  const result = document.querySelector("[data-fit-result]");

  openButton?.addEventListener("click", () => modal?.showModal());

  submitButton?.addEventListener("click", async () => {
    if (!form || !result) return;
    const formData = new FormData(form);
    const slug = form.dataset.productSlug;
    const params = new URLSearchParams({
      height_cm: String(formData.get("height_cm")),
      weight_kg: String(formData.get("weight_kg")),
      preference: String(formData.get("preference")),
    });

    result.textContent = "Calculating your fit...";
    try {
      const response = await fetch(`/api/fit/${slug}?${params.toString()}`);
      const data = await response.json();
      result.innerHTML = `<strong>${data.size}</strong><br>${data.message}<br>${data.fit_tip}`;
    } catch {
      result.textContent = "Fit recommendation is unavailable at the moment.";
    }
  });
};

const attachGuestCheckout = () => {
  document.querySelector("[data-guest-checkout]")?.addEventListener("click", () => {
    const fields = document.querySelectorAll(".checkout-form input");
    if (fields.length >= 3) {
      fields[0].value = "Guest Customer";
      fields[1].value = "+94 77 000 0000";
      fields[2].value = "Guest checkout address to be confirmed by SMS";
    }
  });
};

document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;

  const addButton = target.closest("[data-add-to-cart]");
  if (addButton instanceof HTMLElement) {
    addToCart(addButton);
  }

  const removeButton = target.closest("[data-remove-cart-item]");
  if (removeButton instanceof HTMLElement) {
    removeFromCart(removeButton.dataset.removeCartItem);
  }

  if (target.closest("[data-open-mini-cart]")) {
    openMiniCart();
  }

  if (target.closest("[data-close-mini-cart]") || target === overlay) {
    closeMiniCart();
  }

  const previewButton = target.closest("[data-preview-image]");
  if (previewButton instanceof HTMLElement) {
    updatePreview(previewButton);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  refreshCartUi();
  attachShippingLogic();
  attachFitModal();
  attachGuestCheckout();
});
