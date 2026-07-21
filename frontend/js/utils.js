/**
 * VeriLaw — Utility Functions
 * Helper functions: toast system, skeleton loaders, date formatting,
 * debounce, DOM helpers, number formatting, local storage, counter animation.
 */

'use strict';

/* ── Toast Notification System ─────────────────────────────────────────── */

/**
 * Show a toast notification.
 * @param {Object} options
 * @param {'success'|'error'|'warning'|'info'} options.type
 * @param {string} options.title
 * @param {string} [options.message]
 * @param {number} [options.duration=3000]
 */
function showToast({ type = 'info', title, message = '', duration = 3000 }) {
  const container = getOrCreateToastContainer();

  const icons = {
    success: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>`,
    error:   `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
    warning: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>`,
    info:    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`,
  };

  const toast = document.createElement('div');
  toast.className = `toast toast--${type} fade-in`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.innerHTML = `
    <div class="toast__icon">${icons[type]}</div>
    <div class="toast__content">
      <div class="toast__title">${escapeHtml(title)}</div>
      ${message ? `<div class="toast__message">${escapeHtml(message)}</div>` : ''}
    </div>
    <button class="toast__dismiss" aria-label="Dismiss notification">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  `;

  container.appendChild(toast);

  const dismiss = toast.querySelector('.toast__dismiss');
  dismiss.addEventListener('click', () => dismissToast(toast));

  if (duration > 0) {
    setTimeout(() => dismissToast(toast), duration);
  }

  return toast;
}

function dismissToast(toast) {
  if (!toast || toast.classList.contains('dismissing')) return;
  toast.classList.add('dismissing');
  toast.addEventListener('animationend', () => toast.remove(), { once: true });
  setTimeout(() => toast.remove(), 400);
}

function getOrCreateToastContainer() {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    container.setAttribute('aria-label', 'Notifications');
    document.body.appendChild(container);
  }
  return container;
}

/* ── Skeleton Loader ───────────────────────────────────────────────────── */

/**
 * Show skeleton loaders by adding the 'hidden' class to real content
 * and removing 'hidden' from skeletons.
 */
function showSkeletons(wrapperSelector) {
  const wrapper = document.querySelector(wrapperSelector);
  if (!wrapper) return;
  wrapper.querySelectorAll('[data-skeleton]').forEach(el => el.classList.remove('hidden'));
  wrapper.querySelectorAll('[data-content]').forEach(el => el.classList.add('hidden'));
}

function hideSkeletons(wrapperSelector) {
  const wrapper = document.querySelector(wrapperSelector);
  if (!wrapper) return;
  wrapper.querySelectorAll('[data-skeleton]').forEach(el => el.classList.add('hidden'));
  wrapper.querySelectorAll('[data-content]').forEach(el => el.classList.remove('hidden'));
}

/* ── Animated Counter ──────────────────────────────────────────────────── */

/**
 * Animate a number counting up from 0 to the target value.
 * @param {HTMLElement} element
 * @param {number} target
 * @param {number} [duration=1500]
 * @param {string} [suffix='']
 */
function animateCounter(element, target, duration = 1500, suffix = '') {
  if (!element) return;
  const start = performance.now();
  const startValue = 0;

  function update(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = Math.round(startValue + eased * (target - startValue));
    element.textContent = formatNumber(current) + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

/**
 * Trigger counter animations for all elements with [data-counter] attribute.
 */
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.counter, 10);
        const suffix = el.dataset.suffix || '';
        animateCounter(el, target, 1500, suffix);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  counters.forEach(counter => observer.observe(counter));
}

/* ── Scroll Animations ─────────────────────────────────────────────────── */

/**
 * Animate elements as they scroll into view using IntersectionObserver.
 */
function initScrollAnimations() {
  const elements = document.querySelectorAll('[data-animate]');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const animation = el.dataset.animate || 'fade-in-up';
        el.classList.add(animation);
        el.style.animationFillMode = 'both';
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.1 });

  elements.forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });
}

/* ── Date & Time Helpers ───────────────────────────────────────────────── */

/**
 * Format a date as "July 21, 2026"
 * @param {Date|string} date
 * @returns {string}
 */
function formatDate(date) {
  const d = date instanceof Date ? date : new Date(date);
  return d.toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
}

/**
 * Format a date as "21 Jul 2026, 10:30 AM"
 * @param {Date|string} date
 * @returns {string}
 */
function formatDateTime(date) {
  const d = date instanceof Date ? date : new Date(date);
  return d.toLocaleDateString('en-IN', {
    year: 'numeric', month: 'short', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  });
}

/**
 * Return a human-readable relative time (e.g., "2 hours ago")
 * @param {Date|string} date
 * @returns {string}
 */
function timeAgo(date) {
  const d = date instanceof Date ? date : new Date(date);
  const seconds = Math.floor((Date.now() - d.getTime()) / 1000);
  const intervals = [
    [31536000, 'year'],  [2592000, 'month'],
    [86400, 'day'],      [3600, 'hour'],
    [60, 'minute'],      [1, 'second'],
  ];
  for (const [secs, label] of intervals) {
    const count = Math.floor(seconds / secs);
    if (count >= 1) return `${count} ${label}${count !== 1 ? 's' : ''} ago`;
  }
  return 'just now';
}

/* ── Number & String Helpers ───────────────────────────────────────────── */

/**
 * Format a number with commas (e.g. 12000 → "12,000")
 */
function formatNumber(n) {
  return n.toLocaleString('en-IN');
}

/**
 * Truncate text to a max length with an ellipsis.
 */
function truncate(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength).trimEnd() + '…';
}

/**
 * Escape HTML special characters to prevent XSS.
 */
function escapeHtml(str) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(str).replace(/[&<>"']/g, ch => map[ch]);
}

/**
 * Convert a string to title case.
 */
function toTitleCase(str) {
  return str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase());
}

/* ── Debounce ──────────────────────────────────────────────────────────── */

/**
 * Return a debounced version of fn that fires after `wait` ms of silence.
 */
function debounce(fn, wait = 300) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), wait);
  };
}

/**
 * Return a throttled version of fn that fires at most once per `wait` ms.
 */
function throttle(fn, wait = 100) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= wait) {
      last = now;
      fn.apply(this, args);
    }
  };
}

/* ── Local Storage Helpers ─────────────────────────────────────────────── */

function storageGet(key, defaultValue = null) {
  try {
    const value = localStorage.getItem(key);
    return value !== null ? JSON.parse(value) : defaultValue;
  } catch {
    return defaultValue;
  }
}

function storageSet(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

function storageRemove(key) {
  try {
    localStorage.removeItem(key);
  } catch { /* ignore */ }
}

/* ── DOM Helpers ───────────────────────────────────────────────────────── */

/**
 * Select a single element; throws a descriptive error if not found.
 */
function qs(selector, context = document) {
  const el = context.querySelector(selector);
  return el;
}

/**
 * Select all matching elements as an Array.
 */
function qsa(selector, context = document) {
  return Array.from(context.querySelectorAll(selector));
}

/**
 * Add one or more event listeners with optional cleanup.
 */
function on(element, events, handler, options) {
  if (!element) return () => {};
  const evts = events.split(' ');
  evts.forEach(evt => element.addEventListener(evt, handler, options));
  return () => evts.forEach(evt => element.removeEventListener(evt, handler, options));
}

/**
 * Delegate events from a parent to matching children.
 */
function delegate(parent, eventType, selector, handler) {
  if (!parent) return;
  parent.addEventListener(eventType, (e) => {
    const target = e.target.closest(selector);
    if (target && parent.contains(target)) handler.call(target, e);
  });
}

/**
 * Smoothly scroll to an element.
 */
function scrollTo(selector) {
  const el = document.querySelector(selector);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Get current date formatted for the welcome card.
 */
function getFormattedDate() {
  return new Date().toLocaleDateString('en-IN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
}

/* ── File Helpers ──────────────────────────────────────────────────────── */

/**
 * Format a file size in human-readable units.
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${units[i]}`;
}

/**
 * Return a file type icon name based on extension.
 */
function getFileIcon(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  const map = {
    pdf: 'file-text', jpg: 'image', jpeg: 'image', png: 'image',
    mp3: 'music', wav: 'music', doc: 'file', docx: 'file',
  };
  return map[ext] || 'file';
}

/* ── Exports (available globally) ─────────────────────────────────────── */
window.VLUtils = {
  showToast,
  showSkeletons,
  hideSkeletons,
  animateCounter,
  initCounters,
  initScrollAnimations,
  formatDate,
  formatDateTime,
  timeAgo,
  formatNumber,
  truncate,
  escapeHtml,
  toTitleCase,
  debounce,
  throttle,
  storageGet,
  storageSet,
  storageRemove,
  qs,
  qsa,
  on,
  delegate,
  scrollTo,
  getFormattedDate,
  formatFileSize,
  getFileIcon,
};
