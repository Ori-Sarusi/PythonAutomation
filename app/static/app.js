// Products Data
const PRODUCTS = [
  { id: 1, name: "Noise-Cancelling Headphones", category: "Audio", price: 199.99, desc: "Premium wireless audio with active noise cancellation." },
  { id: 2, name: "Smart Fitness Watch", category: "Wearables", price: 89.50, desc: "Track steps, heart rate, and sleep metrics with AMOLED display." },
  { id: 3, name: "Mechanical Gaming Keyboard", category: "Accessories", price: 120.00, desc: "RGB backlit tactile mechanical keys." },
  { id: 4, name: "Ultra-Fast Wireless Charger", category: "Accessories", price: 29.99, desc: "15W fast charging stand for iOS and Android." },
  { id: 5, name: "Studio Microphone USB", category: "Audio", price: 79.99, desc: "Cardioid condenser mic with pop filter for podcasting." },
  { id: 6, name: "Ergonomic Vertical Mouse", category: "Accessories", price: 45.00, desc: "Reduces wrist strain with adjustable DPI optical sensor." }
];

// Users database in-memory
const USERS = [
  { username: "standard_user", email: "standard@example.com", password: "secret123", locked: false },
  { username: "locked_user", email: "locked@example.com", password: "secret123", locked: true }
];

let currentUser = null;
let cart = [];
let appliedDiscount = 0;

// DOM Elements
const loginSection = document.getElementById("login-section");
const loginFormContainer = document.getElementById("login-form-container");
const registerFormContainer = document.getElementById("register-form-container");
const tabLogin = document.getElementById("tab-login");
const tabRegister = document.getElementById("tab-register");

const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const registerForm = document.getElementById("register-form");
const registerError = document.getElementById("register-error");
const registerSuccess = document.getElementById("register-success");

const userDisplay = document.getElementById("user-display");
const usernameVal = document.getElementById("username-val");
const logoutBtn = document.getElementById("logout-btn");
const cartBtn = document.getElementById("cart-btn");
const cartCount = document.getElementById("cart-count");

// AUTH TABS TOGGLE
tabLogin.addEventListener("click", () => {
  tabLogin.classList.add("active");
  tabRegister.classList.remove("active");
  loginFormContainer.classList.remove("hidden");
  registerFormContainer.classList.add("hidden");
  loginError.classList.add("hidden");
});

tabRegister.addEventListener("click", () => {
  tabRegister.classList.add("active");
  tabLogin.classList.remove("active");
  registerFormContainer.classList.remove("hidden");
  loginFormContainer.classList.add("hidden");
  registerError.classList.add("hidden");
  registerSuccess.classList.add("hidden");
});

// 1. AUTHENTICATION - LOGIN
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  loginError.classList.add("hidden");

  const user = USERS.find(u => u.username === username && u.password === password);

  if (!user) {
    loginError.textContent = "Invalid username or password.";
    loginError.classList.remove("hidden");
    return;
  }

  if (user.locked) {
    loginError.textContent = "Epic sadface: Sorry, this user has been locked out.";
    loginError.classList.remove("hidden");
    return;
  }

  currentUser = user.username;
  usernameVal.textContent = user.username;
  userDisplay.classList.remove("hidden");
  logoutBtn.classList.remove("hidden");
  cartBtn.classList.remove("hidden");
  showView("products");
  renderProducts();
});

// 1.1 AUTHENTICATION - REGISTER
registerForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value.trim();
  const confirmPassword = document.getElementById("reg-confirm-password").value.trim();

  registerError.classList.add("hidden");
  registerSuccess.classList.add("hidden");

  if (password.length < 6) {
    registerError.textContent = "Password must be at least 6 characters long.";
    registerError.classList.remove("hidden");
    return;
  }

  if (password !== confirmPassword) {
    registerError.textContent = "Passwords do not match.";
    registerError.classList.remove("hidden");
    return;
  }

  if (USERS.some(u => u.username.toLowerCase() === username.toLowerCase())) {
    registerError.textContent = "Username already exists.";
    registerError.classList.remove("hidden");
    return;
  }

  // Register new user
  USERS.push({ username, email, password, locked: false });
  registerSuccess.textContent = "Account created successfully! You can now log in.";
  registerSuccess.classList.remove("hidden");
  registerForm.reset();
});

logoutBtn.addEventListener("click", () => {
  currentUser = null;
  cart = [];
  appliedDiscount = 0;
  updateCartBadge();
  userDisplay.classList.add("hidden");
  logoutBtn.classList.add("hidden");
  cartBtn.classList.add("hidden");
  loginForm.reset();
  showView("login");
});

// VIEW SWITCHER
function showView(view) {
  loginSection.classList.add("hidden");
  productsSection.classList.add("hidden");
  cartSection.classList.add("hidden");
  checkoutSection.classList.add("hidden");
  confirmationSection.classList.add("hidden");

  if (view === "login") loginSection.classList.remove("hidden");
  if (view === "products") productsSection.classList.remove("hidden");
  if (view === "cart") cartSection.classList.remove("hidden");
  if (view === "checkout") checkoutSection.classList.remove("hidden");
  if (view === "confirmation") confirmationSection.classList.remove("hidden");
}

// 2. PRODUCTS RENDERING & FILTERING
function renderProducts() {
  const query = searchInput.value.toLowerCase();
  const cat = categoryFilter.value;
  const sort = sortSelect.value;

  let list = PRODUCTS.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(query) || p.desc.toLowerCase().includes(query);
    const matchesCat = cat === "all" || p.category === cat;
    return matchesSearch && matchesCat;
  });

  // Intentional Bug 1: Alphabetical string sorting bug for prices (e.g. "120" before "29")
  if (sort === "price-asc") {
    list.sort((a, b) => String(a.price).localeCompare(String(b.price))); // BUG: string comparison instead of a.price - b.price
  } else if (sort === "price-desc") {
    list.sort((a, b) => String(b.price).localeCompare(String(a.price)));
  } else if (sort === "name-asc") {
    list.sort((a, b) => a.name.localeCompare(b.name));
  }

  productsGrid.innerHTML = list.map(item => `
    <div class="product-card" data-test="product-card-${item.id}">
      <div class="product-category">${item.category}</div>
      <h3 class="product-title" data-test="product-title">${item.name}</h3>
      <p class="product-desc">${item.desc}</p>
      <div class="product-footer">
        <span class="product-price" data-test="product-price">$${item.price.toFixed(2)}</span>
        <button class="btn secondary-btn" data-test="add-to-cart-${item.id}" onclick="addToCart(${item.id})">
          Add to Cart
        </button>
      </div>
    </div>
  `).join("");
}

searchInput.addEventListener("input", renderProducts);
categoryFilter.addEventListener("change", renderProducts);
sortSelect.addEventListener("change", renderProducts);

// 3. CART ACTIONS
window.addToCart = function(id) {
  const item = PRODUCTS.find(p => p.id === id);
  if (item) {
    cart.push(item);
    updateCartBadge();
  }
};

function updateCartBadge() {
  cartCount.textContent = cart.length;
}

cartBtn.addEventListener("click", () => {
  renderCart();
  showView("cart");
});

closeCartBtn.addEventListener("click", () => {
  showView("products");
});

function renderCart() {
  if (cart.length === 0) {
    cartItemsContainer.innerHTML = `<p class="subtitle">Your cart is empty.</p>`;
  } else {
    cartItemsContainer.innerHTML = cart.map((item, index) => `
      <div class="cart-row" data-test="cart-row">
        <div>
          <h4>${item.name}</h4>
          <span class="product-price">$${item.price.toFixed(2)}</span>
        </div>
        <button class="btn text-btn" data-test="remove-cart-item" onclick="removeFromCart(${index})" style="color: var(--danger)">Remove</button>
      </div>
    `).join("");
  }

  calculateTotals();
}

window.removeFromCart = function(index) {
  cart.splice(index, 1);
  updateCartBadge();
  renderCart();
};

// Intentional Bug 2: Coupon calculation discounts first item price only rather than total cart subtotal
applyCouponBtn.addEventListener("click", () => {
  const code = couponInput.value.trim().toUpperCase();
  if (code === "SAVE10") {
    if (cart.length > 0) {
      appliedDiscount = cart[0].price * 0.10; // BUG: 10% of first item instead of total subtotal
      couponMsg.textContent = "Coupon 'SAVE10' applied (10% off)!";
      couponMsg.style.color = "var(--success)";
      couponMsg.classList.remove("hidden");
    }
  } else {
    couponMsg.textContent = "Invalid coupon code.";
    couponMsg.style.color = "var(--danger)";
    couponMsg.classList.remove("hidden");
    appliedDiscount = 0;
  }
  calculateTotals();
});

function calculateTotals() {
  const subtotal = cart.reduce((sum, item) => sum + item.price, 0);
  const total = Math.max(0, subtotal - appliedDiscount);

  subtotalVal.textContent = `$${subtotal.toFixed(2)}`;
  discountVal.textContent = `$${appliedDiscount.toFixed(2)}`;
  totalVal.textContent = `$${total.toFixed(2)}`;
}

// 4. CHECKOUT
proceedCheckoutBtn.addEventListener("click", () => {
  if (cart.length === 0) {
    alert("Please add items to your cart before proceeding.");
    return;
  }
  showView("checkout");
});

cancelCheckoutBtn.addEventListener("click", () => {
  showView("cart");
});

// Intentional Bug 3: No validation check on postal code field even though requirement states required
checkoutForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const firstName = document.getElementById("first-name").value.trim();
  const lastName = document.getElementById("last-name").value.trim();
  
  if (!firstName || !lastName) {
    checkoutError.textContent = "Please fill in all required fields.";
    checkoutError.classList.remove("hidden");
    return;
  }

  // Completing Order
  document.getElementById("order-id").textContent = `#TV-${Math.floor(1000 + Math.random() * 9000)}`;
  cart = [];
  appliedDiscount = 0;
  updateCartBadge();
  checkoutForm.reset();
  showView("confirmation");
});

backHomeBtn.addEventListener("click", () => {
  showView("products");
});
