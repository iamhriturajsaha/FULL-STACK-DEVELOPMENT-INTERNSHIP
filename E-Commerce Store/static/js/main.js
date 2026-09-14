/**
 * NOVA/FORM — Main Entry Point
 * Loading screen, app initialization, and page transition handling.
 */

(function () {
  'use strict';

  // ── Loading Screen ─────────────────────────────────────────
  const loadingScreen = document.getElementById('loading-screen');
  const loadingProgress = document.getElementById('loading-progress');

  function hideLoadingScreen() {
    if (!loadingScreen) return;

    // Animate progress bar
    if (loadingProgress) {
      loadingProgress.style.width = '100%';
    }

    // Hide after brief delay
    setTimeout(() => {
      loadingScreen.classList.add('is-hidden');
    }, 400);
  }

  // Show loading progress
  if (loadingProgress) {
    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += Math.random() * 30;
      if (progress > 80) {
        clearInterval(progressInterval);
        progress = 80;
      }
      loadingProgress.style.width = `${progress}%`;
    }, 100);

    // Complete on window load
    window.addEventListener('load', () => {
      clearInterval(progressInterval);
      hideLoadingScreen();
    });

    // Fallback: hide after 2s max
    setTimeout(() => {
      clearInterval(progressInterval);
      hideLoadingScreen();
    }, 2000);
  } else {
    window.addEventListener('load', hideLoadingScreen);
  }

  // Reduced motion: skip loading
  if (NovaUtils.prefersReducedMotion() && loadingScreen) {
    loadingScreen.classList.add('is-hidden');
  }

  // ── Focus visible polyfill ─────────────────────────────────
  // Only show focus ring on keyboard navigation
  document.addEventListener('mousedown', () => {
    document.body.classList.add('using-mouse');
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      document.body.classList.remove('using-mouse');
    }
  });

  // ── Image error fallback ───────────────────────────────────
  document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function () {
      if (!this.dataset.errorHandled) {
        this.dataset.errorHandled = 'true';
        this.style.backgroundColor = '#F2EFEB';
        this.alt = this.alt || 'Image unavailable';
      }
    });
  });

  // ── Smooth scroll for anchor links ─────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const id = this.getAttribute('href');
      if (id === '#') return;

      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

})();
