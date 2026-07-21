/**
 * VeriLaw — Dashboard Module
 * Dashboard interactions, stat cards, recent activity, notifications,
 * sidebar toggle, analytics placeholder, and file upload UI.
 * Depends on: utils.js, api.js, auth.js
 */

'use strict';

/* ── Dashboard Initializer ─────────────────────────────────────────────── */

async function initDashboard() {
  // Require authentication
  if (window.VLAuth) window.VLAuth.requireAuth();

  // Populate user info immediately from session
  populateUserInfo();

  // Set today's date on welcome card
  const dateEl = document.getElementById('welcome-date');
  if (dateEl) dateEl.textContent = window.VLUtils.getFormattedDate();

  // Load dashboard data
  await loadDashboardData();

  // Init sidebar
  initSidebar();

  // Init logout
  if (window.VLAuth) window.VLAuth.initLogout();

  // Init notifications
  await loadNotifications();

  // Init upload zone (if present on page)
  initUploadZone();

  // Init accordion on any page
  initAccordions();
}

/* ── User Info ─────────────────────────────────────────────────────────── */

function populateUserInfo() {
  const user = window.VLAuth ? window.VLAuth.getCurrentUser() : null;
  const name = user ? user.full_name : 'Demo User';
  const initial = name.charAt(0).toUpperCase();

  document.querySelectorAll('[data-user-name]').forEach(el => {
    el.textContent = name;
  });

  document.querySelectorAll('[data-user-initial]').forEach(el => {
    el.textContent = initial;
  });

  document.querySelectorAll('[data-user-email]').forEach(el => {
    if (user) el.textContent = user.email;
  });
}

/* ── Dashboard Data ────────────────────────────────────────────────────── */

async function loadDashboardData() {
  showDashboardSkeletons(true);

  try {
    const result = await window.VLAPI.fetchDashboard();

    if (result.success) {
      renderStats(result.data.stats);
      renderRecentActivity(result.data.recent_activity);
      renderRecentDocuments(result.data.recent_documents);
    } else {
      window.VLUtils.showToast({
        type: 'error',
        title: 'Load Error',
        message: 'Could not load dashboard data.',
      });
    }
  } catch {
    window.VLUtils.showToast({
      type: 'error',
      title: 'Error',
      message: 'Failed to load dashboard. Please refresh.',
    });
  } finally {
    showDashboardSkeletons(false);
  }
}

function showDashboardSkeletons(show) {
  const skeletons = document.querySelectorAll('[data-skeleton]');
  const contents  = document.querySelectorAll('[data-content]');
  skeletons.forEach(el => el.classList.toggle('hidden', !show));
  contents.forEach(el => el.classList.toggle('hidden', show));
}

/* ── Stat Cards ────────────────────────────────────────────────────────── */

function renderStats(stats) {
  if (!stats) return;

  const map = {
    'stat-documents-verified': stats.documents_verified,
    'stat-pending':            stats.pending_verifications,
    'stat-alerts':             stats.fraud_alerts,
    'stat-uploads':            stats.recent_uploads,
  };

  Object.entries(map).forEach(([id, value]) => {
    const el = document.getElementById(id);
    if (el) window.VLUtils.animateCounter(el, value, 1200);
  });
}

/* ── Recent Activity Feed ──────────────────────────────────────────────── */

function renderRecentActivity(activities) {
  const list = document.getElementById('activity-list');
  if (!list || !activities) return;

  list.innerHTML = '';

  if (activities.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <p class="text-secondary text-sm">No recent activity.</p>
      </div>`;
    return;
  }

  const iconMap = {
    upload:   { icon: uploadSvg(),  cls: 'activity-item__icon--primary' },
    verified: { icon: checkSvg(),   cls: 'activity-item__icon--success' },
    alert:    { icon: alertSvg(),   cls: 'activity-item__icon--danger'  },
    default:  { icon: fileSvg(),    cls: 'activity-item__icon--primary' },
  };

  activities.forEach(item => {
    const { icon, cls } = iconMap[item.type] || iconMap.default;
    const li = document.createElement('div');
    li.className = 'activity-item fade-in';
    li.innerHTML = `
      <div class="activity-item__icon ${cls}" aria-hidden="true">${icon}</div>
      <div class="activity-item__content">
        <div class="activity-item__title">${window.VLUtils.escapeHtml(item.title)}</div>
        <div class="activity-item__description">${window.VLUtils.escapeHtml(item.description)}</div>
      </div>
      <div class="activity-item__time">${window.VLUtils.timeAgo(item.time)}</div>
    `;
    list.appendChild(li);
  });
}

/* ── Recent Documents ──────────────────────────────────────────────────── */

function renderRecentDocuments(documents) {
  const tbody = document.getElementById('documents-tbody');
  if (!tbody || !documents) return;

  tbody.innerHTML = '';

  if (documents.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="text-center text-secondary" style="padding: var(--space-lg);">
          No documents yet. Upload your first document.
        </td>
      </tr>`;
    return;
  }

  const statusBadge = {
    'Verified': 'badge--success',
    'Pending':  'badge--warning',
    'Alert':    'badge--danger',
  };

  documents.forEach(doc => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div class="flex items-center gap-sm">
          <div style="color:var(--color-primary)" aria-hidden="true">${fileSvg()}</div>
          <span class="font-medium">${window.VLUtils.escapeHtml(doc.name)}</span>
        </div>
      </td>
      <td><span class="badge badge--neutral">${window.VLUtils.escapeHtml(doc.category)}</span></td>
      <td><span class="badge ${statusBadge[doc.status] || 'badge--neutral'} badge--dot">${window.VLUtils.escapeHtml(doc.status)}</span></td>
      <td class="text-secondary">${window.VLUtils.formatDate(doc.date)}</td>
      <td>
        <div class="flex items-center gap-xs">
          <button class="btn btn--sm btn--outline" aria-label="Download ${window.VLUtils.escapeHtml(doc.name)}">Download</button>
          <button class="btn btn--sm btn--danger-outline" data-delete-id="${doc.id}" aria-label="Delete ${window.VLUtils.escapeHtml(doc.name)}">Delete</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Bind delete buttons
  tbody.addEventListener('click', async (e) => {
    const deleteBtn = e.target.closest('[data-delete-id]');
    if (!deleteBtn) return;

    const id = deleteBtn.dataset.deleteId;
    if (!confirm('Are you sure you want to delete this document?')) return;

    const result = await window.VLAPI.deleteDocument(id);
    if (result.success) {
      deleteBtn.closest('tr').remove();
      window.VLUtils.showToast({ type: 'success', title: 'Deleted', message: 'Document removed.' });
    } else {
      window.VLUtils.showToast({ type: 'error', title: 'Error', message: result.message });
    }
  });
}

/* ── Notifications ─────────────────────────────────────────────────────── */

async function loadNotifications() {
  try {
    const result = await window.VLAPI.fetchNotifications();
    if (!result.success) return;

    const { unread_count, notifications } = result.data;

    // Update badge
    const badge = document.getElementById('notification-badge');
    if (badge) {
      badge.textContent = unread_count;
      badge.classList.toggle('hidden', unread_count === 0);
    }

    // Render list
    const list = document.getElementById('notification-list');
    if (!list) return;

    list.innerHTML = '';

    notifications.forEach(n => {
      const item = document.createElement('div');
      item.className = `notification-item${n.read ? '' : ' notification-item--unread'}`;
      item.innerHTML = `
        <div class="notification-item__content">
          <div class="notification-item__title">${window.VLUtils.escapeHtml(n.title)}</div>
          <div class="notification-item__text">${window.VLUtils.escapeHtml(n.text)}</div>
        </div>
        <div class="notification-item__time">${window.VLUtils.timeAgo(n.time)}</div>
      `;
      list.appendChild(item);
    });
  } catch {
    // Notifications are non-critical — fail silently
    console.warn('[VeriLaw Dashboard] Failed to load notifications.');
  }
}

/* ── Sidebar ───────────────────────────────────────────────────────────── */

function initSidebar() {
  const sidebar       = document.getElementById('sidebar');
  const overlay       = document.getElementById('sidebar-overlay');
  const mobileToggle  = document.getElementById('header-hamburger');
  const desktopToggle = document.getElementById('sidebar-toggle');

  if (!sidebar) return;

  // Highlight current page in sidebar nav
  highlightActiveSidebarItem();

  // Mobile open/close
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
      overlay && overlay.classList.toggle('active');
      mobileToggle.setAttribute('aria-expanded',
        sidebar.classList.contains('mobile-open').toString()
      );
    });
  }

  // Overlay click closes sidebar on mobile
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
      mobileToggle && mobileToggle.setAttribute('aria-expanded', 'false');
    });
  }

  // Desktop collapse toggle
  if (desktopToggle) {
    desktopToggle.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      const mainContent = document.querySelector('.main-content');
      if (mainContent) mainContent.classList.toggle('sidebar-collapsed');
      const isCollapsed = sidebar.classList.contains('collapsed');
      desktopToggle.setAttribute('aria-label', isCollapsed ? 'Expand sidebar' : 'Collapse sidebar');
      window.VLUtils.storageSet('vl_sidebar_collapsed', isCollapsed);
    });

    // Restore previous state
    if (window.VLUtils.storageGet('vl_sidebar_collapsed')) {
      sidebar.classList.add('collapsed');
      const mainContent = document.querySelector('.main-content');
      if (mainContent) mainContent.classList.add('sidebar-collapsed');
    }
  }
}

function highlightActiveSidebarItem() {
  const currentPage = window.location.pathname.split('/').pop() || 'dashboard.html';
  document.querySelectorAll('.sidebar__nav-item[href]').forEach(link => {
    const linkPage = link.getAttribute('href').split('/').pop();
    link.classList.toggle('active', linkPage === currentPage);
    if (linkPage === currentPage) {
      link.setAttribute('aria-current', 'page');
    }
  });
}

/* ── File Upload Zone ──────────────────────────────────────────────────── */

function initUploadZone() {
  const zone       = document.getElementById('upload-zone');
  const fileInput  = document.getElementById('file-input');
  const fileList   = document.getElementById('upload-file-list');
  const progressEl = document.getElementById('upload-progress');

  if (!zone || !fileInput) return;

  // Click to open file picker
  zone.addEventListener('click', () => fileInput.click());

  // Keyboard access
  zone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  // Drag events
  ['dragenter', 'dragover'].forEach(evt => {
    zone.addEventListener(evt, (e) => {
      e.preventDefault();
      zone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(evt => {
    zone.addEventListener(evt, () => zone.classList.remove('drag-over'));
  });

  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files, fileList, progressEl);
  });

  fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files, fileList, progressEl);
    fileInput.value = ''; // Reset so the same file can be re-selected
  });
}

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf', 'audio/mpeg', 'audio/wav'];
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB

function handleFiles(files, fileList, progressEl) {
  if (!files || files.length === 0) return;

  Array.from(files).forEach(file => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      window.VLUtils.showToast({
        type: 'error',
        title: 'Invalid File Type',
        message: `${file.name} is not supported. Allowed: JPG, PNG, PDF, MP3, WAV.`,
      });
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      window.VLUtils.showToast({
        type: 'error',
        title: 'File Too Large',
        message: `${file.name} exceeds the 20 MB limit.`,
      });
      return;
    }

    uploadSingleFile(file, fileList, progressEl);
  });
}

async function uploadSingleFile(file, fileList, progressEl) {
  // Add file item to list
  const itemId = `file-item-${Date.now()}`;
  if (fileList) {
    const item = document.createElement('div');
    item.className = 'upload-file-item fade-in';
    item.id = itemId;
    item.innerHTML = `
      <span class="upload-file-item__name">${window.VLUtils.escapeHtml(file.name)}</span>
      <span class="upload-file-item__size">${window.VLUtils.formatFileSize(file.size)}</span>
      <div class="progress" style="width:80px">
        <div class="progress__fill" id="prog-${itemId}" style="width:0%"></div>
      </div>
      <button class="upload-file-item__remove" aria-label="Remove ${window.VLUtils.escapeHtml(file.name)}" data-remove="${itemId}">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    `;
    fileList.appendChild(item);

    item.querySelector('[data-remove]').addEventListener('click', () => item.remove());
  }

  const formData = new FormData();
  formData.append('file', file);

  const result = await window.VLAPI.uploadDocument(formData, (pct) => {
    const bar = document.getElementById(`prog-${itemId}`);
    if (bar) bar.style.width = `${pct}%`;
  });

  if (result.success) {
    window.VLUtils.showToast({ type: 'success', title: 'Uploaded', message: `${file.name} uploaded.` });
  } else {
    window.VLUtils.showToast({ type: 'error', title: 'Upload Failed', message: result.message });
    const failedItem = document.getElementById(itemId);
    if (failedItem) failedItem.style.borderColor = 'var(--color-danger)';
  }
}

/* ── Analytics Placeholder ─────────────────────────────────────────────── */

function initAnalyticsPlaceholder() {
  const chart = document.getElementById('analytics-chart');
  if (!chart) return;

  // Sample data for last 7 days
  const data = [40, 65, 55, 80, 70, 90, 75];
  const max  = Math.max(...data);

  chart.innerHTML = '';
  data.forEach((val, i) => {
    const bar = document.createElement('div');
    bar.className = `analytics-bar${i === data.length - 1 ? ' analytics-bar--active' : ''}`;
    bar.style.height = `${(val / max) * 100}%`;
    bar.setAttribute('title', `Day ${i + 1}: ${val} verifications`);
    bar.setAttribute('role', 'img');
    bar.setAttribute('aria-label', `Day ${i + 1}: ${val} verifications`);
    chart.appendChild(bar);
  });
}

/* ── Accordion ─────────────────────────────────────────────────────────── */

function initAccordions() {
  document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.accordion-item');
      if (!item) return;
      const isOpen = item.classList.contains('open');
      // Close all siblings
      item.closest('.accordion')?.querySelectorAll('.accordion-item').forEach(i => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
      header.setAttribute('aria-expanded', (!isOpen).toString());
    });
  });
}

/* ── Inline SVG Helpers ────────────────────────────────────────────────── */

function uploadSvg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`;
}

function checkSvg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>`;
}

function alertSvg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>`;
}

function fileSvg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`;
}

/* ── Exports ───────────────────────────────────────────────────────────── */
window.VLDashboard = {
  initDashboard,
  loadDashboardData,
  loadNotifications,
  initSidebar,
  initUploadZone,
  initAnalyticsPlaceholder,
  initAccordions,
};
