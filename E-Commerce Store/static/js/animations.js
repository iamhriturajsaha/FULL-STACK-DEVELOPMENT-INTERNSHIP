/**
 * NOVA/FORM — Animations
 * GSAP-powered hero entrance, scroll reveals, and section transitions.
 * Gracefully degrades when GSAP is not loaded or reduced-motion is preferred.
 */

(function () {
  'use strict';

  // Wait for GSAP to load
  function initAnimations() {
    if (typeof gsap === 'undefined') {
      // Fallback: just show everything
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
      return;
    }

    const reducedMotion = NovaUtils.prefersReducedMotion();

    // Register ScrollTrigger
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);
    }

    // ── Hero Entrance Animation ──────────────────────────────
    const hero = document.getElementById('hero');
    if (hero && !reducedMotion) {
      const tl = gsap.timeline({ delay: 0.3 });

      // Image scale reveal
      tl.to('#hero-image', {
        scale: 1,
        duration: 1.8,
        ease: 'power3.out',
      }, 0);


      // Title words stagger
      tl.to('.hero__title-word', {
        y: 0,
        opacity: 1,
        duration: 1,
        stagger: 0.12,
        ease: 'power3.out',
      }, 0.5);

      // Subtitle
      tl.to('#hero-subtitle', {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
      }, 1);

      // CTA
      tl.to('#hero-cta', {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
      }, 1.2);

      // Enter Button
      if (document.getElementById('hero-enter')) {
        tl.to('#hero-enter', {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
        }, 1.4);
      }

      // Set initial states for GSAP
      gsap.set('#hero-subtitle', { opacity: 0, y: 20 });
      gsap.set('#hero-cta', { opacity: 0, y: 20 });
      if (document.getElementById('hero-enter')) {
        gsap.set('#hero-enter', { opacity: 0, y: 20 });
      }


    } else if (hero && reducedMotion) {
      // Show everything immediately
      gsap.set('.hero__title-word', { y: 0, opacity: 1 });
      gsap.set('#hero-subtitle, #hero-cta, #hero-enter', { opacity: 1, y: 0 });
      gsap.set('#hero-image', { scale: 1 });
    }

    // ── Scroll Reveal Animations ─────────────────────────────
    if (!reducedMotion && typeof ScrollTrigger !== 'undefined') {
      document.querySelectorAll('.reveal').forEach((el) => {
        ScrollTrigger.create({
          trigger: el,
          start: 'top 85%',
          once: true,
          onEnter: () => el.classList.add('is-visible'),
        });
      });

      // Parallax on hero image
      if (hero) {
        gsap.to('#hero-image', {
          y: '15%',
          ease: 'none',
          scrollTrigger: {
            trigger: hero,
            start: 'top top',
            end: 'bottom top',
            scrub: true,
          },
        });
      }
    } else {
      // Show all reveals immediately
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
    }
  }

  // Run after DOM ready and GSAP loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      // Small delay to ensure GSAP is parsed
      setTimeout(initAnimations, 50);
    });
  } else {
    setTimeout(initAnimations, 50);
  }
})();
