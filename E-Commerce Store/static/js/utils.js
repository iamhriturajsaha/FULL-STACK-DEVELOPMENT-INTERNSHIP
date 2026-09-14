/**
 * NOVA/FORM — Utility Functions
 * Toast notifications, reduced-motion detection, helpers.
 */

const NovaUtils = {
  /**
   * Detect if user prefers reduced motion.
   */
  prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },

  /**
   * Detect touch device.
   */
  isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  },

  /**
   * Show a toast notification.
   */
  showToast(message, type = 'success', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    toast.setAttribute('role', 'status');
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        toast.classList.add('is-visible');
      });
    });

    // Auto dismiss
    setTimeout(() => {
      toast.classList.remove('is-visible');
      setTimeout(() => toast.remove(), 400);
    }, duration);
  },

  /**
   * Get CSRF token for AJAX requests.
   */
  getCSRFToken() {
    return window.NOVAFORM?.csrfToken || '';
  },

  /**
   * Debounce function.
   */
  debounce(fn, delay = 100) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  },

  /**
   * Lerp (linear interpolation).
   */
  lerp(start, end, factor) {
    return start + (end - start) * factor;
  },

  /**
   * Clamp value between min and max.
   */
  clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  },

  /**
   * Format price as currency string.
   */
  formatPrice(value) {
    return `$${parseFloat(value).toFixed(2)}`;
  }
};

// Make globally available
window.NovaUtils = NovaUtils;
