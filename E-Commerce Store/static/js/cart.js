/**
 * NOVA/FORM — Cart Module
 * AJAX add-to-cart, cart drawer, quantity updates, and micro-interactions.
 */

(function () {
  'use strict';

  const cartToggle = document.getElementById('cart-toggle');
  const cartDrawer = document.getElementById('cart-drawer');
  const cartOverlay = document.getElementById('cart-overlay');
  const cartClose = document.getElementById('cart-close');

  // ── Cart Drawer Toggle ───────────────────────────────────────
  function openCartDrawer() {
    if (!cartDrawer || !cartOverlay) return;
    cartDrawer.classList.add('is-open');
    cartOverlay.classList.add('is-open');
    cartOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeCartDrawer() {
    if (!cartDrawer || !cartOverlay) return;
    cartDrawer.classList.remove('is-open');
    cartOverlay.classList.remove('is-open');
    cartOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (cartToggle) cartToggle.addEventListener('click', openCartDrawer);
  if (cartClose) cartClose.addEventListener('click', closeCartDrawer);
  if (cartOverlay) cartOverlay.addEventListener('click', closeCartDrawer);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && cartDrawer?.classList.contains('is-open')) {
      closeCartDrawer();
    }
  });

  // ── AJAX Cart Operations ─────────────────────────────────────
  function cartRequest(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': NovaUtils.getCSRFToken(),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams(data).toString(),
    }).then(res => res.json());
  }

  function updateCartUI(data) {
    // Update bag count
    const bagCount = document.getElementById('bag-count');
    const drawerBagCount = document.getElementById('drawer-bag-count');
    if (bagCount) bagCount.textContent = `(${data.cart_total_items})`;
    if (drawerBagCount) drawerBagCount.textContent = `(${data.cart_total_items})`;

    // Update drawer totals
    const drawerSubtotal = document.getElementById('drawer-subtotal');
    const drawerShipping = document.getElementById('drawer-shipping');
    const drawerTotal = document.getElementById('drawer-total');
    if (drawerSubtotal) drawerSubtotal.textContent = NovaUtils.formatPrice(data.cart_subtotal);
    if (drawerShipping) drawerShipping.textContent = parseFloat(data.cart_shipping) === 0 ? 'Complimentary' : NovaUtils.formatPrice(data.cart_shipping);
    if (drawerTotal) drawerTotal.textContent = NovaUtils.formatPrice(data.cart_total);

    // Rebuild drawer items
    const drawerItems = document.getElementById('cart-drawer-items');
    const drawerFooter = document.getElementById('cart-drawer-footer');

    if (drawerItems && data.cart_items) {
      if (data.cart_items.length === 0) {
        drawerItems.innerHTML = `
          <div class="cart-drawer__empty">
            <div class="cart-drawer__empty-text">Your bag is empty</div>
            <a href="${window.NOVAFORM.urls.shop}" class="btn btn--secondary">Continue Shopping</a>
          </div>`;
        if (drawerFooter) drawerFooter.style.display = 'none';
      } else {
        drawerItems.innerHTML = data.cart_items.map(item => `
          <div class="cart-item" data-product-id="${item.id}">
            <img src="${item.image}" alt="${item.name}" class="cart-item__image" loading="lazy" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 3 4%22><rect fill=%22%23F2EFEB%22 width=%223%22 height=%224%22/></svg>'">
            <div class="cart-item__details">
              <span class="cart-item__category">${item.category}</span>
              <span class="cart-item__name">${item.name}</span>
              <span class="cart-item__price">${NovaUtils.formatPrice(item.price)}</span>
              <div class="cart-item__actions">
                <div class="cart-item__qty">
                  <button class="cart-item__qty-btn" data-action="decrease" data-product-id="${item.id}" aria-label="Decrease quantity">−</button>
                  <span class="cart-item__qty-value">${item.quantity}</span>
                  <button class="cart-item__qty-btn" data-action="increase" data-product-id="${item.id}" aria-label="Increase quantity">+</button>
                </div>
                <button class="cart-item__remove" data-action="remove" data-product-id="${item.id}" aria-label="Remove ${item.name}">Remove</button>
              </div>
            </div>
          </div>`).join('');
        if (drawerFooter) drawerFooter.style.display = '';
      }
    }
  }

  // ── Add to Cart (product detail page) ────────────────────────
  const addToCartForm = document.getElementById('add-to-cart-form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = document.getElementById('add-to-cart-btn');
      const productId = addToCartForm.dataset.productId;
      const quantity = document.getElementById('qty-input')?.value || 1;

      // Button state change
      btn.classList.add('is-adding');
      btn.textContent = 'Adding...';

      cartRequest(window.NOVAFORM.urls.cartAdd, {
        product_id: productId,
        quantity: quantity,
      }).then(data => {
        if (data.success) {
          // Success state
          btn.classList.remove('is-adding');
          btn.classList.add('is-added');
          btn.textContent = 'Added to Bag ✓';

          // Update cart UI
          updateCartUI(data);

          // Open cart drawer
          setTimeout(() => openCartDrawer(), 300);

          // Toast
          NovaUtils.showToast(data.message, 'success');

          // Reset button after 2s
          setTimeout(() => {
            btn.classList.remove('is-added');
            btn.textContent = 'Add to Bag';
          }, 2000);
        } else {
          btn.classList.remove('is-adding');
          btn.textContent = 'Add to Bag';
          NovaUtils.showToast(data.message, 'error');
        }
      }).catch(() => {
        btn.classList.remove('is-adding');
        btn.textContent = 'Add to Bag';
        NovaUtils.showToast('Something went wrong. Please try again.', 'error');
      });
    });
  }

  // ── Cart Drawer Item Actions (delegated) ─────────────────────
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn || !btn.closest('.cart-drawer')) return;

    const action = btn.dataset.action;
    const productId = btn.dataset.productId;

    if (action === 'remove') {
      cartRequest(window.NOVAFORM.urls.cartRemove, {
        product_id: productId,
      }).then(data => {
        if (data.success) {
          updateCartUI(data);
          NovaUtils.showToast(data.message, 'success');
        }
      });
    } else if (action === 'increase' || action === 'decrease') {
      const item = btn.closest('.cart-item');
      const qtyEl = item?.querySelector('.cart-item__qty-value');
      let currentQty = parseInt(qtyEl?.textContent || 1);
      let newQty = action === 'increase' ? currentQty + 1 : currentQty - 1;

      if (newQty <= 0) {
        cartRequest(window.NOVAFORM.urls.cartRemove, {
          product_id: productId,
        }).then(data => {
          if (data.success) {
            updateCartUI(data);
            NovaUtils.showToast('Removed from bag.', 'success');
          }
        });
      } else {
        cartRequest(window.NOVAFORM.urls.cartUpdate, {
          product_id: productId,
          quantity: newQty,
        }).then(data => {
          if (data.success) {
            updateCartUI(data);
          } else {
            NovaUtils.showToast(data.message, 'error');
          }
        });
      }
    }
  });
})();
