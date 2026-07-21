/**
 * VeriLaw — Application Initializer
 * Entry point: loads shared modules, initializes global behaviours,
 * determines which page-specific module to run.
 * Depends on: utils.js, validation.js, api.js, auth.js, dashboard.js
 */

'use strict';

/* ── Theme Management ──────────────────────────────────────────────────── */

function initTheme() {
  const stored = window.VLUtils.storageGet('vl_theme') || 'light';
  document.documentElement.setAttribute('data-theme', stored);
  updateThemeToggleIcon(stored);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next    = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  window.VLUtils.storageSet('vl_theme', next);
  updateThemeToggleIcon(next);
}

function updateThemeToggleIcon(theme) {
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    btn.innerHTML = theme === 'dark' ? sunIcon() : moonIcon();
  });
}

function sunIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`;
}

function moonIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
}

/* ── Navbar ────────────────────────────────────────────────────────────── */

function initNavbar() {
  const hamburger = document.getElementById('navbar-hamburger');
  const mobileNav = document.getElementById('mobile-nav');

  if (!hamburger || !mobileNav) return;

  hamburger.addEventListener('click', () => {
    const isOpen = mobileNav.classList.toggle('open');
    hamburger.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', isOpen.toString());
  });

  // Close mobile nav when a link is clicked
  mobileNav.querySelectorAll('.mobile-nav__link').forEach(link => {
    link.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });

  // Close mobile nav when clicking outside
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !mobileNav.contains(e.target)) {
      mobileNav.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });

  // Sticky navbar shadow on scroll
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = window.VLUtils.throttle(() => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, 100);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Close mobile nav
        mobileNav.classList.remove('open');
        hamburger.classList.remove('open');
      }
    });
  });
}

/* ── Active Nav Link ───────────────────────────────────────────────────── */

function setActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar__link[href], .mobile-nav__link[href]').forEach(link => {
    const linkPage = link.getAttribute('href').split('/').pop();
    if (linkPage === currentPage) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });
}

/* ── Theme Toggle Button ───────────────────────────────────────────────── */

function initThemeToggles() {
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });
}

/* ── Global Modal Manager ──────────────────────────────────────────────── */

function initModals() {
  // Open modal on trigger click
  document.querySelectorAll('[data-modal-open]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = trigger.dataset.modalOpen;
      openModal(modalId);
    });
  });

  // Close modal on backdrop, close btn, or Escape
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeModal(backdrop.id);
    });
  });

  document.querySelectorAll('[data-modal-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      const backdrop = btn.closest('.modal-backdrop');
      if (backdrop) closeModal(backdrop.id);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const open = document.querySelector('.modal-backdrop.open');
      if (open) closeModal(open.id);
    }
  });
}

function openModal(modalId) {
  const backdrop = document.getElementById(modalId);
  if (!backdrop) return;
  backdrop.classList.add('open');
  document.body.style.overflow = 'hidden';
  // Focus first focusable element
  const firstFocusable = backdrop.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  if (firstFocusable) firstFocusable.focus();
}

function closeModal(modalId) {
  const backdrop = document.getElementById(modalId);
  if (!backdrop) return;
  backdrop.classList.remove('open');
  document.body.style.overflow = '';
}

/* ── Page Detection & Routing ──────────────────────────────────────────── */

function detectPage() {
  const path = window.location.pathname;
  const page = path.split('/').pop() || 'index.html';

  if (page === '' || page === 'index.html') return 'landing';
  if (page === 'login.html')                return 'login';
  if (page === 'register.html')             return 'register';
  if (page === 'dashboard.html')            return 'dashboard';
  return 'other';
}

/* ── Boot ──────────────────────────────────────────────────────────────── */

async function boot() {
  // Apply theme immediately to prevent flash
  initTheme();

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
  }

  const page = detectPage();

  // Global inits (run on every page)
  initNavbar();
  setActiveNavLink();
  initThemeToggles();
  initModals();
  window.VLUtils.initScrollAnimations();
  window.VLUtils.initCounters();

  // Page-specific inits
  switch (page) {
    case 'landing':
      initLandingPage();
      break;

    case 'login':
      window.VLAuth.redirectIfAuthenticated();
      window.VLAuth.initLoginForm();
      window.VLAuth.initGoogleAuth();
      window.VLAuth.initForgotPassword();
      break;

    case 'register':
      window.VLAuth.redirectIfAuthenticated();
      window.VLAuth.initRegisterForm();
      window.VLAuth.initGoogleAuth();
      break;

    case 'dashboard':
      await window.VLDashboard.initDashboard();
      window.VLDashboard.initAnalyticsPlaceholder();
      break;
  }
}

/* ── Landing Page Specific ─────────────────────────────────────────────── */

function initLandingPage() {
  // Smooth-scroll CTAs that link to sections on the same page
  document.querySelectorAll('[data-scroll-to]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.VLUtils.scrollTo(btn.dataset.scrollTo);
    });
  });

  // FAQ accordions
  window.VLDashboard.initAccordions();
}

/* ── Start the app ─────────────────────────────────────────────────────── */
boot().catch(err => {
  console.error('[VeriLaw] Boot error:', err);
});

/* ── Expose globally for debugging & inline event fallbacks ────────────── */
window.VLApp = {
  openModal,
  closeModal,
  toggleTheme,
  boot,
};
