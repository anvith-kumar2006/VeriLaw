/* =======================================================
GLOBAL CONFIG
======================================================= */
const API_BASE    = '/api/v1';
const API_TIMEOUT = 10000; // 10 seconds

/* =======================================================
CONSTANTS
======================================================= */
const SESSION_KEY   = 'vl_token';
const USER_KEY      = 'vl_user';
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf', 'audio/mpeg', 'audio/wav'];
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB

/* =======================================================
GLOBAL VARIABLES
======================================================= */
// State shared across the app shell if needed

/* =======================================================
UTILITY FUNCTIONS
======================================================= */
const VLUtils = {
  showToast({ type = 'info', title, message = '', duration = 3000 }) {
    const container = document.getElementById('toast-container') || (() => {
      const c = document.createElement('div');
      c.id = 'toast-container';
      c.className = 'toast-container';
      c.setAttribute('aria-label', 'Notifications');
      document.body.appendChild(c);
      return c;
    })();

    const icons = {
      success: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>`,
      error:   `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
      warning: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>`,
      info:    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`,
    };

    const toast = document.createElement('div');
    toast.className = `toast toast--${type} fade-in`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
      <div class="toast__icon">${icons[type]}</div>
      <div class="toast__content">
        <div class="toast__title">${this.escapeHtml(title)}</div>
        ${message ? `<div class="toast__message">${this.escapeHtml(message)}</div>` : ''}
      </div>
      <button class="toast__dismiss" aria-label="Dismiss notification">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>`;

    container.appendChild(toast);
    toast.querySelector('.toast__dismiss').onclick = () => toast.remove();
    if (duration > 0) setTimeout(() => toast.remove(), duration);
  },

  animateCounter(element, target, duration = 1500, suffix = '') {
    if (!element) return;
    const start = performance.now();
    const update = (currentTime) => {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      const current = Math.round(progress * target);
      element.textContent = current.toLocaleString('en-IN') + suffix;
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  },

  initCounters() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateCounter(entry.target, parseInt(entry.target.dataset.counter), 1500, entry.target.dataset.suffix || '');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('[data-counter]').forEach(c => observer.observe(c));
  },

  initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add(entry.target.dataset.animate || 'fade-in-up');
          entry.target.style.opacity = '1';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-animate]').forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  },

  escapeHtml(str) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(str).replace(/[&<>"']/g, ch => map[ch]);
  },

  storageGet(key) { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } },
  storageSet(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); } catch {} },
  storageRemove(key) { localStorage.removeItem(key); },

  formatDate(date) { return new Date(date).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' }); },
  timeAgo(date) {
    const seconds = Math.floor((Date.now() - new Date(date).getTime()) / 1000);
    const intervals = [[31536000, 'year'], [2592000, 'month'], [86400, 'day'], [3600, 'hour'], [60, 'minute'], [1, 'second']];
    for (const [secs, label] of intervals) {
      const count = Math.floor(seconds / secs);
      if (count >= 1) return `${count} ${label}${count !== 1 ? 's' : ''} ago`;
    }
    return 'just now';
  },

  debounce(fn, wait = 300) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn.apply(this, args), wait);
    };
  },

  throttle(fn, wait = 100) {
    let last = 0;
    return (...args) => {
      const now = Date.now();
      if (now - last >= wait) { last = now; fn.apply(this, args); }
    };
  },

  getFormattedDate() { return new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }); },
  formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${['B', 'KB', 'MB', 'GB'][i]}`;
  }
};
window.VLUtils = VLUtils;

/* =======================================================
HELPERS (SVG Icons & UI UI States)
======================================================= */
const VLHelpers = {
  eyeIcon: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>`,
  eyeOffIcon: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></svg>`,
  uploadSvg: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
  checkSvg: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>`,
  alertSvg: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>`,
  fileSvg: () => `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
  
  setButtonLoading(btn, loading, label) {
    if (!btn) return;
    btn.disabled = loading;
    btn.classList.toggle('btn--loading', loading);
    const textEl = btn.querySelector('.btn__text');
    if (textEl) textEl.textContent = label;
  }
};

/* =======================================================
API CONFIGURATION & FUNCTIONS
======================================================= */
const VLAPI = {
  async request(endpoint, options = {}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), API_TIMEOUT);
    const token = VLUtils.storageGet(SESSION_KEY);
    const headers = { ...options.headers };
    if (!options.isFormData) headers['Content-Type'] = 'application/json';
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers, signal: controller.signal });
      clearTimeout(timeout);
      if (!response.ok) return { success: false, message: `Error ${response.status}`, data: null };
      return await response.json();
    } catch (err) {
      clearTimeout(timeout);
      return { success: false, message: err.name === 'AbortError' ? 'Timeout' : 'Network Error', data: null };
    }
  },

  // Auth
  async loginUser(credentials) {
    return new Promise(res => setTimeout(() => res({ success: true, data: { token: 'stub', user: { full_name: 'Demo User', email: credentials.email, role: 'citizen' } } }), 1000));
  },
  async registerUser(userData) {
    return new Promise(res => setTimeout(() => res({ success: true, message: 'Registered' }), 1200));
  },
  async logoutUser() {
    return new Promise(res => setTimeout(() => res({ success: true }), 300));
  },

  // Dashboard & Data
  async fetchDashboard() {
    return new Promise(res => setTimeout(() => res({
      success: true,
      data: {
        stats: { documents_verified: 24, pending_verifications: 3, fraud_alerts: 1, recent_uploads: 7 },
        recent_activity: [{ id: 1, type: 'upload', title: 'Doc Uploaded', description: 'Aadhaar.pdf uploaded.', time: new Date().toISOString() }],
        recent_documents: [{ id: 1, name: 'Rental Agreement', category: 'Legal', status: 'Verified', date: new Date().toISOString() }]
      }
    }), 800));
  },
  async fetchNotifications() {
    return new Promise(res => setTimeout(() => res({ success: true, data: { unread_count: 2, notifications: [{ id: 1, title: 'Complete', text: 'Verified', time: new Date().toISOString(), read: false }] } }), 600));
  },
  async uploadDocument(formData, onProgress) {
    return new Promise(res => {
      let pct = 0;
      const int = setInterval(() => { pct += 20; if(onProgress) onProgress(Math.min(pct, 95)); if(pct >= 100) clearInterval(int); }, 200);
      setTimeout(() => { if(onProgress) onProgress(100); res({ success: true, data: { file_id: 123 } }); }, 1500);
    });
  },
  async deleteDocument(id) { return new Promise(res => setTimeout(() => res({ success: true }), 400)); }
};
window.VLAPI = VLAPI;

/* =======================================================
AUTHENTICATION & TOKEN MANAGEMENT
======================================================= */
const VLAuth = {
  setSession(token, user) { VLUtils.storageSet(SESSION_KEY, token); VLUtils.storageSet(USER_KEY, user); },
  clearSession() { VLUtils.storageRemove(SESSION_KEY); VLUtils.storageRemove(USER_KEY); },
  getToken: () => VLUtils.storageGet(SESSION_KEY),
  getCurrentUser: () => VLUtils.storageGet(USER_KEY),
  isAuthenticated() { return !!this.getToken(); },
  redirectIfAuthenticated() { if (this.isAuthenticated()) window.location.href = 'dashboard.html'; },
  requireAuth() { if (!this.isAuthenticated()) window.location.href = 'login.html'; },

  async logoutUser() {
    try { await VLAPI.logoutUser(); } finally {
      this.clearSession();
      VLUtils.showToast({ type: 'info', title: 'Logged Out' });
      setTimeout(() => { window.location.href = 'login.html'; }, 800);
    }
  }
};
window.VLAuth = VLAuth;

/* =======================================================
VALIDATION (Field & Form)
======================================================= */
const VLValidation = {
  validateEmail: (v) => (!v || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) ? { valid: false, message: 'Valid email required.' } : { valid: true },
  validatePassword: (v) => (!v || v.length < 8) ? { valid: false, message: 'Min 8 chars.' } : { valid: true },
  validatePhone: (v) => (v.replace(/\D/g, '').length !== 10) ? { valid: false, message: '10 digits required.' } : { valid: true },
  validateRequired: (v, n) => (!v || !v.trim()) ? { valid: false, message: `${n} required.` } : { valid: true },

  setFieldError(input, msg) {
    const group = input.closest('.form-group');
    if (!group) return;
    group.classList.add('form-group--error');
    let err = group.querySelector('.form-error') || document.createElement('p');
    err.className = 'form-error'; err.textContent = msg;
    if (!group.querySelector('.form-error')) group.appendChild(err);
  },
  setFieldSuccess(input) {
    const group = input.closest('.form-group');
    if (group) { group.classList.remove('form-group--error'); group.classList.add('form-group--success'); }
  },
  clearFieldState(input) {
    const group = input.closest('.form-group');
    if (group) { group.classList.remove('form-group--error', 'form-group--success'); }
  },

  bindRealTimeValidation(input, validator, args = []) {
    if (!input) return;
    const handler = () => {
      const res = validator(input.value, ...args);
      if (input.value === '') this.clearFieldState(input);
      else if (res.valid) this.setFieldSuccess(input);
      else this.setFieldError(input, res.message);
    };
    input.addEventListener('blur', handler);
    input.addEventListener('input', VLUtils.debounce(handler, 400));
  },

  updatePasswordStrengthUI(pass, meter) {
    if (!meter) return;
    let score = 0;
    if (pass.length >= 8) score++;
    if (pass.length >= 12) score++;
    if (/[A-Z]/.test(pass) && /\d/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;
    const bars = meter.querySelectorAll('.password-strength__bar');
    bars.forEach((b, i) => b.classList.toggle('active-strong', i < score));
  }
};
window.VLValidation = VLValidation;

/* =======================================================
LOGIN & SIGNUP
======================================================= */
function initLoginForm() {
  const form = document.getElementById('login-form');
  if (!form) return;
  const email = document.getElementById('login-email'), pass = document.getElementById('login-password');
  VLValidation.bindRealTimeValidation(email, VLValidation.validateEmail);
  
  form.onsubmit = async (e) => {
    e.preventDefault();
    VLHelpers.setButtonLoading(document.getElementById('login-submit'), true, 'Logging in...');
    const res = await VLAPI.loginUser({ email: email.value, password: pass.value });
    if (res.success) {
      VLAuth.setSession(res.data.token, res.data.user);
      VLUtils.showToast({ type: 'success', title: 'Login Success' });
      setTimeout(() => window.location.href = 'dashboard.html', 1000);
    } else {
      VLHelpers.setButtonLoading(document.getElementById('login-submit'), false, 'Login');
      VLUtils.showToast({ type: 'error', title: 'Login Failed' });
    }
  };
}

function initRegisterForm() {
  const form = document.getElementById('register-form');
  if (!form) return;
  const email = document.getElementById('reg-email'), pass = document.getElementById('reg-password'), meter = document.getElementById('password-strength');
  pass.oninput = () => VLValidation.updatePasswordStrengthUI(pass.value, meter);

  form.onsubmit = async (e) => {
    e.preventDefault();
    VLHelpers.setButtonLoading(document.getElementById('register-submit'), true, 'Creating...');
    const res = await VLAPI.registerUser({});
    if (res.success) {
      VLUtils.showToast({ type: 'success', title: 'Account Created' });
      setTimeout(() => window.location.href = 'login.html', 1500);
    } else {
      VLHelpers.setButtonLoading(document.getElementById('register-submit'), false, 'Create Account');
    }
  };
}

/* =======================================================
DASHBOARD & NOTIFICATIONS
======================================================= */
const VLDashboard = {
  async initDashboard() {
    VLAuth.requireAuth();
    this.populateUserInfo();
    const dateEl = document.getElementById('welcome-date');
    if (dateEl) dateEl.textContent = VLUtils.getFormattedDate();
    await this.loadDashboardData();
    await this.loadNotifications();
    this.initSidebar();
    this.initUploadZone();
    this.initAccordions();
    this.initAnalyticsPlaceholder();
  },

  populateUserInfo() {
    const user = VLAuth.getCurrentUser() || { full_name: 'User', email: '' };
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.full_name);
    document.querySelectorAll('[data-user-initial]').forEach(el => el.textContent = user.full_name.charAt(0));
  },

  async loadDashboardData() {
    const res = await VLAPI.fetchDashboard();
    if (!res.success) return;
    const { stats, recent_activity, recent_documents } = res.data;
    
    const statMap = { 'stat-documents-verified': stats.documents_verified, 'stat-pending': stats.pending_verifications, 'stat-alerts': stats.fraud_alerts, 'stat-uploads': stats.recent_uploads };
    Object.entries(statMap).forEach(([id, val]) => VLUtils.animateCounter(document.getElementById(id), val));

    const activityList = document.getElementById('activity-list');
    if (activityList) {
      activityList.innerHTML = recent_activity.map(item => `
        <div class="activity-item">
          <div class="activity-item__icon">${VLHelpers.uploadSvg()}</div>
          <div class="activity-item__content">
            <div class="activity-item__title">${item.title}</div>
            <div class="activity-item__description">${item.description}</div>
          </div>
        </div>`).join('');
      activityList.classList.remove('hidden');
    }

    const tbody = document.getElementById('documents-tbody');
    if (tbody) {
      tbody.innerHTML = recent_documents.map(doc => `
        <tr>
          <td>${doc.name}</td>
          <td>${doc.category}</td>
          <td><span class="badge badge--success">${doc.status}</span></td>
          <td>${VLUtils.formatDate(doc.date)}</td>
          <td><button class="btn btn--sm" data-delete="${doc.id}">Delete</button></td>
        </tr>`).join('');
    }
    document.querySelectorAll('[data-skeleton]').forEach(el => el.remove());
  },

  async loadNotifications() {
    const res = await VLAPI.fetchNotifications();
    if (!res.success) return;
    const badge = document.getElementById('notification-badge');
    if (badge) badge.textContent = res.data.unread_count;
    const list = document.getElementById('notification-list');
    if (list) list.innerHTML = res.data.notifications.map(n => `<div class="notification-item"><b>${n.title}</b><p>${n.text}</p></div>`).join('');
  },

  initSidebar() {
    const sidebar = document.getElementById('sidebar'), overlay = document.getElementById('sidebar-overlay'), ham = document.getElementById('header-hamburger');
    if (!sidebar) return;
    const toggle = () => { sidebar.classList.toggle('mobile-open'); overlay.classList.toggle('active'); };
    if (ham) ham.onclick = toggle;
    if (overlay) overlay.onclick = toggle;
  },

  initUploadZone() {
    const zone = document.getElementById('upload-zone'), input = document.getElementById('file-input');
    if (!zone || !input) return;
    zone.onclick = () => input.click();
    zone.ondragover = (e) => { e.preventDefault(); zone.classList.add('drag-over'); };
    zone.ondragleave = () => zone.classList.remove('drag-over');
    zone.ondrop = async (e) => {
      e.preventDefault();
      const files = e.dataTransfer.files;
      for (let f of files) {
        if (ALLOWED_TYPES.includes(f.type)) {
          const res = await VLAPI.uploadDocument(new FormData(), (p) => console.log(p));
          if (res.success) VLUtils.showToast({ type: 'success', title: 'File Uploaded', message: f.name });
        }
      }
    };
  },

  initAccordions() {
    document.querySelectorAll('.accordion-header').forEach(h => {
      h.onclick = () => h.closest('.accordion-item').classList.toggle('open');
    });
  },

  initAnalyticsPlaceholder() {
    const chart = document.getElementById('analytics-chart');
    if (chart) chart.innerHTML = [40, 65, 55, 80, 70, 90, 75].map(v => `<div class="analytics-bar" style="height:${v}%"></div>`).join('');
  }
};
window.VLDashboard = VLDashboard;

/* =======================================================
THEME & MODALS
======================================================= */
const VLApp = {
  initTheme() {
    const theme = VLUtils.storageGet('vl_theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
    this.updateThemeIcons(theme);
  },
  toggleTheme() {
    const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    VLUtils.storageSet('vl_theme', next);
    this.updateThemeIcons(next);
  },
  updateThemeIcons(theme) {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.innerHTML = theme === 'dark' ? 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>` : 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
    });
  },
  initModals() {
    document.querySelectorAll('[data-modal-open]').forEach(btn => btn.onclick = () => {
      const m = document.getElementById(btn.dataset.modalOpen);
      if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; }
    });
    document.querySelectorAll('[data-modal-close], .modal-backdrop').forEach(el => el.onclick = (e) => {
      if (e.target === el || el.hasAttribute('data-modal-close')) {
        const m = el.closest('.modal-backdrop');
        if (m) { m.classList.remove('open'); document.body.style.overflow = ''; }
      }
    });
  }
};

/* =======================================================
EVENT LISTENERS & INITIALIZATION
======================================================= */
async function initializeApp() {
  VLApp.initTheme();
  VLApp.initModals();
  VLUtils.initScrollAnimations();
  VLUtils.initCounters();

  document.querySelectorAll('[data-theme-toggle]').forEach(b => b.onclick = () => VLApp.toggleTheme());
  document.querySelectorAll('[data-action="logout"]').forEach(b => b.onclick = () => VLAuth.logoutUser());

  const path = window.location.pathname, page = path.split('/').pop() || 'index.html';
  
  if (page === 'login.html') {
    VLAuth.redirectIfAuthenticated();
    initLoginForm();
  } else if (page === 'register.html') {
    VLAuth.redirectIfAuthenticated();
    initRegisterForm();
  } else if (page === 'dashboard.html') {
    await VLDashboard.initDashboard();
  } else if (page === 'index.html') {
    VLDashboard.initAccordions();
  }
}

document.addEventListener('DOMContentLoaded', initializeApp);