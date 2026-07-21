/**
 * VeriLaw — Form Validation Module
 * Email, password (strength meter), phone, complaint fields.
 * All functions are pure — they return {valid, message}.
 */

'use strict';

/* ── Field Validators ──────────────────────────────────────────────────── */

/**
 * Validate an email address.
 * @param {string} value
 * @returns {{ valid: boolean, message: string }}
 */
function validateEmail(value) {
  if (!value || !value.trim()) {
    return { valid: false, message: 'Email address is required.' };
  }
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!re.test(value.trim())) {
    return { valid: false, message: 'Please enter a valid email address.' };
  }
  return { valid: true, message: '' };
}

/**
 * Validate a password (minimum 8 characters).
 * @param {string} value
 * @returns {{ valid: boolean, message: string }}
 */
function validatePassword(value) {
  if (!value) {
    return { valid: false, message: 'Password is required.' };
  }
  if (value.length < 8) {
    return { valid: false, message: 'Password must be at least 8 characters.' };
  }
  return { valid: true, message: '' };
}

/**
 * Validate that confirm password matches the original.
 * @param {string} value
 * @param {string} original
 * @returns {{ valid: boolean, message: string }}
 */
function validateConfirmPassword(value, original) {
  if (!value) {
    return { valid: false, message: 'Please confirm your password.' };
  }
  if (value !== original) {
    return { valid: false, message: 'Passwords do not match.' };
  }
  return { valid: true, message: '' };
}

/**
 * Validate a phone number (exactly 10 digits).
 * @param {string} value
 * @returns {{ valid: boolean, message: string }}
 */
function validatePhone(value) {
  if (!value || !value.trim()) {
    return { valid: false, message: 'Phone number is required.' };
  }
  const digits = value.replace(/\D/g, '');
  if (digits.length !== 10) {
    return { valid: false, message: 'Phone number must be exactly 10 digits.' };
  }
  return { valid: true, message: '' };
}

/**
 * Validate a required text field.
 * @param {string} value
 * @param {string} fieldName
 * @returns {{ valid: boolean, message: string }}
 */
function validateRequired(value, fieldName = 'This field') {
  if (!value || !value.trim()) {
    return { valid: false, message: `${fieldName} is required.` };
  }
  return { valid: true, message: '' };
}

/**
 * Validate a full name (at least 2 chars, no numbers).
 * @param {string} value
 * @returns {{ valid: boolean, message: string }}
 */
function validateFullName(value) {
  if (!value || !value.trim()) {
    return { valid: false, message: 'Full name is required.' };
  }
  if (value.trim().length < 2) {
    return { valid: false, message: 'Name must be at least 2 characters.' };
  }
  if (/\d/.test(value)) {
    return { valid: false, message: 'Name must not contain numbers.' };
  }
  return { valid: true, message: '' };
}

/**
 * Validate a complaint description (minimum 30 characters).
 * @param {string} value
 * @returns {{ valid: boolean, message: string }}
 */
function validateComplaintDescription(value) {
  if (!value || !value.trim()) {
    return { valid: false, message: 'Complaint description is required.' };
  }
  if (value.trim().length < 30) {
    return { valid: false, message: `Description too short. ${30 - value.trim().length} more character(s) needed.` };
  }
  return { valid: true, message: '' };
}

/* ── Password Strength ─────────────────────────────────────────────────── */

/**
 * Calculate password strength score (0–4).
 * @param {string} password
 * @returns {{ score: number, label: string, cssClass: string }}
 */
function getPasswordStrength(password) {
  if (!password) return { score: 0, label: '', cssClass: '' };

  let score = 0;
  if (password.length >= 8)  score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const levels = [
    { score: 0, label: '',        cssClass: '' },
    { score: 1, label: 'Weak',    cssClass: 'weak' },
    { score: 2, label: 'Fair',    cssClass: 'fair' },
    { score: 3, label: 'Good',    cssClass: 'good' },
    { score: 4, label: 'Strong',  cssClass: 'strong' },
  ];

  const capped = Math.min(score, 4);
  return levels[capped];
}

/**
 * Update password strength meter UI.
 * @param {string} password
 * @param {HTMLElement} meterEl — element with class 'password-strength'
 */
function updatePasswordStrengthUI(password, meterEl) {
  if (!meterEl) return;
  const bars  = meterEl.querySelectorAll('.password-strength__bar');
  const label = meterEl.querySelector('.password-strength__label');
  const { score, label: text, cssClass } = getPasswordStrength(password);

  bars.forEach((bar, i) => {
    bar.className = 'password-strength__bar';
    if (i < score) {
      bar.classList.add(`active-${cssClass}`);
    }
  });

  if (label) {
    label.textContent = text;
    label.className = `password-strength__label ${cssClass}`;
  }
}

/* ── Field UI State Helpers ────────────────────────────────────────────── */

/**
 * Apply success styling to a form group.
 */
function setFieldSuccess(inputEl) {
  const group = inputEl.closest('.form-group');
  if (!group) return;
  group.classList.remove('form-group--error');
  group.classList.add('form-group--success');
  const errEl = group.querySelector('.form-error');
  if (errEl) errEl.textContent = '';
}

/**
 * Apply error styling and message to a form group.
 */
function setFieldError(inputEl, message) {
  const group = inputEl.closest('.form-group');
  if (!group) return;
  group.classList.remove('form-group--success');
  group.classList.add('form-group--error');
  let errEl = group.querySelector('.form-error');
  if (!errEl) {
    errEl = document.createElement('p');
    errEl.className = 'form-error';
    errEl.setAttribute('role', 'alert');
    group.appendChild(errEl);
  }
  errEl.textContent = message;
}

/**
 * Clear validation state from a form group.
 */
function clearFieldState(inputEl) {
  const group = inputEl.closest('.form-group');
  if (!group) return;
  group.classList.remove('form-group--error', 'form-group--success');
  const errEl = group.querySelector('.form-error');
  if (errEl) errEl.textContent = '';
}

/* ── Full Form Validators ──────────────────────────────────────────────── */

/**
 * Validate the login form.
 * @param {{ email: string, password: string }} fields
 * @returns {{ valid: boolean, errors: Object }}
 */
function validateLoginForm({ email, password }) {
  const errors = {};
  const emailResult = validateEmail(email);
  if (!emailResult.valid) errors.email = emailResult.message;

  const passResult = validateRequired(password, 'Password');
  if (!passResult.valid) errors.password = passResult.message;

  return { valid: Object.keys(errors).length === 0, errors };
}

/**
 * Validate the register form.
 * @param {{ fullName, email, phone, password, confirmPassword, terms }} fields
 * @returns {{ valid: boolean, errors: Object }}
 */
function validateRegisterForm({ fullName, email, phone, password, confirmPassword, terms }) {
  const errors = {};

  const nameResult = validateFullName(fullName);
  if (!nameResult.valid) errors.fullName = nameResult.message;

  const emailResult = validateEmail(email);
  if (!emailResult.valid) errors.email = emailResult.message;

  const phoneResult = validatePhone(phone);
  if (!phoneResult.valid) errors.phone = phoneResult.message;

  const passResult = validatePassword(password);
  if (!passResult.valid) errors.password = passResult.message;

  const confirmResult = validateConfirmPassword(confirmPassword, password);
  if (!confirmResult.valid) errors.confirmPassword = confirmResult.message;

  if (!terms) errors.terms = 'You must agree to the Terms of Service.';

  return { valid: Object.keys(errors).length === 0, errors };
}

/* ── Real-time Validation Binding ─────────────────────────────────────── */

/**
 * Bind real-time validation to an input element.
 * @param {HTMLInputElement} inputEl
 * @param {Function} validatorFn - receives value, returns {valid, message}
 * @param {any[]} [extraArgs] - additional arguments for the validator
 */
function bindRealTimeValidation(inputEl, validatorFn, extraArgs = []) {
  if (!inputEl) return;

  const validate = () => {
    const result = validatorFn(inputEl.value, ...extraArgs);
    if (inputEl.value === '') {
      clearFieldState(inputEl);
    } else if (result.valid) {
      setFieldSuccess(inputEl);
    } else {
      setFieldError(inputEl, result.message);
    }
  };

  inputEl.addEventListener('blur', validate);
  inputEl.addEventListener('input', window.VLUtils
    ? window.VLUtils.debounce(validate, 400)
    : validate
  );
}

/* ── Exports ───────────────────────────────────────────────────────────── */
window.VLValidation = {
  validateEmail,
  validatePassword,
  validateConfirmPassword,
  validatePhone,
  validateRequired,
  validateFullName,
  validateComplaintDescription,
  getPasswordStrength,
  updatePasswordStrengthUI,
  setFieldSuccess,
  setFieldError,
  clearFieldState,
  validateLoginForm,
  validateRegisterForm,
  bindRealTimeValidation,
};
