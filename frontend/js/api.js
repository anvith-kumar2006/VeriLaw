/**
 * VeriLaw — API Module
 * Placeholder API methods — all functions are backend-ready stubs.
 * Replace the console.log calls with real fetch() calls when the Flask
 * backend is available. Response shape follows the agreed JSON contract:
 * { success: boolean, message: string, data: {} }
 */

'use strict';

/* ── API Base Configuration ────────────────────────────────────────────── */

const API_BASE    = '/api/v1';
const API_TIMEOUT = 10000; // 10 seconds

/**
 * Default request headers.
 * JWT token is appended automatically if present in localStorage.
 */
function getHeaders(isFormData = false) {
  const headers = {};
  if (!isFormData) headers['Content-Type'] = 'application/json';

  const token = window.VLUtils
    ? window.VLUtils.storageGet('vl_token')
    : localStorage.getItem('vl_token');

  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

/**
 * Core fetch wrapper with timeout and standard error handling.
 * @param {string} endpoint
 * @param {RequestInit} options
 * @returns {Promise<{ success: boolean, message: string, data: any }>}
 */
async function request(endpoint, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: { ...getHeaders(options.isFormData), ...options.headers },
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        success: false,
        message: errorData.message || `Request failed (${response.status})`,
        data: null,
      };
    }

    return await response.json();

  } catch (err) {
    clearTimeout(timeout);
    if (err.name === 'AbortError') {
      return { success: false, message: 'Request timed out. Please try again.', data: null };
    }
    return { success: false, message: 'Network error. Please check your connection.', data: null };
  }
}

/* ── Authentication API ────────────────────────────────────────────────── */

/**
 * Log in an existing user.
 * @param {{ email: string, password: string }} credentials
 * @returns {Promise}
 */
async function loginUser(credentials) {
  console.log('[VeriLaw API] loginUser called with:', { email: credentials.email });

  // Placeholder — simulate API call
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('[VeriLaw API] loginUser response (placeholder):', {
        success: true,
        message: 'Login successful.',
        data: {
          token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.placeholder',
          user: {
            id: 1,
            full_name: 'Demo User',
            email: credentials.email,
            role: 'citizen',
          },
        },
      });
      resolve({
        success: true,
        message: 'Login successful.',
        data: {
          token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.placeholder',
          user: {
            id: 1,
            full_name: 'Demo User',
            email: credentials.email,
            role: 'citizen',
          },
        },
      });
    }, 1000);
  });

  // Production implementation:
  // return request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) });
}

/**
 * Register a new user.
 * @param {{ full_name: string, email: string, mobile: string, password: string }} userData
 * @returns {Promise}
 */
async function registerUser(userData) {
  console.log('[VeriLaw API] registerUser called with:', { email: userData.email, name: userData.full_name });

  return new Promise(resolve => {
    setTimeout(() => {
      console.log('[VeriLaw API] registerUser response (placeholder):', {
        success: true,
        message: 'Registration successful. Please log in.',
        data: { userId: 42 },
      });
      resolve({
        success: true,
        message: 'Registration successful. Please log in.',
        data: { userId: 42 },
      });
    }, 1200);
  });

  // Production implementation:
  // return request('/auth/register', { method: 'POST', body: JSON.stringify(userData) });
}

/**
 * Log out the current user (clears token, calls backend).
 * @returns {Promise}
 */
async function logoutUser() {
  console.log('[VeriLaw API] logoutUser called');

  return new Promise(resolve => {
    setTimeout(() => {
      console.log('[VeriLaw API] logoutUser response (placeholder):', {
        success: true,
        message: 'Logged out successfully.',
        data: null,
      });
      resolve({ success: true, message: 'Logged out successfully.', data: null });
    }, 300);
  });

  // Production implementation:
  // return request('/auth/logout', { method: 'POST' });
}

/* ── Dashboard API ─────────────────────────────────────────────────────── */

/**
 * Fetch dashboard statistics and recent activity.
 * @returns {Promise}
 */
async function fetchDashboard() {
  console.log('[VeriLaw API] fetchDashboard called');

  return new Promise(resolve => {
    setTimeout(() => {
      const data = {
        stats: {
          documents_verified: 24,
          pending_verifications: 3,
          fraud_alerts: 1,
          recent_uploads: 7,
        },
        recent_activity: [
          { id: 1, type: 'upload',   title: 'Document Uploaded',      description: 'Aadhaar_Card.pdf uploaded successfully.',         time: new Date(Date.now() - 3600000).toISOString() },
          { id: 2, type: 'verified', title: 'Verification Complete',   description: 'Rental Agreement verified — no issues found.',    time: new Date(Date.now() - 7200000).toISOString() },
          { id: 3, type: 'alert',    title: 'Fraud Alert Raised',      description: 'Signature mismatch detected on Invoice_May.pdf.', time: new Date(Date.now() - 86400000).toISOString() },
          { id: 4, type: 'upload',   title: 'Document Uploaded',       description: 'Bank_Statement_Q1.pdf uploaded successfully.',    time: new Date(Date.now() - 172800000).toISOString() },
        ],
        recent_documents: [
          { id: 1, name: 'Rental Agreement',     category: 'Legal',    status: 'Verified',    date: new Date(Date.now() - 86400000).toISOString() },
          { id: 2, name: 'Aadhaar Card',          category: 'Identity', status: 'Verified',    date: new Date(Date.now() - 3600000).toISOString() },
          { id: 3, name: 'Invoice_May.pdf',       category: 'Finance',  status: 'Alert',       date: new Date(Date.now() - 172800000).toISOString() },
          { id: 4, name: 'Bank Statement Q1',     category: 'Finance',  status: 'Pending',     date: new Date(Date.now() - 7200000).toISOString() },
          { id: 5, name: 'Employment Letter',     category: 'Legal',    status: 'Verified',    date: new Date(Date.now() - 259200000).toISOString() },
        ],
      };
      console.log('[VeriLaw API] fetchDashboard response (placeholder):', { success: true, data });
      resolve({ success: true, message: '', data });
    }, 800);
  });

  // Production implementation:
  // return request('/dashboard');
}

/* ── Notifications API ─────────────────────────────────────────────────── */

/**
 * Fetch user notifications.
 * @returns {Promise}
 */
async function fetchNotifications() {
  console.log('[VeriLaw API] fetchNotifications called');

  return new Promise(resolve => {
    setTimeout(() => {
      const data = {
        unread_count: 2,
        notifications: [
          { id: 1, type: 'success', title: 'Verification Complete',  text: 'Your Rental Agreement has been verified.',      time: new Date(Date.now() - 1800000).toISOString(), read: false },
          { id: 2, type: 'warning', title: 'Pending Review',         text: 'Bank Statement Q1 is awaiting verification.',   time: new Date(Date.now() - 7200000).toISOString(), read: false },
          { id: 3, type: 'danger',  title: 'Fraud Alert',            text: 'Signature mismatch on Invoice_May.pdf.',        time: new Date(Date.now() - 86400000).toISOString(), read: true },
          { id: 4, type: 'info',    title: 'Welcome to VeriLaw',     text: 'Start by uploading your first document.',       time: new Date(Date.now() - 259200000).toISOString(), read: true },
        ],
      };
      console.log('[VeriLaw API] fetchNotifications response (placeholder):', { success: true, data });
      resolve({ success: true, message: '', data });
    }, 600);
  });

  // Production implementation:
  // return request('/notifications');
}

/* ── Document Upload API ───────────────────────────────────────────────── */

/**
 * Upload a document file.
 * @param {FormData} formData — must include 'file' and 'complaint_id'
 * @param {Function} [onProgress] — called with (percent: number)
 * @returns {Promise}
 */
async function uploadDocument(formData, onProgress) {
  const fileName = formData.get ? formData.get('file')?.name : 'unknown';
  console.log('[VeriLaw API] uploadDocument called for file:', fileName);

  return new Promise(resolve => {
    // Simulate progress
    if (typeof onProgress === 'function') {
      let pct = 0;
      const interval = setInterval(() => {
        pct = Math.min(pct + Math.random() * 20, 95);
        onProgress(Math.round(pct));
        if (pct >= 95) clearInterval(interval);
      }, 200);

      setTimeout(() => {
        clearInterval(interval);
        onProgress(100);
      }, 1500);
    }

    setTimeout(() => {
      const data = {
        file_id: Math.floor(Math.random() * 10000),
        original_name: fileName,
        stored_name: `vl_${Date.now()}_${fileName}`,
        file_type: 'document',
        status: 'uploaded',
        ocr_status: 'pending',
      };
      console.log('[VeriLaw API] uploadDocument response (placeholder):', { success: true, data });
      resolve({ success: true, message: 'Document uploaded successfully.', data });
    }, 1800);
  });

  // Production implementation:
  // return request('/documents/upload', { method: 'POST', body: formData, isFormData: true });
}

/* ── Documents API ─────────────────────────────────────────────────────── */

/**
 * Fetch list of uploaded/generated documents.
 * @param {{ page?: number, status?: string }} params
 * @returns {Promise}
 */
async function fetchDocuments(params = {}) {
  console.log('[VeriLaw API] fetchDocuments called with params:', params);

  return new Promise(resolve => {
    setTimeout(() => {
      const data = {
        total: 5,
        page: params.page || 1,
        documents: [
          { id: 1, name: 'Rental Agreement',   category: 'Legal',    status: 'Verified', size: '1.2 MB', date: new Date().toISOString() },
          { id: 2, name: 'Aadhaar Card',        category: 'Identity', status: 'Verified', size: '0.3 MB', date: new Date().toISOString() },
          { id: 3, name: 'Invoice May',         category: 'Finance',  status: 'Alert',    size: '0.8 MB', date: new Date().toISOString() },
          { id: 4, name: 'Bank Statement Q1',   category: 'Finance',  status: 'Pending',  size: '2.1 MB', date: new Date().toISOString() },
          { id: 5, name: 'Employment Letter',   category: 'Legal',    status: 'Verified', size: '0.4 MB', date: new Date().toISOString() },
        ],
      };
      console.log('[VeriLaw API] fetchDocuments response (placeholder):', { success: true, data });
      resolve({ success: true, message: '', data });
    }, 700);
  });

  // Production implementation:
  // const query = new URLSearchParams(params).toString();
  // return request(`/documents?${query}`);
}

/**
 * Delete a document by ID.
 * @param {number} documentId
 * @returns {Promise}
 */
async function deleteDocument(documentId) {
  console.log('[VeriLaw API] deleteDocument called for ID:', documentId);

  return new Promise(resolve => {
    setTimeout(() => {
      console.log('[VeriLaw API] deleteDocument response (placeholder):', { success: true, message: 'Document deleted.' });
      resolve({ success: true, message: 'Document deleted successfully.', data: null });
    }, 400);
  });

  // Production implementation:
  // return request(`/documents/${documentId}`, { method: 'DELETE' });
}

/* ── User Profile API ──────────────────────────────────────────────────── */

/**
 * Fetch the current user's profile.
 * @returns {Promise}
 */
async function fetchProfile() {
  console.log('[VeriLaw API] fetchProfile called');

  return new Promise(resolve => {
    setTimeout(() => {
      const data = {
        id: 1,
        full_name: 'Demo User',
        email: 'demo@verilaw.in',
        mobile: '9876543210',
        joined: new Date(Date.now() - 30 * 86400000).toISOString(),
        documents_count: 24,
        verified_count: 21,
      };
      console.log('[VeriLaw API] fetchProfile response (placeholder):', { success: true, data });
      resolve({ success: true, message: '', data });
    }, 500);
  });

  // Production implementation:
  // return request('/users/profile');
}

/* ── Exports ───────────────────────────────────────────────────────────── */
window.VLAPI = {
  loginUser,
  registerUser,
  logoutUser,
  fetchDashboard,
  fetchNotifications,
  uploadDocument,
  fetchDocuments,
  deleteDocument,
  fetchProfile,
};
