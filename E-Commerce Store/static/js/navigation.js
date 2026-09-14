/**
 * NOVA/FORM — Navigation
 * Scroll-based navbar state transitions, mobile menu, and search overlay.
 */

(function () {
  'use strict';

  const navbar = document.getElementById('navbar');
  const menuToggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const searchToggle = document.getElementById('search-toggle');
  const searchOverlay = document.getElementById('search-overlay');
  const searchClose = document.getElementById('search-close');
  const searchInput = document.getElementById('search-input');

  // ── Scroll-based navbar ──────────────────────────────────────
  let lastScroll = 0;

  function updateNavbar() {
    const scrollY = window.scrollY;

    // Only do transparent → solid if the page has a hero
    if (navbar.classList.contains('navbar--transparent') || navbar.classList.contains('navbar--solid')) {
      if (scrollY > 100) {
        navbar.classList.remove('navbar--transparent');
        navbar.classList.add('navbar--solid');
      } else {
        // Only go back to transparent if page started with transparent nav
        const isHomepage = document.querySelector('.hero');
        if (isHomepage) {
          navbar.classList.remove('navbar--solid');
          navbar.classList.add('navbar--transparent');
        }
      }
    }

    lastScroll = scrollY;
  }

  window.addEventListener('scroll', NovaUtils.debounce(updateNavbar, 10), { passive: true });
  updateNavbar();

  // ── Mobile menu ──────────────────────────────────────────────
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.contains('is-open');

      if (isOpen) {
        mobileMenu.classList.remove('is-open');
        menuToggle.classList.remove('is-active');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      } else {
        mobileMenu.classList.add('is-open');
        menuToggle.classList.add('is-active');
        menuToggle.setAttribute('aria-expanded', 'true');
        mobileMenu.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      }
    });

    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('is-open');
        menuToggle.classList.remove('is-active');
        document.body.style.overflow = '';
      });
    });
  }

  // ── Search overlay ───────────────────────────────────────────
  if (searchToggle && searchOverlay) {
    searchToggle.addEventListener('click', () => {
      searchOverlay.classList.add('is-open');
      searchOverlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      setTimeout(() => searchInput?.focus(), 300);
    });

    if (searchClose) {
      searchClose.addEventListener('click', () => {
        searchOverlay.classList.remove('is-open');
        searchOverlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && searchOverlay.classList.contains('is-open')) {
        searchOverlay.classList.remove('is-open');
        searchOverlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
  }

  // ── Keyboard navigation — close mobile menu on Escape ────────
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu?.classList.contains('is-open')) {
      mobileMenu.classList.remove('is-open');
      menuToggle.classList.remove('is-active');
      document.body.style.overflow = '';
    }
  });
})();
