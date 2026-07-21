# VeriLaw — Frontend

**AI-Powered Legal Document Verification Platform**

---

## Project Overview

VeriLaw is a citizen-assistance platform that helps users verify legal documents, detect fraud, and prepare complaint packages before submitting them to the appropriate government authority. This repository contains the **frontend foundation** — production-ready HTML, CSS, and Vanilla JavaScript with no framework dependencies.

---

## Folder Structure

```
frontend/
├── index.html          Landing page
├── login.html          Login page
├── register.html       Registration page
├── dashboard.html      User dashboard
│
├── css/
│   ├── style.css       Master import (load this file only)
│   ├── variables.css   Design tokens (colors, spacing, typography)
│   ├── layout.css      Grid, containers, flex utilities, app shell
│   ├── components.css  Cards, navbar, modals, toasts, tables, badges
│   ├── buttons.css     Button variants and states
│   ├── forms.css       Inputs, validation states, file upload zone
│   ├── dashboard.css   Sidebar, header, stat cards, activity feed
│   └── responsive.css  Breakpoints: mobile / tablet / desktop
│
├── js/
│   ├── app.js          Application initializer, routing, theme, modals
│   ├── auth.js         Login, register, logout, session management
│   ├── dashboard.js    Dashboard data, sidebar, upload, analytics
│   ├── api.js          Placeholder API methods (backend-ready stubs)
│   ├── validation.js   Field validators, password strength meter
│   └── utils.js        Toast, counters, debounce, date helpers, DOM utils
│
└── assets/
    ├── logo.svg        VeriLaw wordmark (SVG, scalable)
    ├── hero.svg        Hero section illustration (SVG)
    └── icons/          Inline SVG icons (no external font CDN needed)
```

---

## How to Run

The frontend is a set of static HTML files — no build step required.

**Option 1 — Open directly in browser:**
```
open frontend/index.html
```

**Option 2 — Simple local server (Python):**
```bash
cd frontend
python3 -m http.server 8080
# Open http://localhost:8080
```

**Option 3 — Via Flask (future integration):**
Move files into the Flask `templates/` and `static/` directories.  
See [Future Flask Integration](#future-flask-integration) below.

---

## Technology Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Markup      | HTML5 (semantic, WCAG 2.1 AA) |
| Styling     | CSS3 — custom, modular, no frameworks |
| Scripting   | Vanilla JavaScript (ES6+)   |
| Font        | Inter (Google Fonts)         |
| Icons       | Inline SVG (no icon CDN)    |

**Intentionally excluded:** React, Vue, Angular, Bootstrap, Tailwind.  
All UI components are hand-crafted.

---

## Frontend Architecture

### CSS Architecture
- **CSS Custom Properties** (design tokens) for all colors, spacing, radii, shadows.
- **Mobile-first** breakpoints: `<768px` → `768–1024px` → `>1024px`.
- **Dark mode** via `[data-theme="dark"]` attribute on `<html>`.
- **Modular files** — no duplicate styles; every file has a single responsibility.

### JavaScript Architecture
All JS is organized as module-like IIFE-free namespaced objects exposed on `window`:

| Namespace       | Contents                                         |
|-----------------|--------------------------------------------------|
| `window.VLUtils`      | Toast, counters, debounce, DOM helpers, formatters |
| `window.VLValidation` | Field validators, password strength, form validators |
| `window.VLAPI`        | Placeholder API stubs (backend-ready)            |
| `window.VLAuth`       | Session, login, register, logout, Google OAuth stub |
| `window.VLDashboard`  | Dashboard data, sidebar, upload zone, notifications |
| `window.VLApp`        | Initializer, routing, theme, modals              |

**Script load order in HTML (bottom of `<body>`):**
```
utils.js → validation.js → api.js → auth.js → dashboard.js → app.js
```

### API Contract
All placeholder API functions return a consistent shape:
```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```

Replace the `setTimeout` bodies in `api.js` with real `fetch()` calls when the Flask backend is ready.

---

## Design System

| Token               | Value          |
|---------------------|----------------|
| Primary Color       | `#2563EB`      |
| Secondary Color     | `#0F172A`      |
| Accent Color        | `#06B6D4`      |
| Success             | `#22C55E`      |
| Warning             | `#F59E0B`      |
| Danger              | `#EF4444`      |
| Background          | `#F8FAFC`      |
| Surface             | `#FFFFFF`      |
| Primary Font        | Inter          |
| Border Radius (btn) | `12px`         |
| Border Radius (card)| `16px`         |

---

## Accessibility

- WCAG 2.1 AA compliant
- Semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<header>`, `<footer>`)
- ARIA labels on all interactive elements
- Visible focus indicators on all focusable elements
- Keyboard navigation for modals, dropdowns, accordions
- `prefers-reduced-motion` respected
- Sufficient color contrast ratios

---

## Future Flask Integration

1. Copy HTML files to `backend/templates/`.
2. Extend `base.html` with `{% block content %}`.
3. Replace static paths with `{{ url_for('static', filename='...') }}`.
4. Replace placeholder API functions in `api.js` with real `fetch()` calls to Flask routes.
5. Replace hardcoded dummy data with Jinja2 template variables where needed.

---

## Future API Integration

Each function in `api.js` includes a commented-out production `fetch()` call:
```javascript
// Production implementation:
// return request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) });
```

Uncomment and delete the `setTimeout` block to connect to the real backend.

---

## Legal Disclaimer

VeriLaw provides legal information and document verification assistance only. It does not constitute legal advice and is not a substitute for a qualified legal professional.

---

*Frontend v1.0 — VeriLaw Hackathon MVP*
