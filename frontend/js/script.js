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
      const data = await response.json().catch(() => null);
      if (!response.ok) {
        return { success: false, message: data?.message || `Error ${response.status}`, data: data?.details || null };
      }
      return data;
    } catch (err) {
      clearTimeout(timeout);
      return { success: false, message: err.name === 'AbortError' ? 'Timeout' : 'Network Error', data: null };
    }
  },

  // Auth
  async loginUser(credentials) {
    return await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
  },
  async registerUser(userData) {
    return await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  },
  async logoutUser() {
    return await this.request('/auth/logout', {
      method: 'POST'
    });
  },

  // Dashboard & Data
  async fetchDashboard() {
    return await this.request('/reports/summary', {
      method: 'GET'
    });
  },
  async fetchNotifications() {
    return await this.request('/notifications', {
      method: 'GET'
    });
  },
  async uploadDocument(formData, onProgress) {
    // onProgress is not supported by native fetch easily, but we can call the endpoint
    return await this.request('/evidence/upload', {
      method: 'POST',
      body: formData,
      isFormData: true
    });
  },
  async deleteDocument(id) { 
    return await this.request(`/evidence/${id}`, {
      method: 'DELETE'
    });
  }
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
      VLUtils.showToast({ type: 'error', title: res.message || 'Login Failed' });
    }
  };
}

function initRegisterForm() {
  const form = document.getElementById('register-form');
  if (!form) return;
  const name = document.getElementById('reg-name');
  const email = document.getElementById('reg-email');
  const phone = document.getElementById('reg-phone');
  const pass = document.getElementById('reg-password');
  const confirmPass = document.getElementById('reg-confirm-password');
  const meter = document.getElementById('password-strength');

  pass.oninput = () => VLValidation.updatePasswordStrengthUI(pass.value, meter);

  form.onsubmit = async (e) => {
    e.preventDefault();
    if (pass.value !== confirmPass.value) {
      VLUtils.showToast({ type: 'error', title: 'Passwords do not match' });
      return;
    }
    VLHelpers.setButtonLoading(document.getElementById('register-submit'), true, 'Creating...');
    const res = await VLAPI.registerUser({
      full_name: name.value,
      email: email.value,
      mobile: phone.value,
      password: pass.value
    });
    if (res.success) {
      VLUtils.showToast({ type: 'success', title: 'Account Created' });
      setTimeout(() => window.location.href = 'login.html', 1500);
    } else {
      VLHelpers.setButtonLoading(document.getElementById('register-submit'), false, 'Create Account');
      VLUtils.showToast({ type: 'error', title: res.message || 'Registration failed' });
    }
  };
}

/* =======================================================
DASHBOARD, SIDEBAR & NOTIFICATIONS
======================================================= */
const VLDashboard = {
  populateUserInfo() {
    const user = VLAuth.getCurrentUser() || { full_name: 'Demo Practitioner', email: 'practitioner@verilaw.ai' };
    document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.full_name);
    document.querySelectorAll('[data-user-initial]').forEach(el => el.textContent = user.full_name.charAt(0));
    document.querySelectorAll('[data-user-email]').forEach(el => el.textContent = user.email);
  },

  async loadNotifications() {
    const res = await VLAPI.fetchNotifications();
    if (!res.success) return;
    const badge = document.getElementById('notification-badge');
    if (badge) {
      badge.textContent = res.data.unread_count;
      badge.style.display = res.data.unread_count > 0 ? 'flex' : 'none';
    }
    const list = document.getElementById('notification-list');
    if (list) {
      if (res.data.notifications.length === 0) {
        list.innerHTML = '<div class="text-secondary text-sm" style="text-align:center;padding:var(--space-md)">No active alerts.</div>';
      } else {
        list.innerHTML = res.data.notifications.map(n => `
          <div class="notification-item" style="padding:10px;border-bottom:1px solid rgba(255,255,255,0.05)">
            <b style="font-size:12px;color:#c084fc;display:block;margin-bottom:2px;">${n.title}</b>
            <p style="font-size:11.5px;margin:0;color:rgba(255,255,255,0.7)">${n.text}</p>
          </div>
        `).join('');
      }
    }
  },

  initSidebar() {
    const sidebar = document.getElementById('premium-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const ham = document.getElementById('btn-sidebar-toggle');
    const collapseBtn = document.getElementById('sidebar-collapse-btn');

    if (ham && sidebar && overlay) {
      ham.onclick = () => {
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
      };
      overlay.onclick = () => {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
      };
    }

    if (collapseBtn && sidebar) {
      // Load preference
      const isCollapsed = localStorage.getItem('vl_sidebar_collapsed') === 'true';
      if (isCollapsed) {
        sidebar.classList.add('collapsed');
      }

      collapseBtn.onclick = () => {
        sidebar.classList.toggle('collapsed');
        localStorage.setItem('vl_sidebar_collapsed', sidebar.classList.contains('collapsed'));
        // Dispatch resize event to trigger redraws of any dynamic content
        window.dispatchEvent(new Event('resize'));
      };
    }
  },

  initAccordions() {
    document.querySelectorAll('.accordion-header').forEach(h => {
      h.onclick = () => h.closest('.accordion-item').classList.toggle('open');
    });
  }
};
window.VLDashboard = VLDashboard;

/* =======================================================
THEME & MODALS
======================================================= */
const VLApp = {
  initTheme() {
    const theme = VLUtils.storageGet('vl_theme') || 'dark';
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
        `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>` : 
        `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
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
window.VLApp = VLApp;

/* =======================================================
CONVERSATIONAL CHAT ENGINE (VLChat)
======================================================= */
const VLChat = {
  activeThreadId: null,
  activeEvidenceId: null,
  threads: [],

  async initChat() {
    VLAuth.requireAuth();
    VLDashboard.populateUserInfo();
    VLDashboard.initSidebar();
    await VLDashboard.loadNotifications();
    
    this.initDOM();
    await this.loadThreads();
    this.initUpload();
  },

  initDOM() {
    // Right panel drawer toggle controls
    const toggleBtn = document.getElementById('toggle-detail-btn');
    const closeDrawerBtn = document.getElementById('btn-close-drawer-panel');
    const detailPanel = document.getElementById('chat-detail-panel');
    
    if (toggleBtn && detailPanel) {
      toggleBtn.onclick = () => {
        detailPanel.classList.toggle('closed');
      };
    }
    if (closeDrawerBtn && detailPanel) {
      closeDrawerBtn.onclick = () => {
        detailPanel.classList.add('closed');
      };
    }

    // New thread button
    const newChatBtn = document.getElementById('new-chat-btn');
    if (newChatBtn) {
      newChatBtn.onclick = async () => {
        const title = prompt("Enter a title for this new legal session/thread:", "Property Verification Workspace");
        if (title) {
          const res = await VLAPI.request('/complaints', {
            method: 'POST',
            body: JSON.stringify({
              title: title,
              description: "Custom session thread for AI verification & legal assistance.",
              category_id: 1,
              state: "National",
              district: "AI Workspace"
            })
          });
          if (res.success) {
            VLUtils.showToast({ type: 'success', title: 'Thread Created', message: title });
            await this.loadThreads(res.data.complaint_id);
          } else {
            VLUtils.showToast({ type: 'error', title: 'Error', message: res.message });
          }
        }
      };
    }

    // Chat form input submission
    const form = document.getElementById('chat-input-form');
    const textarea = document.getElementById('chat-textarea');
    if (form && textarea) {
      textarea.onkeydown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          form.requestSubmit();
        }
      };

      form.onsubmit = async (e) => {
        e.preventDefault();
        const text = textarea.value.trim();
        if (!text) return;
        
        textarea.value = '';
        textarea.style.height = 'auto';
        
        await this.sendMessage(text);
      };

      // Auto expand textarea
      textarea.oninput = () => {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
      };
    }

    // Connect all suggested prompt actions
    document.querySelectorAll('[data-prompt]').forEach(btn => {
      btn.onclick = (e) => {
        e.preventDefault();
        if (textarea) {
          textarea.value = btn.dataset.prompt;
          textarea.style.height = 'auto';
          textarea.style.height = (textarea.scrollHeight) + 'px';
          textarea.focus();
        }
      };
    });

    // Navigation button binds & workspace view switching
    const navItems = {
      'nav-chat-assistant': () => this.switchWorkspace('ai-assistant', 'General Legal Assistant'),
      'nav-my-documents': () => this.switchWorkspace('my-documents', 'My Documents'),
      'nav-fraud-alerts': () => this.switchWorkspace('fraud-alerts', 'Fraud Alerts & Document Audits'),
      'nav-complaint-history': () => this.switchWorkspace('complaint-history', 'Complaint History'),
      'nav-legal-search': () => this.switchWorkspace('legal-search', 'Legal & Reference Search'),
      'nav-settings': () => this.switchWorkspace('settings', 'Account & Settings')
    };

    Object.entries(navItems).forEach(([id, handler]) => {
      const el = document.getElementById(id);
      if (el) {
        el.onclick = (e) => {
          e.preventDefault();
          document.querySelectorAll('.sidebar-nav-menu .nav-item').forEach(item => item.classList.remove('active'));
          el.classList.add('active');
          handler();
        };
      }
    });

    // Toolbar shortcuts
    const uploadShortcut = document.getElementById('upload-doc-shortcut');
    const chatFileInput = document.getElementById('chat-file-input');
    if (uploadShortcut && chatFileInput) {
      uploadShortcut.onclick = () => chatFileInput.click();
    }

    // Voice / mic alert
    const micBtn = document.getElementById('chat-mic-btn');
    if (micBtn) {
      micBtn.onclick = () => {
        VLUtils.showToast({ type: 'info', title: 'Voice Input Enabled', message: 'Speak clearly. Dictating legal notes...' });
        if (textarea) {
          textarea.value = "Verify this rental contract notary stamp under Delhi Stamp Slabs.";
          textarea.focus();
        }
      };
    }

    // Right drawer auditing action binds
    const reverifyBtn = document.getElementById('btn-reverify');
    if (reverifyBtn) {
      reverifyBtn.onclick = () => {
        if (this.activeEvidenceId) {
          this.triggerDocumentVerification(this.activeEvidenceId);
        } else {
          VLUtils.showToast({ type: 'warning', title: 'No document active', message: 'Select or upload an evidence file first.' });
        }
      };
    }

    const flagFraudBtn = document.getElementById('btn-flag-fraud');
    if (flagFraudBtn) {
      flagFraudBtn.onclick = async () => {
        if (this.activeEvidenceId) {
          const res = await VLAPI.request(`/evidence/${this.activeEvidenceId}`, {
            method: 'PUT',
            body: JSON.stringify({ category: "FLAGGED FRAUD" })
          });
          VLUtils.showToast({ type: 'error', title: 'Document Flagged', message: 'This file has been reported as fraudulent.' });
        }
      };
    }
  },

  async loadThreads(selectThreadId = null) {
    const res = await VLAPI.request('/ai/chat/threads');
    if (!res.success) return;
    this.threads = res.data.threads;
    
    // Distribute threads into Today, Yesterday, and Previous Week
    const todayList = document.getElementById('threads-today');
    const yesterdayList = document.getElementById('threads-yesterday');
    const prevweekList = document.getElementById('threads-prevweek');

    if (!todayList || !yesterdayList || !prevweekList) return;

    todayList.innerHTML = '';
    yesterdayList.innerHTML = '';
    prevweekList.innerHTML = '';

    const now = new Date();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const startOfYesterday = new Date(startOfToday.getTime() - (24 * 60 * 60 * 1000));

    let activeSet = false;

    this.threads.forEach(t => {
      // Set activeThreadId to either the selected thread or the first thread in the list
      const isActive = selectThreadId ? (t.id === selectThreadId) : (this.activeThreadId ? t.id === this.activeThreadId : !activeSet);
      if (isActive) {
        this.activeThreadId = t.id;
        activeSet = true;
      }

      const itemHtml = `
        <div class="thread-item ${isActive ? 'active' : ''}" data-id="${t.id}">
          <svg class="thread-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          <span class="thread-title">${t.title}</span>
          <button class="delete-thread-btn" data-delete-id="${t.id}" title="Clear/Delete Thread">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
      `;

      const threadDate = new Date(t.updated_at);

      if (threadDate >= startOfToday) {
        todayList.insertAdjacentHTML('beforeend', itemHtml);
      } else if (threadDate >= startOfYesterday) {
        yesterdayList.insertAdjacentHTML('beforeend', itemHtml);
      } else {
        prevweekList.insertAdjacentHTML('beforeend', itemHtml);
      }
    });

    // Handle empty sections gracefully
    if (!todayList.innerHTML) todayList.innerHTML = '<div style="font-size:11px;color:rgba(255,255,255,0.2);padding:4px 10px;">No threads today</div>';
    if (!yesterdayList.innerHTML) yesterdayList.innerHTML = '<div style="font-size:11px;color:rgba(255,255,255,0.2);padding:4px 10px;">No threads yesterday</div>';
    if (!prevweekList.innerHTML) prevweekList.innerHTML = '<div style="font-size:11px;color:rgba(255,255,255,0.2);padding:4px 10px;">No older threads</div>';

    // Bind click handlers to threads
    document.querySelectorAll('.thread-item').forEach(el => {
      el.onclick = (e) => {
        if (e.target.closest('.delete-thread-btn')) {
          const id = parseInt(e.target.closest('.delete-thread-btn').dataset.deleteId);
          this.deleteThread(id);
          return;
        }
        const id = parseInt(el.dataset.id);
        this.switchThread(id);
      };
    });

    const activeT = this.threads.find(t => t.id === this.activeThreadId);
    if (activeT) {
      document.getElementById('current-thread-title').textContent = activeT.title;
    }

    await this.loadChatHistory();
    await this.loadWorkspaceFiles();
  },

  async deleteThread(id) {
    if (confirm("Are you sure you want to clear/delete this conversation thread?")) {
      const res = await VLAPI.request(`/ai/chat/threads/${id}`, { method: 'DELETE' });
      if (res.success) {
        VLUtils.showToast({ type: 'success', title: 'Deleted', message: 'Thread cleared successfully.' });
        if (this.activeThreadId === id) {
          this.activeThreadId = null;
        }
        await this.loadThreads();
      }
    }
  },

  async switchThread(id) {
    this.activeThreadId = id;
    document.querySelectorAll('.thread-item').forEach(el => {
      el.classList.toggle('active', parseInt(el.dataset.id) === id);
    });
    const activeT = this.threads.find(t => t.id === id);
    if (activeT) {
      document.getElementById('current-thread-title').textContent = activeT.title;
    }
    await this.loadChatHistory();
    await this.loadWorkspaceFiles();
  },

  async loadChatHistory() {
    const stream = document.getElementById('chat-stream');
    const welcome = document.getElementById('chat-welcome-screen');
    if (!stream || !welcome) return;

    stream.innerHTML = '<div class="text-secondary text-sm" style="text-align:center;padding:var(--space-md)">Synchronizing chat history…</div>';

    const res = await VLAPI.request(`/ai/chat/history?complaint_id=${this.activeThreadId}`);
    if (!res.success) {
      stream.innerHTML = '';
      welcome.classList.remove('hidden');
      return;
    }

    // If there are no custom user/AI messages (length is 0 or 1 with system greeting), display the elegant welcome view
    if (res.data.messages.length <= 1) {
      stream.innerHTML = '';
      stream.classList.add('hidden');
      welcome.classList.remove('hidden');
    } else {
      welcome.classList.add('hidden');
      stream.classList.remove('hidden');
      stream.innerHTML = '';
      res.data.messages.forEach(msg => {
        // Skip default template system instructions if present
        if (msg.content && msg.content.includes("verify_system_instruction")) return;
        this.appendMessageBubble(msg.sender_id === VLAuth.getCurrentUser()?.user_id ? 'user' : 'ai', msg.content);
      });
      this.scrollToBottom();
    }
  },

  appendMessageBubble(role, content) {
    const stream = document.getElementById('chat-stream');
    const welcome = document.getElementById('chat-welcome-screen');
    if (!stream) return;

    if (welcome) welcome.classList.add('hidden');
    stream.classList.remove('hidden');

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message chat-message--${role}`;

    // Add avatar container
    const avatar = document.createElement('div');
    avatar.className = role === 'user' ? 'user-avatar-premium' : 'user-avatar-premium ai-avatar-styled';
    avatar.style.background = role === 'user' ? 'linear-gradient(135deg, #7c3aed 0%, #2563eb 100%)' : '#1e293b';
    avatar.innerHTML = role === 'user' ? (VLAuth.getCurrentUser()?.full_name?.charAt(0) || 'U') : '⚖';
    avatar.style.width = '32px';
    avatar.style.height = '32px';
    avatar.style.borderRadius = '50%';
    avatar.style.display = 'flex';
    avatar.style.alignItems = 'center';
    avatar.style.justifyContent = 'center';
    avatar.style.fontSize = '12px';
    avatar.style.fontWeight = '700';
    avatar.style.color = '#fff';
    avatar.style.flexShrink = '0';

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';
    bubble.innerHTML = this.parseMarkdown(content);

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(bubble);
    stream.appendChild(msgDiv);
  },

  parseMarkdown(text) {
    if (!text) return '';
    let html = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Headings
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold & Italics
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Lists
    html = html.replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>');
    html = html.replace(/^\s*\*\s+(.*$)/gim, '<li>$1</li>');

    // Blockquotes
    html = html.replace(/^\s*>\s+(.*$)/gim, '<blockquote style="border-left:3px solid #7c3aed;padding-left:10px;margin-bottom:10px;color:rgba(255,255,255,0.7)">$1</blockquote>');

    // Tables parsing
    const lines = html.split('\n');
    let inTable = false;
    let tableHtml = '';
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
        const cells = lines[i].split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
        if (!inTable) {
          inTable = true;
          tableHtml += '<div class="table-container" style="overflow-x:auto;margin:10px 0;"><table class="premium-table" style="width:100%;border-collapse:collapse;font-size:12.5px;"><thead><tr style="background:rgba(255,255,255,0.05);border-bottom:1.5px solid rgba(255,255,255,0.1);">';
          cells.forEach(c => tableHtml += `<th style="padding:8px 12px;text-align:left;font-weight:700;color:#c084fc;">${c}</th>`);
          tableHtml += '</tr></thead><tbody>';
        } else {
          if (cells.every(c => /^:-*:$/.test(c) || /^--*$/.test(c))) {
            continue;
          }
          tableHtml += '<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">';
          cells.forEach(c => tableHtml += `<td style="padding:8px 12px;color:rgba(255,255,255,0.85);">${c}</td>`);
          tableHtml += '</tr>';
        }
        lines[i] = '';
      } else {
        if (inTable) {
          inTable = false;
          tableHtml += '</tbody></table></div>';
          lines[i] = tableHtml + '\n' + lines[i];
          tableHtml = '';
        }
      }
    }
    html = lines.filter(l => l !== '').join('\n');

    // Paragraph splits
    return html.split('\n\n').map(p => {
      const trimmed = p.trim();
      if (trimmed.startsWith('<h') || trimmed.startsWith('<li') || trimmed.startsWith('<blockquote') || trimmed.startsWith('<div')) return p;
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');
  },

  scrollToBottom() {
    const stream = document.getElementById('chat-stream');
    if (stream) stream.scrollTop = stream.scrollHeight;
  },

  showTypingIndicator() {
    const stream = document.getElementById('chat-stream');
    if (!stream) return;

    const ind = document.createElement('div');
    ind.className = 'chat-message chat-message--ai typing-indicator-container';
    
    const avatar = document.createElement('div');
    avatar.className = 'user-avatar-premium ai-avatar-styled';
    avatar.style.background = '#1e293b';
    avatar.innerHTML = '⚖';
    avatar.style.width = '32px';
    avatar.style.height = '32px';
    avatar.style.borderRadius = '50%';
    avatar.style.display = 'flex';
    avatar.style.alignItems = 'center';
    avatar.style.justifyContent = 'center';
    avatar.style.fontSize = '12px';
    avatar.style.color = '#fff';
    avatar.style.flexShrink = '0';

    ind.innerHTML = `
      <div class="chat-bubble" style="display:flex;gap:4px;align-items:center;padding:12px 18px;">
        <div class="typing-dot" style="width:6px;height:6px;border-radius:50%;background:#a78bfa;animation:typeBounce 1.4s infinite ease-in-out;"></div>
        <div class="typing-dot" style="width:6px;height:6px;border-radius:50%;background:#a78bfa;animation:typeBounce 1.4s infinite ease-in-out 0.2s;"></div>
        <div class="typing-dot" style="width:6px;height:6px;border-radius:50%;background:#a78bfa;animation:typeBounce 1.4s infinite ease-in-out 0.4s;"></div>
      </div>
    `;
    ind.prepend(avatar);
    stream.appendChild(ind);
    this.scrollToBottom();

    // Style for typing bouncy dots
    if (!document.getElementById('typing-style-override')) {
      const s = document.createElement('style');
      s.id = 'typing-style-override';
      s.innerHTML = `
        @keyframes typeBounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          45% { transform: scale(1.2); opacity: 1; }
        }
      `;
      document.head.appendChild(s);
    }
  },

  removeTypingIndicator() {
    const ind = document.querySelector('.typing-indicator-container');
    if (ind) ind.remove();
  },

  async sendMessage(text) {
    this.appendMessageBubble('user', text);
    this.scrollToBottom();
    this.showTypingIndicator();

    const res = await VLAPI.request('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        message: text,
        complaint_id: this.activeThreadId
      })
    });

    this.removeTypingIndicator();
    if (res.success) {
      this.appendMessageBubble('ai', res.data.content);
    } else {
      this.appendMessageBubble('ai', `Sorry, I encountered an error: ${res.message}`);
    }
    this.scrollToBottom();
  },

  initUpload() {
    const trigger = document.getElementById('chat-upload-btn');
    const input = document.getElementById('chat-file-input');
    if (!trigger || !input) return;

    trigger.onclick = () => input.click();
    input.onchange = async () => {
      if (!input.files.length) return;
      const file = input.files[0];
      
      this.appendMessageBubble('user', `Uploaded document: **${file.name}** (${(file.size/1024).toFixed(1)} KB)`);
      this.scrollToBottom();
      
      // Render premium step-by-step visual workflow inside chat bubble
      const stream = document.getElementById('chat-stream');
      const stepsDiv = document.createElement('div');
      stepsDiv.className = 'chat-message chat-message--ai upload-pipeline-stream-block';
      
      const avatar = document.createElement('div');
      avatar.className = 'user-avatar-premium ai-avatar-styled';
      avatar.style.background = '#1e293b';
      avatar.innerHTML = '⚖';
      avatar.style.width = '32px';
      avatar.style.height = '32px';
      avatar.style.borderRadius = '50%';
      avatar.style.display = 'flex';
      avatar.style.alignItems = 'center';
      avatar.style.justifyContent = 'center';
      avatar.style.fontSize = '12px';
      avatar.style.color = '#fff';
      avatar.style.flexShrink = '0';

      stepsDiv.innerHTML = `
        <div class="chat-bubble" style="width:100%; max-width:360px;">
          <h4 style="font-size:13px;font-weight:700;margin-bottom:12px;color:#c084fc;">Evidence Audit Pipeline</h4>
          <div class="analysis-steps-stream">
            <div class="step-item active" id="p-step-0"><span class="step-bullet"></span>Receiving document...</div>
            <div class="step-item" id="p-step-1"><span class="step-bullet"></span>Extracting OCR...</div>
            <div class="step-item" id="p-step-2"><span class="step-bullet"></span>Running fraud detection...</div>
            <div class="step-item" id="p-step-3"><span class="step-bullet"></span>Searching legal database...</div>
            <div class="step-item" id="p-step-4"><span class="step-bullet"></span>Generating legal opinion...</div>
            <div class="step-item" id="p-step-5"><span class="step-bullet"></span>Done.</div>
          </div>
        </div>
      `;
      stepsDiv.prepend(avatar);
      stream.appendChild(stepsDiv);
      this.scrollToBottom();

      // Trigger multi-step visual sequence delays
      const updateStep = (id, state) => {
        const el = document.getElementById(`p-step-${id}`);
        if (!el) return;
        if (state === 'active') {
          el.classList.add('active');
        } else if (state === 'completed') {
          el.classList.remove('active');
          el.classList.add('completed');
        }
      };

      const runVisualPipeline = () => {
        return new Promise((resolve) => {
          setTimeout(() => { updateStep(0, 'completed'); updateStep(1, 'active'); }, 500);
          setTimeout(() => { updateStep(1, 'completed'); updateStep(2, 'active'); }, 1100);
          setTimeout(() => { updateStep(2, 'completed'); updateStep(3, 'active'); }, 1800);
          setTimeout(() => { updateStep(3, 'completed'); updateStep(4, 'active'); }, 2400);
          setTimeout(() => { updateStep(4, 'completed'); updateStep(5, 'active'); }, 3000);
          setTimeout(() => { updateStep(5, 'completed'); resolve(); }, 3500);
        });
      };

      const formData = new FormData();
      formData.append('file', file);
      formData.append('complaint_id', this.activeThreadId);

      // Fire actual API and steps concurrently
      const [apiResponse] = await Promise.all([
        fetch('/api/v1/ai/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${VLUtils.storageGet(SESSION_KEY)}`
          },
          body: formData
        }).then(r => r.json().catch(() => null)),
        runVisualPipeline()
      ]);

      // Remove pipeline placeholder
      stepsDiv.remove();

      if (apiResponse && apiResponse.success) {
        VLUtils.showToast({ type: 'success', title: 'File Extracted', message: file.name });
        await this.loadWorkspaceFiles();
        await this.selectDocument(apiResponse.data.evidence_id);
        
        // Auto-run verification response after upload
        await this.triggerDocumentVerification(apiResponse.data.evidence_id);
      } else {
        this.appendMessageBubble('ai', `Failed to upload and verify file: ${apiResponse?.message || 'Server error'}`);
        this.scrollToBottom();
      }
    };
  },

  async loadWorkspaceFiles() {
    const listEl = document.getElementById('workspace-files-list');
    if (!listEl) return;

    const res = await VLAPI.request(`/evidence/${this.activeThreadId}`);
    if (!res.success || !res.data || !res.data.length) {
      listEl.innerHTML = '<p class="empty-files-text" style="font-size:12px;color:rgba(255,255,255,0.3);text-align:center;padding:15px 0;">No files uploaded in this thread yet. Drag &amp; drop a file or click the attachment icon to upload.</p>';
      document.getElementById('document-analysis-section').classList.add('hidden');
      return;
    }

    listEl.innerHTML = res.data.map(f => {
      const isSelected = this.activeEvidenceId === f.evidence_id;
      return `
        <div class="workspace-file-item ${isSelected ? 'selected' : ''}" data-file-id="${f.evidence_id}">
          <div class="file-info-block">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            <div>
              <div class="file-info-name" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;">${f.original_name}</div>
              <div class="file-info-meta">${f.file_type} · ${(f.file_size/1024).toFixed(1)} KB</div>
            </div>
          </div>
          <button class="btn-logout-sidebar delete-file-btn" data-del-file-id="${f.evidence_id}" title="Delete file" style="padding:4px;color:rgba(255,255,255,0.3)">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
      `;
    }).join('');

    listEl.querySelectorAll('.workspace-file-item').forEach(el => {
      el.onclick = (e) => {
        if (e.target.closest('.delete-file-btn')) {
          const id = parseInt(e.target.closest('.delete-file-btn').dataset.delFileId);
          this.deleteFile(id);
          return;
        }
        const id = parseInt(el.dataset.fileId);
        this.selectDocument(id);
      };
    });
  },

  async deleteFile(id) {
    if (confirm("Are you sure you want to delete this document from the workspace?")) {
      const res = await VLAPI.request(`/evidence/${id}`, { method: 'DELETE' });
      if (res.success) {
        VLUtils.showToast({ type: 'success', title: 'Deleted', message: 'Document removed successfully.' });
        if (this.activeEvidenceId === id) this.activeEvidenceId = null;
        await this.loadWorkspaceFiles();
      }
    }
  },

  async selectDocument(id) {
    this.activeEvidenceId = id;
    document.querySelectorAll('.workspace-file-item').forEach(el => {
      el.classList.toggle('selected', parseInt(el.dataset.fileId) === id);
    });

    const res = await VLAPI.request(`/ai/document/${id}`);
    if (!res.success) return;

    const data = res.data;
    document.getElementById('analysis-doc-type').textContent = data.analysis.document_type;
    document.getElementById('analysis-status').textContent = data.analysis.status;
    
    const prob = data.analysis.fraud_probability;
    const probEl = document.getElementById('analysis-fraud-prob');
    probEl.textContent = `${prob}%`;
    
    const fillBar = document.getElementById('risk-bar-fill');
    fillBar.style.width = `${prob}%`;
    fillBar.className = 'risk-bar-fill';
    if (prob > 75) {
      fillBar.classList.add('risk-bar-fill--high');
      probEl.style.color = '#ef4444';
    } else if (prob > 35) {
      fillBar.classList.add('risk-bar-fill--med');
      probEl.style.color = '#f59e0b';
    } else {
      fillBar.classList.add('risk-bar-fill--low');
      probEl.style.color = '#10b981';
    }

    document.getElementById('analysis-confidence').textContent = data.analysis.confidence_score;
    document.getElementById('analysis-date').textContent = new Date(data.upload_time).toLocaleDateString(undefined, {month:'short', day:'numeric', year:'numeric'});
    document.getElementById('analysis-ocr-content').textContent = data.ocr_text;

    document.getElementById('document-analysis-section').classList.remove('hidden');
    
    const panel = document.getElementById('chat-detail-panel');
    if (panel) panel.classList.remove('closed');
  },

  async triggerDocumentVerification(id) {
    this.showTypingIndicator();
    this.appendMessageBubble('ai', "Initiating secure digital notary and signature authenticity audit. Searching Bharatiya Nyaya Sanhita (BNS) indices...");
    this.scrollToBottom();

    const res = await VLAPI.request('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        evidence_id: id,
        complaint_id: this.activeThreadId
      })
    });

    this.removeTypingIndicator();
    if (res.success) {
      this.appendMessageBubble('ai', res.data.content);
    } else {
      this.appendMessageBubble('ai', `Analysis failed: ${res.message}`);
    }
    this.scrollToBottom();
  },

  /* ──────────────────────────────────────────────────────────
     WORKSPACE SWITCHING & VIEW RENDERERS
  ────────────────────────────────────────────────────────── */
  activeWorkspaceMode: 'ai-assistant',

  switchWorkspace(mode, headingTitle) {
    this.activeWorkspaceMode = mode;
    
    // Update Header Title
    const titleEl = document.getElementById('current-thread-title');
    if (titleEl) titleEl.textContent = headingTitle || 'VeriLaw Workspace';

    // Hide chat stream & chat input footer if not in AI Assistant mode
    const chatStream = document.getElementById('chat-stream');
    const welcomeScreen = document.getElementById('chat-welcome-screen');
    const inputFooter = document.querySelector('.chat-input-sticky-footer');

    // Hide all workspace views
    document.querySelectorAll('.workspace-view-container').forEach(v => v.classList.add('hidden'));

    if (mode === 'ai-assistant') {
      if (chatStream) chatStream.classList.remove('hidden');
      if (inputFooter) inputFooter.classList.remove('hidden');
      if (welcomeScreen && chatStream && chatStream.children.length === 0) {
        welcomeScreen.classList.remove('hidden');
      }
    } else {
      if (chatStream) chatStream.classList.add('hidden');
      if (welcomeScreen) welcomeScreen.classList.add('hidden');
      if (inputFooter) inputFooter.classList.add('hidden');

      const viewEl = document.getElementById(`view-${mode}`);
      if (viewEl) {
        viewEl.classList.remove('hidden');
      }

      // Load specific workspace view data
      if (mode === 'my-documents') this.loadMyDocumentsWorkspace();
      else if (mode === 'fraud-alerts') this.loadFraudAlertsWorkspace();
      else if (mode === 'complaint-history') this.loadComplaintHistoryWorkspace();
      else if (mode === 'legal-search') this.loadLegalSearchWorkspace();
      else if (mode === 'settings') this.loadSettingsWorkspace();
    }
  },

  /* 1. My Documents Workspace */
  async loadMyDocumentsWorkspace() {
    const container = document.getElementById('documents-list-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-spinner">Loading generated documents...</div>';

    const res = await VLAPI.request('/documents');
    if (!res.success) {
      container.innerHTML = `<div class="error-workspace-state">Failed to load documents: ${VLUtils.escapeHtml(res.message)}</div>`;
      return;
    }

    const docs = res.data || [];
    if (docs.length === 0) {
      container.innerHTML = `
        <div class="empty-workspace-state">
          <h3>No Generated Documents</h3>
          <p>You have not generated any complaint documents yet. File a complaint or ask the AI Assistant to generate one.</p>
        </div>`;
      return;
    }

    container.innerHTML = docs.map(doc => `
      <div class="workspace-card" id="doc-card-${doc.document_id}">
        <div class="card-title-row">
          <h3>📄 Document #${doc.document_id} (${doc.document_type})</h3>
          <span class="badge badge--primary">${doc.document_type}</span>
        </div>
        <div class="card-meta-row">
          <span>Complaint ID: ${doc.complaint_id}</span>
          <span>Generated: ${doc.generated_at ? new Date(doc.generated_at).toLocaleString('en-IN') : 'N/A'}</span>
        </div>
        <div class="card-actions-row">
          <a href="/api/v1/documents/download/${doc.document_id}" target="_blank" class="btn btn--primary btn--sm" style="display:inline-flex;align-items:center;gap:4px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Download ${doc.document_type}
          </a>
          <button class="btn btn--danger btn--sm btn-delete-doc" data-doc-id="${doc.document_id}">Delete</button>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.btn-delete-doc').forEach(btn => {
      btn.onclick = async () => {
        const id = btn.dataset.docId;
        if (confirm(`Delete document #${id}?`)) {
          const delRes = await VLAPI.request(`/documents/${id}`, { method: 'DELETE' });
          if (delRes.success) {
            VLUtils.showToast({ type: 'success', title: 'Deleted', message: 'Document removed.' });
            this.loadMyDocumentsWorkspace();
          } else {
            VLUtils.showToast({ type: 'error', title: 'Error', message: delRes.message });
          }
        }
      };
    });
  },

  /* 2. Fraud Alerts Workspace */
  async loadFraudAlertsWorkspace() {
    const container = document.getElementById('fraud-alerts-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-spinner">Loading evidence and fraud audits...</div>';

    // Fetch complaints first to list evidence
    const complaintsRes = await VLAPI.request('/complaints');
    if (!complaintsRes.success) {
      container.innerHTML = `<div class="error-workspace-state">Failed to load complaints: ${VLUtils.escapeHtml(complaintsRes.message)}</div>`;
      return;
    }

    const complaints = complaintsRes.data?.data || complaintsRes.data || [];
    let allEvidence = [];

    for (const c of complaints) {
      const evRes = await VLAPI.request(`/evidence/${c.complaint_id}`);
      if (evRes.success && Array.isArray(evRes.data)) {
        allEvidence.push(...evRes.data);
      }
    }

    if (allEvidence.length === 0) {
      container.innerHTML = `
        <div class="empty-workspace-state">
          <h3>No Documents Uploaded for Fraud Auditing</h3>
          <p>Upload property deeds, agreements, or bills in the AI chat to trigger automated fraud audit reports.</p>
        </div>`;
      return;
    }

    container.innerHTML = allEvidence.map(ev => `
      <div class="workspace-card" id="fraud-card-${ev.evidence_id}">
        <div class="card-title-row">
          <h3>📑 ${VLUtils.escapeHtml(ev.original_name || ev.file_name)}</h3>
          <span class="badge ${ev.category === 'Property Dispute' ? 'badge--warning' : 'badge--info'}">${ev.category || 'General'}</span>
        </div>
        <div class="card-meta-row">
          <span>Type: ${ev.file_type || 'File'}</span>
          <span>Size: ${ev.file_size ? (ev.file_size / 1024).toFixed(1) + ' KB' : 'N/A'}</span>
          <span>Uploaded: ${ev.upload_time ? new Date(ev.upload_time).toLocaleDateString('en-IN') : 'N/A'}</span>
        </div>
        <div style="margin-bottom:12px;font-size:0.85rem;color:var(--color-text-secondary);background:rgba(0,0,0,0.2);padding:8px 12px;border-radius:8px;max-height:80px;overflow:hidden;">
          ${VLUtils.escapeHtml((ev.ocr_text || 'No extracted text.').substring(0, 200))}...
        </div>
        <div class="card-actions-row">
          <button class="btn btn--primary btn--sm btn-inspect-audit" data-ev-id="${ev.evidence_id}">Inspect Audit Report</button>
          <a href="/api/v1/evidence/download/${ev.evidence_id}" target="_blank" class="btn btn--outline btn--sm">Download Original</a>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.btn-inspect-audit').forEach(btn => {
      btn.onclick = () => {
        const id = parseInt(btn.dataset.evId);
        this.selectDocument(id);
      };
    });
  },

  /* 3. Complaint History Workspace */
  async loadComplaintHistoryWorkspace() {
    const container = document.getElementById('complaint-history-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-spinner">Loading complaint records...</div>';

    const res = await VLAPI.request('/complaints');
    if (!res.success) {
      container.innerHTML = `<div class="error-workspace-state">Failed to load complaints: ${VLUtils.escapeHtml(res.message)}</div>`;
      return;
    }

    const complaints = res.data?.data || res.data || [];
    if (complaints.length === 0) {
      container.innerHTML = `
        <div class="empty-workspace-state">
          <h3>No Complaints Filed</h3>
          <p>You have not filed any legal complaints yet. Use the AI Assistant to classify and file a complaint.</p>
        </div>`;
      return;
    }

    container.innerHTML = complaints.map(c => `
      <div class="workspace-card" id="complaint-card-${c.complaint_id}">
        <div class="card-title-row">
          <h3>⚖️ ${VLUtils.escapeHtml(c.title)}</h3>
          <span class="badge ${c.status === 'Completed' ? 'badge--success' : 'badge--warning'}">${c.status}</span>
        </div>
        <div class="card-meta-row">
          <span>Complaint ID: ${c.complaint_id}</span>
          <span>State: ${VLUtils.escapeHtml(c.state || 'N/A')}, ${VLUtils.escapeHtml(c.district || 'N/A')}</span>
          <span>Confidence: ${c.ai_confidence ? c.ai_confidence + '%' : 'N/A'}</span>
          <span>Filed: ${c.created_at ? new Date(c.created_at).toLocaleDateString('en-IN') : 'N/A'}</span>
        </div>
        <p style="font-size:0.9rem;margin-bottom:12px;color:var(--color-text-secondary);">${VLUtils.escapeHtml(c.description.substring(0, 250))}${c.description.length > 250 ? '...' : ''}</p>
        <div class="card-actions-row">
          <button class="btn btn--outline btn--sm btn-view-complaint-details" data-comp-id="${c.complaint_id}">View Details</button>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.btn-view-complaint-details').forEach(btn => {
      btn.onclick = async () => {
        const id = btn.dataset.compId;
        const compRes = await VLAPI.request(`/complaints/${id}`);
        if (compRes.success) {
          const detail = compRes.data;
          alert(`Complaint #${detail.complaint_id}\nTitle: ${detail.title}\nCategory: ${detail.category?.category_name || 'N/A'}\nDepartment: ${detail.department?.department_name || 'N/A'}\nStatus: ${detail.status}\nDescription:\n${detail.description}`);
        } else {
          VLUtils.showToast({ type: 'error', title: 'Error', message: compRes.message });
        }
      };
    });
  },

  /* 4. Legal Search Workspace */
  async loadLegalSearchWorkspace() {
    const container = document.getElementById('legal-search-container');
    const input = document.getElementById('legal-search-input');
    if (!container) return;
    container.innerHTML = '<div class="loading-spinner">Loading legal reference index...</div>';

    const [catRes, deptRes] = await Promise.all([
      VLAPI.request('/categories'),
      VLAPI.request('/departments')
    ]);

    const categories = catRes.success ? (catRes.data || []) : [];
    const departments = deptRes.success ? (deptRes.data || []) : [];

    const renderResults = (query = '') => {
      const q = query.toLowerCase().trim();
      const filteredCats = categories.filter(c => c.category_name.toLowerCase().includes(q) || (c.description && c.description.toLowerCase().includes(q)));
      const filteredDepts = departments.filter(d => d.department_name.toLowerCase().includes(q) || (d.description && d.description.toLowerCase().includes(q)));

      if (filteredCats.length === 0 && filteredDepts.length === 0) {
        container.innerHTML = `
          <div class="empty-workspace-state">
            <h3>No Results Found</h3>
            <p>No legal categories or government departments matched your query "${VLUtils.escapeHtml(query)}".</p>
          </div>`;
        return;
      }

      let html = '';
      if (filteredCats.length > 0) {
        html += `<h3 style="margin-bottom:12px;font-size:1.1rem;color:var(--color-primary);">Legal Complaint Categories (${filteredCats.length})</h3>`;
        html += filteredCats.map(c => `
          <div class="workspace-card" style="margin-bottom:12px;">
            <div class="card-title-row">
              <h3>Category: ${VLUtils.escapeHtml(c.category_name)}</h3>
            </div>
            <p style="font-size:0.9rem;color:var(--color-text-secondary);margin:0;">${VLUtils.escapeHtml(c.description || 'No description available.')}</p>
          </div>
        `).join('');
      }

      if (filteredDepts.length > 0) {
        html += `<h3 style="margin-top:20px;margin-bottom:12px;font-size:1.1rem;color:var(--color-primary);">Government Departments & Authorities (${filteredDepts.length})</h3>`;
        html += filteredDepts.map(d => `
          <div class="workspace-card" style="margin-bottom:12px;">
            <div class="card-title-row">
              <h3>${VLUtils.escapeHtml(d.department_name)}</h3>
              ${d.helpline ? `<span class="badge badge--success">📞 ${d.helpline}</span>` : ''}
            </div>
            <p style="font-size:0.9rem;color:var(--color-text-secondary);margin-bottom:8px;">${VLUtils.escapeHtml(d.description || 'Department reference.')}</p>
            <div class="card-meta-row">
              ${d.website ? `<span>Website: <a href="${d.website}" target="_blank" style="color:var(--color-primary);">${d.website}</a></span>` : ''}
              ${d.email ? `<span>Email: ${d.email}</span>` : ''}
            </div>
          </div>
        `).join('');
      }

      container.innerHTML = html;
    };

    renderResults('');

    if (input) {
      input.oninput = VLUtils.debounce(() => renderResults(input.value), 300);
    }
  },

  /* 5. Settings Workspace */
  async loadSettingsWorkspace() {
    const user = VLAuth.getCurrentUser() || {};
    const profileRes = await VLAPI.request('/profile');
    const profileData = profileRes.success ? profileRes.data : user;

    const nameInput = document.getElementById('settings-name');
    const mobileInput = document.getElementById('settings-mobile');
    const emailInput = document.getElementById('settings-email');

    if (nameInput) nameInput.value = profileData.full_name || '';
    if (mobileInput) mobileInput.value = profileData.mobile || '';
    if (emailInput) emailInput.value = profileData.email || '';

    // Bind profile form submit
    const profileForm = document.getElementById('settings-profile-form');
    if (profileForm) {
      profileForm.onsubmit = async (e) => {
        e.preventDefault();
        const btn = document.getElementById('save-profile-btn');
        VLHelpers.setButtonLoading(btn, true, 'Saving...');
        const res = await VLAPI.request('/profile', {
          method: 'PUT',
          body: JSON.stringify({
            full_name: nameInput.value,
            mobile: mobileInput.value
          })
        });
        VLHelpers.setButtonLoading(btn, false, 'Save Profile');
        if (res.success) {
          VLUtils.showToast({ type: 'success', title: 'Success', message: 'Profile updated.' });
          // Update local session
          const updatedUser = { ...profileData, full_name: nameInput.value, mobile: mobileInput.value };
          VLUtils.storageSet(USER_KEY, updatedUser);
          VLDashboard.populateUserInfo();
        } else {
          VLUtils.showToast({ type: 'error', title: 'Error', message: res.message });
        }
      };
    }

    // Bind password form submit
    const passForm = document.getElementById('settings-password-form');
    if (passForm) {
      passForm.onsubmit = async (e) => {
        e.preventDefault();
        const currPass = document.getElementById('settings-curr-pass').value;
        const newPass = document.getElementById('settings-new-pass').value;
        const btn = document.getElementById('change-pass-btn');

        VLHelpers.setButtonLoading(btn, true, 'Updating...');
        const res = await VLAPI.request('/profile/password', {
          method: 'PUT',
          body: JSON.stringify({
            current_password: currPass,
            new_password: newPass
          })
        });
        VLHelpers.setButtonLoading(btn, false, 'Update Password');
        if (res.success) {
          VLUtils.showToast({ type: 'success', title: 'Success', message: 'Password changed successfully.' });
          passForm.reset();
        } else {
          VLUtils.showToast({ type: 'error', title: 'Error', message: res.message });
        }
      };
    }
  }



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
    await VLChat.initChat();
  } else if (page === 'index.html') {
    VLDashboard.initAccordions();
  }
}

document.addEventListener('DOMContentLoaded', initializeApp);