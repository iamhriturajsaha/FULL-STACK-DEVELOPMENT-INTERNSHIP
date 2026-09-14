/**
 * NOVA/FORM — Product Page
 * Image gallery, thumbnails, quantity selector, and accordion.
 */

(function () {
  'use strict';

  // ── Image Gallery ──────────────────────────────────────────
  const mainImage = document.getElementById('main-product-image');
  const thumbs = document.querySelectorAll('.product-gallery__thumb');

  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        const newSrc = thumb.dataset.image;
        if (!newSrc) return;

        // Fade transition
        mainImage.style.opacity = '0';
        setTimeout(() => {
          mainImage.src = newSrc;
          mainImage.style.opacity = '1';
        }, 200);

        // Update active state
        thumbs.forEach(t => t.classList.remove('is-active'));
        thumb.classList.add('is-active');
      });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!document.querySelector('.product-gallery')) return;

      const activeIndex = Array.from(thumbs).findIndex(t => t.classList.contains('is-active'));

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        const next = (activeIndex + 1) % thumbs.length;
        thumbs[next].click();
        thumbs[next].focus();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        const prev = (activeIndex - 1 + thumbs.length) % thumbs.length;
        thumbs[prev].click();
        thumbs[prev].focus();
      }
    });
  }

  // ── Quantity Selector ──────────────────────────────────────
  const qtyInput = document.getElementById('qty-input');
  const qtyDecrease = document.getElementById('qty-decrease');
  const qtyIncrease = document.getElementById('qty-increase');

  if (qtyInput) {
    const min = parseInt(qtyInput.min) || 1;
    const max = parseInt(qtyInput.max) || 99;

    if (qtyDecrease) {
      qtyDecrease.addEventListener('click', () => {
        const current = parseInt(qtyInput.value);
        if (current > min) qtyInput.value = current - 1;
      });
    }

    if (qtyIncrease) {
      qtyIncrease.addEventListener('click', () => {
        const current = parseInt(qtyInput.value);
        if (current < max) qtyInput.value = current + 1;
      });
    }

    // Validate on blur
    qtyInput.addEventListener('blur', () => {
      let val = parseInt(qtyInput.value);
      if (isNaN(val) || val < min) val = min;
      if (val > max) val = max;
      qtyInput.value = val;
    });
  }

  // ── Product Details Accordion ──────────────────────────────
  document.querySelectorAll('.product-details__toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const item = toggle.closest('.product-details__item');
      const content = item.querySelector('.product-details__content');
      const isOpen = item.classList.contains('is-open');

      if (isOpen) {
        content.style.maxHeight = '0';
        item.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        item.classList.add('is-open');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // ── Mobile swipe support for gallery ───────────────────────
  const gallery = document.querySelector('.product-gallery__main');
  if (gallery && thumbs.length > 1) {
    let touchStartX = 0;
    let touchEndX = 0;

    gallery.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    gallery.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const diff = touchStartX - touchEndX;

      if (Math.abs(diff) > 50) {
        const activeIndex = Array.from(thumbs).findIndex(t => t.classList.contains('is-active'));
        if (diff > 0) {
          // Swipe left — next
          const next = (activeIndex + 1) % thumbs.length;
          thumbs[next].click();
        } else {
          // Swipe right — prev
          const prev = (activeIndex - 1 + thumbs.length) % thumbs.length;
          thumbs[prev].click();
        }
      }
    }, { passive: true });
  }
})();
