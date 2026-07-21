# 11_UI_Style_Guide.md

# Judiciary Flow

## UI/UX Design System & Style Guide

**Version:** 1.0

**Project:** Judiciary Flow

**Document Type:** UI Style Guide

**Design Language**

- Modern
- Clean
- Professional
- Government Friendly
- AI Powered
- Mobile First
- Accessible
- High Performance

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | July 2026 | Initial UI Design System |

---

# Table of Contents

1. Design Philosophy
2. Design Principles
3. Brand Identity
4. Color System
5. Typography
6. Icons
7. Spacing System
8. Border Radius
9. Elevation & Shadows
10. Glassmorphism
11. Design Tokens

---

# 1. Design Philosophy

Judiciary Flow is designed to make legal complaint filing feel **simple, trustworthy, and approachable**.

The interface should reduce user anxiety while guiding users through complex legal processes.

The design focuses on:

- Simplicity
- Trust
- Accessibility
- Speed
- Consistency
- Clarity

---

# Design Goals

✅ Easy for first-time users

✅ Government-inspired trust

✅ Modern startup aesthetics

✅ Mobile-first

✅ Fast interactions

✅ Minimal learning curve

---

# User Personas

### Students

Need quick complaint filing.

---

### Working Professionals

Need speed and efficiency.

---

### Senior Citizens

Need larger text and simple navigation.

---

### Rural Users

Need clean interfaces with minimal complexity.

---

### Users with Disabilities

Need accessible colors, keyboard navigation, and readable typography.

---

# 2. Design Principles

Every screen must follow these principles.

---

## Principle 1

### Clarity First

Every page should communicate one primary action.

Example

```
Create Complaint

Upload Evidence

Generate PDF
```

Never overload the screen.

---

## Principle 2

### Progressive Disclosure

Show information gradually.

Instead of showing 20 fields,

display them step-by-step.

---

## Principle 3

### Reduce Cognitive Load

Avoid long forms.

Use

- Step indicators
- Progress bars
- Smart defaults
- Helpful hints

---

## Principle 4

### Accessibility

Every component should support

- Keyboard navigation
- Screen readers
- High contrast
- Focus indicators

---

## Principle 5

### Motion with Purpose

Animations should improve usability,

not distract users.

---

# 3. Brand Identity

## Brand Personality

- Trustworthy
- Intelligent
- Professional
- Friendly
- Modern
- Secure

---

## Brand Keywords

```
Justice

Technology

Trust

Transparency

Accessibility

Efficiency
```

---

## Logo Style

Preferred

Simple Icon

+

Wordmark

Example

```
⚖ Judiciary Flow
```

Logo Characteristics

- Flat Design
- Rounded Corners
- Minimal
- Scalable
- SVG Preferred

---

# 4. Color System

## Primary Color

```
#2563EB
```

Purpose

- Buttons
- Links
- Active Menu
- Primary Actions

---

## Secondary Color

```
#0F172A
```

Purpose

- Headers
- Navigation
- Sidebar

---

## Accent Color

```
#06B6D4
```

Purpose

- AI Features
- Progress
- Highlights

---

## Success

```
#22C55E
```

Purpose

- Success Messages
- Completed Status
- Checkmarks

---

## Warning

```
#F59E0B
```

Purpose

- Pending
- Warning Messages

---

## Error

```
#EF4444
```

Purpose

- Validation Errors
- Delete Actions

---

## Background

```
#F8FAFC
```

---

## Card Background

```
#FFFFFF
```

---

## Text Colors

Primary

```
#0F172A
```

Secondary

```
#64748B
```

Disabled

```
#CBD5E1
```

---

# Complete Color Palette

| Purpose | Color |
|----------|---------|
| Primary | #2563EB |
| Secondary | #0F172A |
| Accent | #06B6D4 |
| Success | #22C55E |
| Warning | #F59E0B |
| Error | #EF4444 |
| Background | #F8FAFC |
| Card | #FFFFFF |
| Border | #E2E8F0 |

---

# 5. Typography

## Font Family

Primary

```
Poppins
```

Fallback

```
sans-serif
```

---

## Font Scale

| Element | Size | Weight |
|----------|------|---------|
| H1 | 42px | 700 |
| H2 | 34px | 700 |
| H3 | 28px | 600 |
| H4 | 22px | 600 |
| H5 | 18px | 600 |
| Body | 16px | 400 |
| Small | 14px | 400 |
| Caption | 12px | 400 |

---

## Line Height

Heading

```
1.2
```

Body

```
1.6
```

---

# 6. Icon System

Recommended Library

```
Font Awesome 6
```

or

```
Bootstrap Icons
```

---

## Icon Sizes

| Usage | Size |
|--------|------|
| Small | 16px |
| Normal | 20px |
| Large | 24px |
| Hero | 48px |

---

## Common Icons

| Feature | Icon |
|----------|------|
| Dashboard | Home |
| Complaint | File |
| Evidence | Upload |
| OCR | Scan |
| AI | Brain |
| Documents | PDF |
| Settings | Gear |
| Profile | User |
| Logout | Arrow Right |

---

# 7. Spacing System

Use an **8-point spacing system** throughout the application.

| Token | Value |
|--------|-------|
| XS | 4px |
| SM | 8px |
| MD | 16px |
| LG | 24px |
| XL | 32px |
| XXL | 48px |
| XXXL | 64px |

---

## Section Padding

Desktop

```
48px
```

Tablet

```
32px
```

Mobile

```
20px
```

---

# 8. Border Radius

| Component | Radius |
|------------|---------|
| Button | 12px |
| Card | 16px |
| Input | 12px |
| Modal | 20px |
| Badge | 999px |

---

# 9. Elevation & Shadows

## Card

```css
box-shadow:
0 10px 30px rgba(0,0,0,0.08);
```

---

## Button Hover

```css
box-shadow:
0 12px 25px rgba(37,99,235,0.25);
```

---

## Modal

```css
box-shadow:
0 30px 80px rgba(0,0,0,0.18);
```

---

# 10. Glassmorphism Rules

Glassmorphism should be used sparingly.

Allowed

- Dashboard Cards
- AI Result Cards
- Modals

Not Recommended

- Forms
- Tables
- Navigation

---

## Glass Card Style

```css
background:
rgba(255,255,255,.7);

backdrop-filter:
blur(16px);

border:
1px solid rgba(255,255,255,.4);
```

---

# 11. Design Tokens

```css
:root{

--primary:#2563EB;

--secondary:#0F172A;

--accent:#06B6D4;

--success:#22C55E;

--warning:#F59E0B;

--danger:#EF4444;

--background:#F8FAFC;

--surface:#FFFFFF;

--text:#0F172A;

--text-secondary:#64748B;

--border:#E2E8F0;

--radius-sm:12px;

--radius-md:16px;

--radius-lg:20px;

--shadow-card:0 10px 30px rgba(0,0,0,.08);

--shadow-hover:0 15px 35px rgba(37,99,235,.18);

--transition:300ms ease;

}
```

---

# UI Design Rules

✅ White backgrounds

✅ Large cards

✅ Rounded corners

✅ Plenty of spacing

✅ High contrast

✅ Consistent button styles

✅ Mobile-first layouts

✅ Maximum content width: **1440px**

✅ Use CSS variables for all colors and spacing

❌ No inline styles

❌ No inconsistent button designs

❌ No excessive gradients

❌ No flashing animations

---

# Part 1 Summary

This section establishes the complete visual identity for Judiciary Flow, including:

- Brand philosophy
- Color palette
- Typography
- Icon system
- Spacing
- Elevation
- Glassmorphism
- Design tokens

These standards ensure a modern, consistent, and accessible interface that AI coding agents can implement reliably.

---

## End of Part 1

**Next:** **Part 2 — Layout System, Responsive Grid, Navigation, Sidebar, Header, Buttons, Forms, Cards, Tables, Modals, Toasts, File Upload Components & Progress Indicators.**

# Part 2 — Layout System, Components & Responsive Design

---

# 12. Layout System

Judiciary Flow follows a **12-column responsive grid system** with a **maximum width of 1440px**.

---

## Desktop

```
┌──────────────────────────────────────────────┐

 Sidebar │          Main Content               │

 280px   │                                    │

         │                                    │

         │                                    │

└──────────────────────────────────────────────┘
```

---

## Tablet

```
┌───────────────────────────────┐

 Header

────────────────────────────────

 Main Content

────────────────────────────────

 Bottom Navigation

└───────────────────────────────┘
```

---

## Mobile

```
┌────────────────────┐

☰ Judiciary Flow

────────────────────

Main Content

────────────────────

Bottom Navigation

└────────────────────┘
```

---

# Responsive Breakpoints

| Device | Width |
|---------|-------|
| Mobile | 0–767px |
| Tablet | 768–1023px |
| Laptop | 1024–1439px |
| Desktop | 1440px+ |

---

# Content Width

```css
max-width:1440px;

margin:auto;

padding:24px;
```

---

# 13. Navigation

Navigation should always remain simple.

---

## Desktop Navigation

```
Dashboard

Complaints

Evidence

Documents

Profile

Settings

Logout
```

---

## Mobile Navigation

```
🏠 Dashboard

📄 Complaints

📂 Evidence

👤 Profile
```

Maximum

```
5 Navigation Items
```

---

# Active Navigation

```css
background:#2563EB;

color:white;

border-radius:12px;
```

---

# Hover State

```css
background:#EFF6FF;
```

---

# 14. Sidebar

Desktop Sidebar Width

```
280px
```

Collapsed

```
80px
```

---

## Sidebar Components

- Logo
- Search
- Navigation
- Divider
- User Card
- Logout

---

## Sidebar Animation

```
Slide

250ms

ease
```

---

# Sidebar Style

```css
background:white;

border-right:1px solid #E2E8F0;
```

---

# 15. Header

Header Height

```
72px
```

---

## Components

- Breadcrumb
- Search
- Notifications
- Theme Toggle
- Profile Menu

---

Header Shadow

```css
box-shadow:

0 5px 15px rgba(0,0,0,.05);
```

---

# 16. Dashboard Cards

Cards should display

- Total Complaints
- Pending
- Completed
- Documents

---

## Card Layout

```
┌─────────────────────┐

📄

Total Complaints

145

+12%

└─────────────────────┘
```

---

## Card Style

```css
padding:24px;

border-radius:16px;

background:white;

box-shadow:

var(--shadow-card);
```

---

## Hover Effect

```css
transform:

translateY(-6px);

transition:

300ms;
```

---

# 17. Buttons

Button Types

---

## Primary

```
Create Complaint
```

Style

```css
background:

var(--primary);

color:white;
```

---

## Secondary

```
Cancel
```

---

## Success

```
Generate PDF
```

---

## Danger

```
Delete
```

---

## Button Sizes

| Size | Height |
|------|--------|
| Small | 36px |
| Medium | 44px |
| Large | 52px |

---

## Button Hover

```css
transform:

translateY(-2px);
```

---

## Button Click

```css
transform:

scale(.98);
```

---

# 18. Forms

Forms should feel clean and guided.

---

## Input Style

```css
height:52px;

border-radius:12px;

padding:16px;
```

---

## Labels

Always visible.

Never use placeholder as label.

---

## Validation

Success

Green Border

---

Error

Red Border

---

Helper Text

Gray

---

Required Fields

Show

```
*
```

---

# Complaint Form

```
Title

Description

State

District

Incident Date

Category

Submit
```

---

# 19. Tables

Used for

- Complaint History
- Documents
- Activity Logs

---

## Table Style

```css
border-radius:16px;

overflow:hidden;
```

---

## Row Hover

```css
background:

#F8FAFC;
```

---

## Pagination

Bottom Right

```
Previous

1

2

3

Next
```

---

# 20. Modals

Use for

- Delete Confirmation
- Logout
- Preview
- AI Results

---

## Width

```
600px
```

---

Border Radius

```
20px
```

---

Animation

```
Fade

+

Scale
```

---

# 21. Toast Notifications

Position

```
Top Right
```

---

Duration

```
3 Seconds
```

---

Types

✅ Success

⚠ Warning

❌ Error

ℹ Information

---

Example

```
Complaint Created Successfully
```

---

# 22. File Upload Component

Use Drag & Drop.

---

Layout

```
┌──────────────────────────────┐

⬆

Drop Files Here

or

Browse Files

──────────────────────────────

Supported

PDF JPG PNG

└──────────────────────────────┘
```

---

Hover

```css
border:

2px dashed

var(--primary);
```

---

Success

Green Checkmark

---

Error

Red Border

---

# Upload Progress

```
██████████░░░░░

65%
```

---

# 23. Progress Indicators

Use progress indicators for

- OCR
- AI Prediction
- PDF Generation
- Upload

---

Linear Progress

```css
height:8px;

border-radius:999px;
```

---

Circular Progress

Use for

```
OCR

AI

PDF
```

---

# 24. Empty States

Instead of empty pages,

show helpful illustrations.

Example

```
📄

No Complaints Yet

Create Your First Complaint

[Create Complaint]
```

---

# 25. Error States

Example

```
⚠

Something went wrong

Try Again

[Retry]
```

---

# 26. Loading States

Never show blank screens.

Use

- Skeleton Cards
- Skeleton Tables
- Skeleton Forms

---

Example

```
████████████

██████

██████████████
```

---

# 27. Search Component

Global Search

```
🔍 Search complaints...
```

Features

- Instant Search
- Auto Suggestions
- Keyboard Friendly

---

# 28. Filter Components

Common Filters

- Category

- Department

- Date

- Status

- State

- District

---

# Filter Chips

```
Consumer

Completed

Ahmedabad

Today
```

---

# 29. Dashboard Widgets

Widgets

- Complaint Summary

- Recent Activity

- AI Suggestions

- Pending Complaints

- Generated Documents

---

# Widget Grid

```
2 Columns

Desktop

↓

1 Column

Mobile
```

---

# Component Accessibility Rules

Every component must

✅ Be keyboard accessible

✅ Have visible focus

✅ Have ARIA labels

✅ Support screen readers

✅ Have sufficient color contrast

---

# Component Summary

| Component | Status |
|------------|--------|
| Sidebar | ✅ |
| Header | ✅ |
| Dashboard Cards | ✅ |
| Buttons | ✅ |
| Forms | ✅ |
| Tables | ✅ |
| Modals | ✅ |
| Toasts | ✅ |
| File Upload | ✅ |
| Progress Indicators | ✅ |
| Search | ✅ |
| Filters | ✅ |
| Widgets | ✅ |

---

## End of Part 2

**Next:** **Part 3 — Complete Screen Specifications (Landing Page, Login, Register, Dashboard, Complaint Wizard, Evidence Upload, OCR Results, AI Recommendation, Profile, Settings, Mobile Screens).**

# Part 3 — Complete Screen Specifications (UI/UX)

---

# 30. Design Principles for All Screens

Every screen in Judiciary Flow must follow these rules.

✅ Mobile First

✅ Clean Layout

✅ Large Touch Targets

✅ Accessible

✅ Minimal Text

✅ Guided User Journey

✅ Animated Transitions

✅ Fast Loading

---

# Screen Navigation Flow

```text
Landing Page

↓

Login / Register

↓

Dashboard

↓

Create Complaint

↓

AI Analysis

↓

Department Recommendation

↓

Upload Evidence

↓

OCR Results

↓

Complaint Preview

↓

Generate PDF

↓

Profile
```

---

# 31. Landing Page

## Purpose

Introduce Judiciary Flow and encourage users to register or log in.

---

## Layout

```text
------------------------------------------------

LOGO

Judiciary Flow

Making Legal Complaint Filing Easy

[Get Started]

[Learn More]

Illustration

Features

Footer

------------------------------------------------
```

---

## Sections

- Hero Section
- Feature Cards
- How It Works
- Benefits
- Footer

---

## CTA Buttons

Primary

```
Get Started
```

Secondary

```
Learn More
```

---

## Animation

Hero fades in

↓

Illustration floats

↓

Cards slide up

↓

Buttons glow on hover

---

# 32. Login Screen

## Layout

```text
--------------------------------

Logo

Welcome Back

Email

Password

Forgot Password?

[Login]

Create Account

--------------------------------
```

---

## Validation

Email

Password Required

Invalid Credentials

---

## Success

Redirect

↓

Dashboard

---

## Animation

Card Fade In

Input Focus Glow

Button Ripple

---

# 33. Register Screen

## Fields

- Full Name

- Email

- Mobile

- Password

- Confirm Password

---

## Button

```
Create Account
```

---

## Validation

Email Unique

Password Match

10 Digit Mobile

---

## Success

Registration Success

↓

Login

---

# 34. Dashboard

## Purpose

Main workspace after login.

---

## Layout

```text
Sidebar

|

Header

|

-------------------------------------------------

Cards

Complaints

Documents

Pending

Completed

-------------------------------------------------

Recent Complaints

-------------------------------------------------

Recent Documents

-------------------------------------------------

AI Suggestions

-------------------------------------------------
```

---

## Dashboard Cards

- Total Complaints

- Pending

- Completed

- Documents

---

## Widgets

- Recent Activity

- AI Suggestions

- Timeline

---

## Animation

Cards Count Up

Charts Animate

Cards Hover Lift

---

# 35. Complaint Wizard

Instead of one long form,

use a multi-step wizard.

---

## Step 1

Basic Information

```
Title

Description
```

---

## Step 2

Location

```
State

District

Date
```

---

## Step 3

AI Classification

```
Predicted Category

Confidence

Department
```

---

## Step 4

Upload Evidence

---

## Step 5

Preview Complaint

---

## Step 6

Generate PDF

---

## Wizard Progress

```text
1

↓

2

↓

3

↓

4

↓

5

↓

6
```

---

# 36. AI Recommendation Screen

Layout

```text
🧠 AI Analysis

--------------------------------

Category

Consumer Complaint

Confidence

96%

Department

Consumer Commission

Reason

Consumer disputes belong to Consumer Commission.

--------------------------------

Accept

Change Category
```

---

## Animation

Brain Pulse

↓

Progress Bar

↓

Result Card Slides In

↓

Department Card Fades In

---

# 37. Evidence Upload Screen

## Layout

```text
Drop Files Here

↓

Upload

↓

Preview

↓

OCR
```

---

## Supported Files

- JPG

- PNG

- PDF

- Audio

---

## Preview

Thumbnail Grid

---

## Upload Animation

Drag

↓

Glow Border

↓

Upload Progress

↓

Success Checkmark

---

# 38. OCR Result Screen

## Layout

```text
Uploaded Image

↓

Extracted Text

↓

Entities

↓

Timeline
```

---

Example

```text
Invoice

Date

Amount

Organization

Customer
```

---

## Buttons

Copy

Download

Edit

Continue

---

## Animation

Scanning Line

↓

Circular Progress

↓

Text Appears

↓

Entity Cards Fade In

---

# 39. Complaint Preview Screen

Purpose

Allow users to review everything before generating the final document.

---

Layout

```text
Complaint

↓

Evidence

↓

Department

↓

Timeline

↓

Generate PDF
```

---

Buttons

Edit

Generate

Cancel

---

# 40. PDF Generation Screen

Layout

```text
Generating Complaint...

██████████████

85%
```

---

Animation

Paper Appears

↓

Loading Ring

↓

Checkmark

↓

Download Button

---

# 41. Complaint History Screen

Table

```text
Complaint

Category

Status

Created

Actions
```

---

Filters

Category

Status

Date

---

Actions

View

Edit

Delete

Download

---

# 42. Profile Screen

Fields

- Name

- Email

- Mobile

- Password

---

Buttons

Update

Change Password

Logout

---

Animation

Profile Card

↓

Slide Up

---

# 43. Settings Screen

Options

- Theme

- Notifications

- Language (Future)

- Account

- Privacy

---

Cards

```text
General

Notifications

Security

About
```

---

# 44. Mobile Design

Bottom Navigation

```text
🏠

📄

📂

👤
```

---

Cards

One Column

---

Buttons

Full Width

---

Forms

Stacked

---

Sidebar

Drawer Menu

---

# 45. Tablet Design

Sidebar

Collapsed

---

Grid

Two Columns

---

Cards

Medium Size

---

# 46. Empty States

Complaint

```text
📄

No Complaints

Create your first complaint.
```

---

Evidence

```text
📂

No Evidence Uploaded
```

---

Documents

```text
📑

No Generated Documents
```

---

# 47. Error Screens

Network

```text
⚠

No Internet

Retry
```

---

404

```text
Page Not Found

Go Home
```

---

500

```text
Something went wrong.
```

---

# 48. Success Screens

Complaint

```text
✅

Complaint Created Successfully
```

---

PDF

```text
✅

PDF Generated Successfully
```

---

Upload

```text
✅

Evidence Uploaded Successfully
```

---

# Screen Summary

| Screen | Status |
|----------|--------|
| Landing | ✅ |
| Login | ✅ |
| Register | ✅ |
| Dashboard | ✅ |
| Complaint Wizard | ✅ |
| AI Recommendation | ✅ |
| Evidence Upload | ✅ |
| OCR Results | ✅ |
| Complaint Preview | ✅ |
| PDF Generation | ✅ |
| History | ✅ |
| Profile | ✅ |
| Settings | ✅ |
| Mobile | ✅ |
| Tablet | ✅ |

---

## End of Part 3

**Next:** **Part 4 — Highly Animated UI (Modern Micro-interactions, Glassmorphism, Premium Dashboard Animations, AI Processing Animations, OCR Scanning Effects, Success Animations, Skeleton Loaders, Page Transitions & Motion Design).** ⭐⭐⭐⭐⭐

# Part 4 — Motion Design System (Highly Animated Premium UI)

> **Goal:** Create a premium, modern, highly animated interface using only **HTML5 + CSS3 + Vanilla JavaScript**. Animations should improve usability and provide feedback without overwhelming users.

---

# 49. Motion Design Principles

Every animation should satisfy at least one of these goals:

- Guide the user's attention
- Confirm an action
- Show system status
- Reduce perceived waiting time
- Make the interface feel responsive

Avoid animations that are purely decorative.

---

# Animation Duration Standards

| Type | Duration |
|--------|----------|
| Hover | 150ms |
| Button Click | 120ms |
| Card Hover | 250ms |
| Page Transition | 350ms |
| Modal | 300ms |
| Sidebar | 250ms |
| Toast | 300ms |
| Loading | Infinite |
| Success | 500ms |

---

# Animation Easing

```css
ease

ease-in-out

cubic-bezier(.22,.61,.36,1)
```

---

# 50. Page Transition Animations

Every page should animate when opened.

---

## Fade + Slide

```text
Opacity

0 → 1

+

TranslateY

20px → 0
```

Duration

```
350ms
```

---

## Scale Animation

```text
Scale

0.98

↓

1
```

Used for

- Dashboard
- Login
- Register

---

# 51. Navigation Animations

## Sidebar

Opening

```text
Slide Left

↓

Fade In
```

Closing

```text
Slide Right

↓

Fade Out
```

Duration

```
250ms
```

---

## Active Menu

When user changes page

```text
Blue Indicator

↓

Slides

↓

Menu Item Expands
```

---

# 52. Dashboard Animations

Dashboard should never appear instantly.

---

## Dashboard Cards

Cards appear one-by-one.

```text
Card 1

↓

Card 2

↓

Card 3

↓

Card 4
```

Delay

```
70ms
```

between cards.

---

## Counter Animation

Numbers animate

```
0

↓

145

↓

220

↓

Final Value
```

Duration

```
1 second
```

---

## Chart Animation

Charts

Grow

↓

Fade

↓

Labels Appear

---

## Recent Activity

Each activity slides upward.

```
Activity 1

↓

Activity 2

↓

Activity 3
```

---

# 53. Button Animations

Buttons should feel interactive.

---

## Hover

```css
transform:

translateY(-2px);

box-shadow:

0 12px 25px rgba(37,99,235,.25);
```

---

## Click

```css
transform:

scale(.97);
```

---

## Ripple Effect

Mouse Click

↓

Ripple Circle

↓

Fade

Duration

```
600ms
```

---

## Glow

Primary Button

Soft Blue Glow

---

# 54. Card Animations

Cards

Hover

↓

Lift

↓

Shadow

↓

Border Highlight

---

Transform

```css
translateY(-8px)

scale(1.02)
```

---

Glass Cards

Blur increases slightly.

---

AI Cards

Border glows using accent color.

---

# 55. Form Animations

Input Focus

Border

↓

Blue

↓

Glow

---

Label

Moves upward.

---

Validation Success

Green Check

Appears

---

Validation Error

Input shakes

↓

Red Border

↓

Error Message Slides Down

---

# 56. AI Processing Animation ⭐

Most important animation.

---

## AI Workflow

```text
Complaint Submitted

↓

Brain Icon Pulses

↓

Scanning Beam

↓

Processing Dots

↓

Classification Card

↓

Confidence Meter

↓

Department Card

↓

Success
```

---

## Brain Animation

```
Pulse

↓

Glow

↓

Rotate 3°

↓

Pulse
```

Infinite while processing.

---

## AI Progress

```
Analyzing Complaint...

██████████░░░░

75%
```

Animated Progress Bar

---

## Confidence Meter

Circular Gauge

```
96%
```

Animated from

```
0

↓

96
```

---

# 57. OCR Scanning Animation ⭐

During OCR

Show

```text
Document

↓

Blue Scan Line

↓

Progress Ring

↓

Extracted Text

↓

Entity Cards
```

---

## Scan Line

Moves

Top

↓

Bottom

↓

Repeats

---

## OCR Progress Ring

Animated Circular Progress

```
0%

↓

100%
```

---

## Extracted Text

Appears

Word

↓

Word

↓

Word

instead of entire paragraph.

---

# 58. Timeline Animation

Timeline appears

Event

↓

Event

↓

Event

↓

Event

Each with

- Fade
- Slide Left

Delay

```
100ms
```

---

# 59. Upload Animation

User Drags File

↓

Border Glows

↓

Upload Starts

↓

Progress Bar

↓

Success Checkmark

↓

File Card Appears

---

Drop Zone

Pulse

while dragging.

---

# 60. PDF Generation Animation

Generating PDF

```text
Paper

↓

Slides Up

↓

Printer Animation

↓

Checkmark

↓

Download Button
```

---

Progress

```
Generating PDF...

███████████░░░░

78%
```

---

# 61. Success Animation

Instead of

```
Saved Successfully
```

Show

```
✔

Scale

↓

Bounce

↓

Fade
```

---

Optional

Small Confetti

(only once)

---

Toast

Slides

↓

Top Right

↓

Auto Hide

---

# 62. Loading Animations

Never use

```
Loading...
```

Instead

---

## Skeleton Cards

```
██████████

██████

██████████
```

Shimmer Effect

---

## Skeleton Table

```
████████████████

████████████████

████████████████
```

---

## Skeleton Dashboard

Cards

Charts

Lists

Placeholders

---

# 63. Empty State Animation

Instead of empty pages

Show Illustration

↓

Floating Animation

↓

Friendly Message

↓

CTA Button

---

Example

```
📄

No Complaints Yet

Start by creating your first complaint.

[Create Complaint]
```

---

# 64. Error Animation

Network Error

```
⚠

Shake

↓

Retry Button

↓

Fade
```

---

Validation Error

```
Input

↓

Shake

↓

Red Border

↓

Message
```

---

# 65. Notification Animations

Toast

Slide

↓

Fade

↓

Disappear

---

Notification Bell

New Notification

↓

Bell Shake

↓

Badge Bounce

---

# 66. Theme Transition

When switching theme

```
Light

↓

Fade

↓

Dark
```

instead of instant switching.

---

Duration

```
300ms
```

---

# 67. Hover Effects

Images

Zoom

```
1

↓

1.05
```

---

Icons

Rotate

```
5°
```

---

Links

Underline grows from left.

---

# 68. Mobile Animations

Drawer

Slide Left

---

Cards

Fade Up

---

Buttons

Ripple

---

Bottom Navigation

Active Icon

↓

Bounce

↓

Glow

---

# 69. Performance Guidelines

To maintain 60 FPS:

✅ Use

- opacity
- transform
- scale
- translate

Avoid animating

- width
- height
- top
- left

Prefer CSS animations over JavaScript.

---

# 70. Motion Accessibility

Respect the user's operating system settings.

Use

```css
@media (prefers-reduced-motion: reduce)
```

In reduced motion mode:

- Disable continuous animations
- Remove parallax
- Shorten transitions
- Keep only essential feedback animations

---

# 71. Animation Checklist

## Page

- [ ] Fade In
- [ ] Slide Up

---

## Dashboard

- [ ] Counter Animation
- [ ] Card Reveal
- [ ] Chart Animation

---

## Forms

- [ ] Focus Animation
- [ ] Validation Animation

---

## AI

- [ ] Brain Animation
- [ ] Progress Ring
- [ ] Confidence Meter

---

## OCR

- [ ] Scan Line
- [ ] Text Reveal

---

## Upload

- [ ] Drag Highlight
- [ ] Upload Progress

---

## PDF

- [ ] Generation Animation
- [ ] Success Animation

---

## Notifications

- [ ] Toast
- [ ] Bell

---

## Loading

- [ ] Skeleton Screens
- [ ] Shimmer Effect

---

# Motion Design Summary

| Animation | Status |
|------------|--------|
| Page Transition | ✅ |
| Sidebar | ✅ |
| Dashboard | ✅ |
| Cards | ✅ |
| Buttons | ✅ |
| Forms | ✅ |
| AI Processing | ✅ |
| OCR Scanning | ✅ |
| Timeline | ✅ |
| Upload | ✅ |
| PDF Generation | ✅ |
| Loading | ✅ |
| Success | ✅ |
| Error | ✅ |
| Mobile | ✅ |
| Accessibility | ✅ |

---

## End of Part 4

**Next:** **Part 5 — Accessibility, Responsive Design, Dark Mode, Design QA Checklist & AI Coding Rules for Cursor, Claude Code, GitHub Copilot and Gemini CLI.** ⭐