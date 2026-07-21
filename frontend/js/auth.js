/**
 * VeriLaw — Authentication Module
 * Handles login, register, logout, session persistence, and Google OAuth stub.
 * Depends on: utils.js, validation.js, api.js
 */

'use strict';

/* ── Session Helpers ───────────────────────────────────────────────────── */

const SESSION_KEY = 'vl_token';
const USER_KEY    = 'vl_user';

/**
 * Store session data after successful login.
 */
function setSession(token, user) {
  window.VLUtils.storageSet(SESSION_KEY, token);
  window.VLUtils.storageSet(USER_KEY, user);
}

/**
 * Clear session data on logout.
 */
function clearSession() {
  window.VLUtils.storageRemove(SESSION_KEY);
  window.VLUtils.storageRemove(USER_KEY);
}

/**
 * Return the stored JWT token, or null.
 */
function getToken() {
  return window.VLUtils.storageGet(SESSION_KEY);
}

/**
 * Return the stored user object, or null.
 */
function getCurrentUser() {
  return window.VLUtils.storageGet(USER_KEY);
}

/**
 * Return true if a token is present (simple session check).
 */
function isAuthenticated() {
  return !!getToken();
}

/**
 * Redirect to dashboard if already logged in (call from login/register pages).
 */
function redirectIfAuthenticated() {
  if (isAuthenticated()) {
    window.location.href = 'dashboard.html';
  }
}

/**
 * Redirect to login if NOT logged in (call from protected pages).
 */
function requireAuth() {
  if (!isAuthenticated()) {
    window.location.href = 'login.html';
  }
}

/* ── Login Handler ─────────────────────────────────────────────────────── */

/**
 * Initialize the login form: validation, submission, loading state.
 */
function initLoginForm() {
  const form         = document.getElementById('login-form');
  const emailInput   = document.getElementById('login-email');
  const passwordInput= document.getElementById('login-password');
  const submitBtn    = document.getElementById('login-submit');
  const showPassBtn  = document.getElementById('toggle-password');
  const rememberMe   = document.getElementById('remember-me');

  if (!form) return;

  // Bind real-time validation
  window.VLValidation.bindRealTimeValidation(emailInput,    window.VLValidation.validateEmail);
  window.VLValidation.bindRealTimeValidation(passwordInput, window.VLValidation.validateRequired.bind(null));

  // Password visibility toggle
  if (showPassBtn) {
    showPassBtn.addEventListener('click', () => {
      const isText = passwordInput.type === 'text';
      passwordInput.type = isText ? 'password' : 'text';
      showPassBtn.setAttribute('aria-label', isText ? 'Show password' : 'Hide password');
      showPassBtn.innerHTML = isText ? eyeIcon() : eyeOffIcon();
    });
  }

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email    = emailInput.value.trim();
    const password = passwordInput.value;

    // Validate
    const { valid, errors } = window.VLValidation.validateLoginForm({ email, password });

    if (!valid) {
      if (errors.email)    window.VLValidation.setFieldError(emailInput,    errors.email);
      if (errors.password) window.VLValidation.setFieldError(passwordInput, errors.password);
      return;
    }

    // Set loading state
    setButtonLoading(submitBtn, true, 'Logging in…');

    try {
      const result = await window.VLAPI.loginUser({ email, password });

      if (result.success) {
        // Persist session
        setSession(result.data.token, result.data.user);

        if (rememberMe && !rememberMe.checked) {
          // Token is session-only — actual implementation would use sessionStorage
        }

        window.VLUtils.showToast({
          type: 'success',
          title: 'Login Successful',
          message: 'Redirecting to your dashboard…',
          duration: 2000,
        });

        setTimeout(() => { window.location.href = 'dashboard.html'; }, 1200);
      } else {
        window.VLUtils.showToast({
          type: 'error',
          title: 'Login Failed',
          message: result.message || 'Incorrect email or password.',
        });
        setButtonLoading(submitBtn, false, 'Login');
      }
    } catch {
      window.VLUtils.showToast({
        type: 'error',
        title: 'Error',
        message: 'Something went wrong. Please try again.',
      });
      setButtonLoading(submitBtn, false, 'Login');
    }
  });
}

/* ── Register Handler ──────────────────────────────────────────────────── */

/**
 * Initialize the registration form.
 */
function initRegisterForm() {
  const form            = document.getElementById('register-form');
  const nameInput       = document.getElementById('reg-name');
  const emailInput      = document.getElementById('reg-email');
  const phoneInput      = document.getElementById('reg-phone');
  const passwordInput   = document.getElementById('reg-password');
  const confirmInput    = document.getElementById('reg-confirm-password');
  const termsInput      = document.getElementById('reg-terms');
  const submitBtn       = document.getElementById('register-submit');
  const showPassBtn     = document.getElementById('toggle-reg-password');
  const strengthMeter   = document.getElementById('password-strength');

  if (!form) return;

  // Real-time validation
  window.VLValidation.bindRealTimeValidation(nameInput,    window.VLValidation.validateFullName);
  window.VLValidation.bindRealTimeValidation(emailInput,   window.VLValidation.validateEmail);
  window.VLValidation.bindRealTimeValidation(phoneInput,   window.VLValidation.validatePhone);
  window.VLValidation.bindRealTimeValidation(passwordInput, window.VLValidation.validatePassword);

  // Confirm password: re-validate whenever either field changes
  const validateConfirm = () => {
    if (!confirmInput.value) return;
    const result = window.VLValidation.validateConfirmPassword(confirmInput.value, passwordInput.value);
    result.valid
      ? window.VLValidation.setFieldSuccess(confirmInput)
      : window.VLValidation.setFieldError(confirmInput, result.message);
  };
  confirmInput.addEventListener('blur', validateConfirm);
  confirmInput.addEventListener('input', validateConfirm);
  passwordInput.addEventListener('input', validateConfirm);

  // Password strength meter
  if (passwordInput && strengthMeter) {
    passwordInput.addEventListener('input', () => {
      window.VLValidation.updatePasswordStrengthUI(passwordInput.value, strengthMeter);
    });
  }

  // Password toggle
  if (showPassBtn) {
    showPassBtn.addEventListener('click', () => {
      const isText = passwordInput.type === 'text';
      passwordInput.type = isText ? 'password' : 'text';
      showPassBtn.innerHTML = isText ? eyeIcon() : eyeOffIcon();
    });
  }

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fields = {
      fullName:        nameInput.value.trim(),
      email:           emailInput.value.trim(),
      phone:           phoneInput.value.trim(),
      password:        passwordInput.value,
      confirmPassword: confirmInput.value,
      terms:           termsInput && termsInput.checked,
    };

    const { valid, errors } = window.VLValidation.validateRegisterForm(fields);

    if (!valid) {
      if (errors.fullName)        window.VLValidation.setFieldError(nameInput,     errors.fullName);
      if (errors.email)           window.VLValidation.setFieldError(emailInput,    errors.email);
      if (errors.phone)           window.VLValidation.setFieldError(phoneInput,    errors.phone);
      if (errors.password)        window.VLValidation.setFieldError(passwordInput, errors.password);
      if (errors.confirmPassword) window.VLValidation.setFieldError(confirmInput,  errors.confirmPassword);
      if (errors.terms) {
        window.VLUtils.showToast({ type: 'warning', title: 'Terms Required', message: errors.terms });
      }
      return;
    }

    setButtonLoading(submitBtn, true, 'Creating account…');

    try {
      const result = await window.VLAPI.registerUser({
        full_name: fields.fullName,
        email:     fields.email,
        mobile:    fields.phone,
        password:  fields.password,
      });

      if (result.success) {
        window.VLUtils.showToast({
          type: 'success',
          title: 'Account Created!',
          message: 'Please log in to continue.',
          duration: 2500,
        });
        setTimeout(() => { window.location.href = 'login.html'; }, 1500);
      } else {
        window.VLUtils.showToast({
          type: 'error',
          title: 'Registration Failed',
          message: result.message || 'Please check your details and try again.',
        });
        setButtonLoading(submitBtn, false, 'Create Account');
      }
    } catch {
      window.VLUtils.showToast({
        type: 'error',
        title: 'Error',
        message: 'Something went wrong. Please try again.',
      });
      setButtonLoading(submitBtn, false, 'Create Account');
    }
  });
}

/* ── Logout Handler ────────────────────────────────────────────────────── */

/**
 * Bind logout buttons across the page.
 */
function initLogout() {
  const logoutBtns = document.querySelectorAll('[data-action="logout"]');
  logoutBtns.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      await logoutUser();
    });
  });
}

/**
 * Perform logout: clear session, call API stub, redirect.
 */
async function logoutUser() {
  try {
    await window.VLAPI.logoutUser();
  } finally {
    clearSession();
    window.VLUtils.showToast({ type: 'info', title: 'Logged Out', message: 'See you soon!' });
    setTimeout(() => { window.location.href = 'login.html'; }, 800);
  }
}

/* ── Google OAuth Stub ─────────────────────────────────────────────────── */

function initGoogleAuth() {
  const googleBtn = document.getElementById('btn-google');
  if (!googleBtn) return;
  googleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.VLUtils.showToast({
      type: 'info',
      title: 'Google Login',
      message: 'Google authentication will be available after backend integration.',
      duration: 4000,
    });
    console.log('[VeriLaw Auth] Google OAuth stub triggered — requires backend OAuth flow.');
  });
}

/* ── Forgot Password Stub ──────────────────────────────────────────────── */

function initForgotPassword() {
  const link = document.getElementById('forgot-password-link');
  if (!link) return;
  link.addEventListener('click', (e) => {
    e.preventDefault();
    window.VLUtils.showToast({
      type: 'info',
      title: 'Password Reset',
      message: 'Password reset will be available after backend integration.',
      duration: 4000,
    });
  });
}

/* ── UI Helpers ────────────────────────────────────────────────────────── */

function setButtonLoading(btn, loading, label) {
  if (!btn) return;
  if (loading) {
    btn.classList.add('btn--loading');
    btn.disabled = true;
    const textEl = btn.querySelector('.btn__text');
    if (textEl) textEl.textContent = label;
  } else {
    btn.classList.remove('btn--loading');
    btn.disabled = false;
    const textEl = btn.querySelector('.btn__text');
    if (textEl) textEl.textContent = label;
  }
}

function eyeIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>`;
}

function eyeOffIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></svg>`;
}

/* ── Exports ───────────────────────────────────────────────────────────── */
window.VLAuth = {
  initLoginForm,
  initRegisterForm,
  initLogout,
  logoutUser,
  initGoogleAuth,
  initForgotPassword,
  getToken,
  getCurrentUser,
  isAuthenticated,
  redirectIfAuthenticated,
  requireAuth,
};
