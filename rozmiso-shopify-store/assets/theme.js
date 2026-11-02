/**
 * Rozmiso Flipkart-Style Enterprise Theme JavaScript
 * Dynamic behaviors: Countdown Timer, Hero Slider, Pincode Checker, Bundle Selector, Instant COD Checkout
 */

document.addEventListener('DOMContentLoaded', () => {
  initCountdownTimer();
  initHeroSlider();
  initPincodeChecker();
  initBundleSelector();
  initWishlistToggle();
});

/* ==========================================================================
   1. Live Countdown Timer (Deals of the Day)
   ========================================================================== */
function initCountdownTimer() {
  const timerElements = document.querySelectorAll('[data-fk-timer]');
  if (!timerElements.length) return;

  // Set an end time 4 hours and 35 minutes into the future, stored in sessionStorage for realism
  let targetTime = sessionStorage.getItem('fk_deal_timer_target');
  if (!targetTime) {
    targetTime = Date.now() + (4 * 3600 + 35 * 60 + 12) * 1000;
    sessionStorage.setItem('fk_deal_timer_target', targetTime);
  } else {
    targetTime = parseInt(targetTime, 10);
    if (Date.now() >= targetTime) {
      targetTime = Date.now() + 5 * 3600 * 1000;
      sessionStorage.setItem('fk_deal_timer_target', targetTime);
    }
  }

  function update() {
    const diff = Math.max(0, targetTime - Date.now());
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    const pad = n => String(n).padStart(2, '0');
    const formatted = `${pad(hours)}h : ${pad(mins)}m : ${pad(secs)}s`;

    timerElements.forEach(el => {
      el.textContent = formatted;
    });
  }

  update();
  setInterval(update, 1000);
}

/* ==========================================================================
   2. Hero Banner Slider
   ========================================================================== */
function initHeroSlider() {
  const slider = document.querySelector('.fk-hero-slider');
  if (!slider) return;

  const slides = slider.querySelectorAll('.fk-slide');
  const prevBtn = slider.querySelector('.fk-slider-nav.prev');
  const nextBtn = slider.querySelector('.fk-slider-nav.next');
  if (!slides.length) return;

  let current = 0;
  let autoTimer = null;

  function showSlide(index) {
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === index);
    });
    current = index;
  }

  function next() {
    const nxt = (current + 1) % slides.length;
    showSlide(nxt);
  }

  function prev() {
    const prv = (current - 1 + slides.length) % slides.length;
    showSlide(prv);
  }

  if (nextBtn) nextBtn.addEventListener('click', () => { next(); resetTimer(); });
  if (prevBtn) prevBtn.addEventListener('click', () => { prev(); resetTimer(); });

  function resetTimer() {
    clearInterval(autoTimer);
    autoTimer = setInterval(next, 5000);
  }

  resetTimer();
}

/* ==========================================================================
   3. Live PIN Code Checker for Indian Delivery & COD
   ========================================================================== */
function initPincodeChecker() {
  const forms = document.querySelectorAll('.fk-pincode-form');
  forms.forEach(form => {
    const input = form.querySelector('.fk-pincode-input');
    const btn = form.querySelector('.fk-pincode-btn');
    const status = form.closest('.fk-delivery-box')?.querySelector('.fk-pincode-status');

    if (!input || !btn || !status) return;

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      checkPin();
    });

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        checkPin();
      }
    });

    function checkPin() {
      const pin = input.value.trim();
      if (!/^\d{6}$/.test(pin)) {
        status.style.color = '#d32f2f';
        status.textContent = '⚠️ Please enter a valid 6-digit Indian Pincode (e.g. 560001)';
        return;
      }

      // Calculate realistic delivery date 3-4 days ahead
      const deliveryDate = new Date();
      deliveryDate.setDate(deliveryDate.getDate() + 3);
      const dateStr = deliveryDate.toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });

      status.style.color = '#388e3c';
      status.innerHTML = `✅ <b>Delivery to ${pin} available by ${dateStr}!</b><br><span style="color:#666; font-size:11px;">• Free Express Shipping • Cash on Delivery (COD) Available • 7 Days Replacement</span>`;
      localStorage.setItem('fk_verified_pincode', pin);
    }

    // Auto-fill from localStorage if previously verified
    const savedPin = localStorage.getItem('fk_verified_pincode');
    if (savedPin) {
      input.value = savedPin;
      checkPin();
    }
  });
}

/* ==========================================================================
   4. Tiered Bundle Quantity Selector (High Converting CRO)
   ========================================================================== */
function initBundleSelector() {
  const bundleWraps = document.querySelectorAll('.fk-bundles-box');
  bundleWraps.forEach(wrap => {
    const options = wrap.querySelectorAll('.fk-bundle-option');
    const variantSelect = document.querySelector('select[name="id"]');
    const priceDisplay = document.querySelector('.fk-pdp-price-current');
    const mrpDisplay = document.querySelector('.fk-pdp-price-mrp');
    const discountDisplay = document.querySelector('.fk-pdp-discount-rate');

    options.forEach(opt => {
      opt.addEventListener('click', () => {
        options.forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');

        const variantId = opt.getAttribute('data-variant-id');
        const price = opt.getAttribute('data-price');
        const mrp = opt.getAttribute('data-mrp');
        const discount = opt.getAttribute('data-discount');

        if (variantSelect && variantId) {
          variantSelect.value = variantId;
        }

        if (priceDisplay && price) priceDisplay.textContent = price;
        if (mrpDisplay && mrp) mrpDisplay.textContent = mrp;
        if (discountDisplay && discount) discountDisplay.textContent = discount;
      });
    });
  });
}

/* ==========================================================================
   5. Wishlist Toggle
   ========================================================================== */
function initWishlistToggle() {
  document.querySelectorAll('.fk-wishlist-icon').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isActive = btn.classList.toggle('active');
      btn.style.color = isActive ? '#e53935' : '#c2c2c2';
    });
  });
}
