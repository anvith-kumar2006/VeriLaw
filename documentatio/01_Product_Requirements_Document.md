# 01_Product_Requirements_Document.md

# Judiciary Flow
## Product Requirements Document (PRD)

**Version:** 1.0

**Document Type:** Product Requirements Document

**Project Type:** AI-Powered Legal Assistance Platform

**Prepared For:** Hackathon MVP

**Technology Stack:**
- Python
- Flask
- Flask REST API
- HTML5
- CSS3
- Vanilla JavaScript
- MySQL
- Scikit-learn
- spaCy
- OpenCV
- Tesseract OCR

**Status:** Draft

---

# Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| 1.0 | July 2026 | Team Judiciary Flow | Initial PRD |

---

# Table of Contents

1. Executive Summary
2. Vision
3. Mission
4. Problem Statement
5. Objectives
6. Market Opportunity
7. Target Users
8. User Personas
9. User Journey
10. Business Goals
11. Success Metrics

---

# 1. Executive Summary

## Overview

Judiciary Flow is an AI-powered citizen assistance platform designed to simplify the legal complaint preparation process for Indian citizens.

Many citizens struggle to understand:

- Which government authority has jurisdiction over their issue.
- How to prepare a professional complaint.
- What supporting evidence is required.
- How to organize documents before submission.

Judiciary Flow addresses these challenges through an intelligent workflow that assists users in preparing complaint packages suitable for submission to the appropriate authority.

The platform focuses on providing **legal information and procedural guidance**. It does **not** provide legal advice or replace qualified legal professionals.

---

## Why Judiciary Flow?

Government grievance systems already exist.

However, they expect citizens to know:

- where to file,
- how to write,
- what documents to attach.

Most first-time users do not possess this knowledge.

Judiciary Flow bridges this gap by helping users prepare before interacting with government systems.

---

## Core Features

The Hackathon MVP focuses on three primary capabilities.

### AI Complaint Routing

Analyze a user's complaint description and recommend the most appropriate government authority.

---

### Smart Complaint Generator

Generate structured complaint documents using predefined templates.

---

### Evidence Organizer

Organize uploaded evidence into a structured timeline using OCR and entity extraction.

---

# 2. Vision

To make legal complaint preparation simple, accessible, and understandable for every citizen regardless of their legal knowledge or technical background.

Judiciary Flow aims to reduce procedural barriers by helping users prepare accurate and complete complaint packages before approaching government authorities.

---

# 3. Mission

Our mission is to build an intelligent digital assistant that helps citizens:

- understand complaint procedures,
- identify the appropriate authority,
- prepare professional complaint documents,
- organize supporting evidence,
- improve the quality of complaint submissions.

The platform empowers citizens while encouraging responsible use of official government grievance mechanisms.

---

# 4. Problem Statement

## Background

India offers multiple grievance redressal systems covering areas such as:

- Consumer protection
- Labour disputes
- Municipal services
- Cybercrime
- Women's safety
- RTI
- Banking
- Insurance
- Public grievances

Despite the availability of these systems, many complaints fail before reaching the correct authority.

---

## Current Challenges

### 1. Lack of Awareness

Many citizens do not know:

- where to file,
- which authority has jurisdiction,
- applicable legal provisions.

---

### 2. Poor Documentation

Complaints often contain:

- missing information,
- incorrect formatting,
- incomplete evidence,
- unclear descriptions.

---

### 3. Unorganized Evidence

Users frequently possess evidence such as:

- bills,
- screenshots,
- emails,
- photographs,
- audio recordings,

but struggle to organize them into a coherent sequence.

---

### 4. Digital Literacy

Government portals can be difficult for:

- senior citizens,
- first-time users,
- rural populations,
- individuals with limited technical experience.

---

### 5. Procedural Errors

Common mistakes include:

- filing in the wrong department,
- submitting incomplete complaints,
- attaching insufficient evidence,
- misunderstanding complaint requirements.

---

## Problem Statement

Citizens often face unnecessary delays because they lack guidance on:

- identifying the correct authority,
- preparing structured complaints,
- organizing evidence.

Judiciary Flow aims to reduce these procedural barriers through intelligent automation.

---

# 5. Objectives

The primary objectives of Judiciary Flow are:

### Objective 1

Help users identify the appropriate government authority.

---

### Objective 2

Simplify complaint drafting using structured templates.

---

### Objective 3

Improve evidence organization.

---

### Objective 4

Reduce complaint preparation time.

---

### Objective 5

Increase confidence in government grievance processes.

---

### Objective 6

Provide a user-friendly interface suitable for users with varying levels of digital literacy.

---

### Objective 7

Demonstrate a practical AI-powered solution within the scope of a hackathon MVP.

---

# 6. Market Opportunity

## Current Situation

India has a rapidly growing digital public infrastructure.

Citizens increasingly rely on online platforms for:

- grievance submission,
- public services,
- digital documentation,
- information access.

However, complaint preparation remains largely manual.

---

## Opportunity

Judiciary Flow fills a gap by assisting users **before** they interact with official systems.

The platform complements—not replaces—existing government services.

---

## Existing Platforms

| Platform | Primary Purpose |
|-----------|-----------------|
| CPGRAMS | Public grievance portal |
| National Consumer Helpline | Consumer complaints |
| DigiLocker | Digital document storage |
| UMANG | Government services |
| RTI Online | RTI applications |
| Cyber Crime Portal | Cybercrime reporting |
| eCourts | Court information |

Most of these systems expect users to already know the correct process.

Judiciary Flow focuses on helping users prepare for these interactions.

---

# 7. Target Users

## Primary Users

### Consumers

Individuals seeking assistance with consumer disputes.

---

### Employees

Workers facing issues related to wages, employment, or workplace rights.

---

### Tenants

Individuals involved in rental or housing disputes.

---

### Citizens

Users requiring assistance with:

- municipal complaints,
- public grievances,
- RTI applications,
- cybercrime reporting.

---

### Senior Citizens

Individuals requiring simplified digital assistance.

---

### Students

Users seeking guidance on legal complaint preparation.

---

## Secondary Users

- NGOs
- Legal aid organizations
- Community service centers
- Educational institutions

---

# 8. User Personas

## Persona 1

### Name

Rahul Sharma

### Age

27

### Occupation

Software Engineer

### Problem

Purchased an electronic appliance that stopped functioning shortly after purchase.

### Goals

- Obtain a replacement or refund.
- Identify the correct consumer authority.
- Generate a professional complaint.

### Pain Points

- Uncertain where to file.
- Limited legal knowledge.
- Unsure which documents are required.

---

## Persona 2

### Name

Priya Verma

### Age

34

### Occupation

Teacher

### Problem

Landlord refuses to return the security deposit.

### Goals

- Understand available complaint options.
- Prepare a structured complaint.
- Organize rental documents.

### Pain Points

- Multiple scattered documents.
- No legal drafting experience.

---

## Persona 3

### Name

Amit Kumar

### Age

41

### Occupation

Small Business Owner

### Problem

Experienced an online banking fraud.

### Goals

- Report the incident quickly.
- Preserve evidence.
- Prepare supporting documentation.

### Pain Points

- Large number of screenshots.
- Confusion regarding reporting channels.

---

# 9. User Journey

```
User Opens Website
        │
        ▼
Creates Account
        │
        ▼
Describes Complaint
        │
        ▼
AI Classifies Complaint
        │
        ▼
Recommended Authority
        │
        ▼
Uploads Evidence
        │
        ▼
OCR Processing
        │
        ▼
Evidence Organized
        │
        ▼
Complaint Generated
        │
        ▼
Downloads Complaint Package
```

---

# 10. Business Goals

The project aims to:

- Improve accessibility to complaint preparation.
- Reduce procedural mistakes.
- Demonstrate practical AI applications.
- Promote legal awareness.
- Showcase an end-to-end complaint preparation workflow suitable for hackathon evaluation.

---

# 11. Success Metrics

## Product Metrics

| Metric | Target |
|----------|---------|
| Complaint Classification Accuracy | ≥85% |
| OCR Accuracy | ≥80% |
| Complaint Generation Success | 100% |
| Average Processing Time | <5 seconds |
| PDF Generation Time | <3 seconds |

---

## User Experience Metrics

- Simple navigation.
- Responsive design.
- Mobile compatibility.
- Accessibility compliance.
- Clear validation messages.

---

## Technical Metrics

- Fast page loading.
- Secure authentication.
- Reliable file uploads.
- Stable API performance.
- Efficient database queries.

---

**End of Part 1**

**Next:** Part 2 — Functional Requirements, Non-Functional Requirements, User Stories, MVP Scope, Feature Overview, and Acceptance Criteria.


# Part 2 — Functional Requirements, Non-Functional Requirements, User Stories, MVP Scope & Acceptance Criteria

---

# 12. Functional Requirements

## 12.1 User Authentication

### Description

The system shall allow users to securely create and access their accounts.

### Functional Requirements

- User Registration
- User Login
- JWT Authentication
- Password Reset (Future)
- Logout
- Session Validation

### Acceptance Criteria

- User can register successfully.
- Duplicate email is rejected.
- Password is securely hashed.
- JWT token is generated after login.

---

## 12.2 Complaint Submission

### Description

Users should be able to describe their legal issue in simple English.

### Functional Requirements

- Complaint title
- Complaint description
- Complaint category (optional)
- Date of incident
- State
- District

### Validation Rules

| Field | Validation |
|---------|------------|
| Title | Required |
| Description | Minimum 30 characters |
| State | Required |
| District | Required |

### Acceptance Criteria

- Complaint is saved successfully.
- Validation errors are displayed.
- User cannot submit empty complaint.

---

## 12.3 Complaint Classification

### Description

The AI module analyzes complaint text and predicts the complaint category.

### Input

- Complaint Description

### Output

- Complaint Category
- Confidence Score
- Recommended Department
- Related Legal Information

### Acceptance Criteria

- Classification completes within 2 seconds.
- Confidence score is displayed.
- User receives recommendation.

---

## 12.4 Department Recommendation

### Description

Recommend the most suitable authority based on complaint type.

### Output Includes

- Department Name
- Department Description
- Reason for Recommendation
- Alternative Department (if available)

### Acceptance Criteria

- Recommendation displayed immediately.
- Alternative shown if confidence is low.

---

## 12.5 Complaint Generator

### Description

Generate a structured complaint document.

### Supported Formats

- PDF
- Printable HTML
- Email Draft

### Information Included

- User Information
- Complaint Details
- Authority Name
- Subject
- Complaint Body
- Supporting Evidence List

### Acceptance Criteria

- Document downloads successfully.
- Required sections are present.
- Template formatting remains consistent.

---

## 12.6 Evidence Upload

### Supported File Types

- JPG
- JPEG
- PNG
- PDF
- MP3
- WAV

### Maximum File Size

20 MB per file

### Features

- Multiple Upload
- Preview
- Delete
- Rename

### Acceptance Criteria

- Valid files upload successfully.
- Invalid formats rejected.
- Upload progress shown.

---

## 12.7 OCR Processing

### Description

Extract text from uploaded documents.

### Supported Sources

- Images
- PDFs

### OCR Engine

- Tesseract OCR

### Acceptance Criteria

- OCR completes automatically.
- Extracted text stored.
- OCR errors handled gracefully.

---

## 12.8 Evidence Organization

Automatically categorize evidence into:

- Bills
- Images
- Communication
- Audio
- Documents

### Acceptance Criteria

- Files categorized correctly.
- Timeline generated.
- Missing evidence suggestions displayed.

---

## 12.9 Dashboard

Dashboard displays

- Recent Complaints
- Generated Documents
- Uploaded Evidence
- AI Recommendations

---

# 13. Non-Functional Requirements

## Performance

| Requirement | Target |
|--------------|----------|
| Page Load | <2 seconds |
| API Response | <1 second |
| Classification | <2 seconds |
| OCR | <5 seconds |
| PDF Generation | <3 seconds |

---

## Reliability

- System uptime during demo
- Graceful error handling
- Input validation
- Automatic recovery from OCR failures

---

## Security

The application shall provide

- JWT Authentication
- Password Hashing
- SQL Injection Prevention
- XSS Protection
- CSRF Protection
- Secure File Uploads
- Role-based Authorization

---

## Scalability

The architecture should support

- Additional complaint categories
- Additional templates
- Multiple government departments
- Future AI models
- Mobile applications

---

## Accessibility

Frontend should support

- Mobile devices
- Screen readers
- Keyboard navigation
- High contrast
- Large buttons

---

## Maintainability

Code should

- Follow modular architecture
- Use reusable components
- Follow naming conventions
- Include documentation
- Support future enhancements

---

# 14. User Stories

---

## Epic 1 — Authentication

### US-001

**As a citizen**

I want to create an account

So that I can securely access my complaints.

---

### US-002

As a registered user

I want to log in

So that I can continue my work.

---

## Epic 2 — Complaint Routing

### US-003

As a citizen

I want to describe my issue

So that the AI recommends the correct department.

---

### US-004

As a citizen

I want to know why a department is recommended

So that I understand the process.

---

## Epic 3 — Complaint Generation

### US-005

As a user

I want the system to generate my complaint

So that I don't have to write legal documents manually.

---

### US-006

As a user

I want to download my complaint

So that I can print or submit it.

---

## Epic 4 — Evidence Management

### US-007

As a user

I want to upload documents

So that they are attached to my complaint.

---

### US-008

As a user

I want OCR to extract text

So that I don't have to manually enter information.

---

### US-009

As a user

I want evidence organized into a timeline

So that my complaint is easier to understand.

---

# 15. MVP Scope

The Hackathon MVP intentionally focuses on three core features.

---

## Included Features

### Authentication

- User Registration
- Login
- JWT Authentication

---

### AI Complaint Routing

- Complaint Classification
- Department Recommendation
- Confidence Score

---

### Complaint Generator

- Template Selection
- PDF Export
- Printable Version

---

### Evidence Organizer

- File Upload
- OCR
- Timeline Generation
- Evidence Categorization

---

### Dashboard

- Complaint History
- Document Downloads
- Uploaded Evidence

---

# 16. Out of Scope

The following features are not part of the Hackathon MVP.

- Voice Input
- Regional Languages
- Live Government API Integration
- Online Complaint Submission
- Advocate Marketplace
- Video Consultation
- Mobile Application
- Blockchain Evidence Verification
- Payment Gateway
- AI Chatbot
- Court Case Tracking

These may be considered for future releases.

---

# 17. Assumptions

- Users have internet access.
- Government departments continue existing complaint procedures.
- OCR quality depends on uploaded images.
- Users provide truthful information.
- Legal templates are reviewed before deployment.

---

# 18. Constraints

## Technical

- Flask Backend
- HTML/CSS/JavaScript Frontend
- MySQL Database
- No React
- No Django
- No FastAPI
- No Firebase
- No MongoDB

---

## Project

- Hackathon Timeline
- Limited Dataset
- Limited Compute Resources
- MVP-focused Implementation

---

# 19. Acceptance Criteria

The MVP will be considered complete if the following conditions are met.

| Feature | Acceptance Criteria |
|----------|---------------------|
| Registration | User can register successfully |
| Login | JWT authentication works |
| Complaint Submission | Complaint saved successfully |
| AI Classification | Category predicted successfully |
| Department Recommendation | Correct authority displayed |
| Complaint Generator | PDF generated successfully |
| OCR | Text extracted from uploaded images |
| Evidence Timeline | Evidence organized chronologically |
| Dashboard | User can view previous complaints |
| Security | Password hashing and JWT implemented |

---

# 20. Risks

| Risk | Impact | Mitigation |
|------|---------|------------|
| Low AI Accuracy | Wrong recommendations | Confidence score + fallback guidance |
| Poor OCR | Missing text | Manual editing option |
| Large File Uploads | Slow processing | File size limits |
| Invalid Inputs | Incorrect results | Strong validation |
| Template Errors | Incorrect documents | Pre-validated templates |

---

# 21. Dependencies

The project depends on:

### Backend

- Flask
- Flask REST API
- Flask-Mail
- bcrypt

### Database

- MySQL

### AI

- Scikit-learn
- Pandas
- NumPy
- spaCy
- OpenCV
- Tesseract OCR

### Document Generation

- ReportLab
- python-docx
- PyMuPDF

---

**End of Part 2**

**Next:** Part 3 — Detailed Feature Specifications, AI Workflow, Screen Flow, Process Flow, Business Rules, and Data Requirements.


# Part 3 — Detailed Feature Specifications, AI Workflow, Screen Flow, Business Rules & Data Requirements

---

# 22. Detailed Feature Specifications

This section describes each feature in detail, including user flow, system behavior, validations, inputs, outputs, and implementation notes.

---

# Feature 1 – User Authentication

## Purpose

Allow users to securely access their complaint history and generated documents.

---

## Features

- User Registration
- User Login
- JWT Authentication
- Logout

---

## Inputs

| Field | Required |
|---------|----------|
| Full Name | Yes |
| Email | Yes |
| Mobile Number | Yes |
| Password | Yes |

---

## Validation Rules

- Email must be unique.
- Password must contain at least 8 characters.
- Mobile number must contain exactly 10 digits.
- Required fields cannot be empty.

---

## Output

- User account created.
- JWT token generated.
- User redirected to Dashboard.

---

## Error Messages

- Email already exists.
- Invalid password.
- Invalid email format.
- Missing required fields.

---

# Feature 2 – Dashboard

## Purpose

Provide users with a centralized workspace.

---

## Dashboard Components

- Welcome Section
- Start New Complaint
- Previous Complaints
- Saved Documents
- Uploaded Evidence
- Profile Settings

---

## Dashboard Actions

- Create Complaint
- View Complaint
- Edit Complaint
- Download PDF
- Upload Evidence
- Delete Complaint

---

# Feature 3 – Complaint Submission

## Purpose

Collect complaint details in a structured format.

---

## Input Fields

| Field | Required |
|---------|----------|
| Complaint Title | Yes |
| Complaint Description | Yes |
| State | Yes |
| District | Yes |
| Incident Date | Optional |

---

## Workflow

User enters complaint details.

↓

System validates inputs.

↓

Complaint saved.

↓

AI classification begins.

---

## Validation

- Description minimum 30 characters.
- State required.
- District required.

---

# Feature 4 – AI Complaint Classification

## Purpose

Identify complaint category automatically.

---

## Input

Complaint Description

---

## Processing Pipeline

Complaint Text

↓

Text Cleaning

↓

Tokenization

↓

TF-IDF Vectorization

↓

Scikit-learn Classification Model

↓

Predicted Category

↓

Confidence Score

---

## Categories

- Consumer Complaint
- Labour Complaint
- Tenant Dispute
- Banking Complaint
- Insurance Complaint
- Cyber Crime
- Municipal Complaint
- RTI
- Property Dispute
- Women's Safety

---

## Output

| Field | Description |
|---------|-------------|
| Category | Complaint Type |
| Confidence | Prediction Score |
| Department | Recommended Authority |
| Legal Information | Relevant procedural information |

---

# Feature 5 – Department Recommendation

## Purpose

Recommend the most suitable authority.

---

## Inputs

- Complaint Category
- State
- District

---

## Outputs

- Department Name
- Department Description
- Why Recommended
- Alternative Department

---

## Example

Complaint

↓

Consumer Complaint

↓

District Consumer Commission

↓

Reason Displayed

↓

Alternative Authority

---

# Feature 6 – Smart Complaint Generator

## Purpose

Generate professionally formatted complaint documents.

---

## Input

- User Details
- Complaint Details
- Authority
- Evidence Summary

---

## Output Formats

- PDF
- HTML
- Printable Version

---

## Sections

- Sender Details
- Receiver Details
- Subject
- Complaint
- Facts
- Relief Requested
- Attached Evidence
- Signature

---

## Templates

- Consumer Complaint
- Labour Complaint
- Tenant Complaint
- RTI
- FIR
- Cyber Crime
- Banking
- Insurance
- Municipal Complaint
- Property Complaint

---

# Feature 7 – Evidence Upload

## Purpose

Allow users to upload supporting evidence.

---

## Supported Formats

Images

- JPG
- PNG
- JPEG

Documents

- PDF

Audio

- MP3
- WAV

---

## Maximum File Size

20 MB

---

## Multiple Upload

Supported

---

## Preview

Supported

---

## Delete

Supported

---

# Feature 8 – OCR Module

## Purpose

Extract text automatically.

---

## OCR Pipeline

Image

↓

OpenCV Enhancement

↓

Noise Removal

↓

Thresholding

↓

Tesseract OCR

↓

Extracted Text

↓

Database

---

## OCR Output

- Names
- Dates
- Amounts
- Addresses
- Organizations

---

# Feature 9 – Evidence Categorization

## Categories

- Bills
- Receipts
- Images
- Audio
- Documents
- Communication

---

## Workflow

Upload

↓

OCR

↓

Entity Extraction

↓

Category Prediction

↓

Timeline Generation

---

# Feature 10 – Evidence Timeline

## Purpose

Present uploaded evidence chronologically.

---

## Timeline Example

01 Jan 2026

Rent Agreement

↓

10 Jan 2026

Security Deposit Receipt

↓

18 Jan 2026

WhatsApp Conversation

↓

20 Jan 2026

Property Photos

↓

25 Jan 2026

Final Notice

---

# Feature 11 – PDF Export

## Output Includes

- Complaint
- User Information
- Authority
- Evidence Summary
- Timeline
- Date
- Signature Section

---

# 23. AI Workflow

## AI Modules

### Module 1

Complaint Classification

Technology

- TF-IDF
- Scikit-learn

---

### Module 2

OCR

Technology

- OpenCV
- Tesseract

---

### Module 3

Entity Extraction

Technology

- spaCy
- Regular Expressions

Extract

- Names
- Dates
- Money
- Addresses
- Organizations

---

### Module 4

Evidence Categorization

Uses

- OCR Results
- File Metadata
- Keywords

---

### AI Pipeline

User Complaint

↓

Text Cleaning

↓

Vectorization

↓

Classification

↓

Department Recommendation

↓

Complaint Generation

↓

Evidence Upload

↓

OCR

↓

Entity Extraction

↓

Timeline

↓

Final Complaint Package

---

# 24. Screen Flow

```

Landing Page

↓

Login / Register

↓

Dashboard

↓

New Complaint

↓

AI Classification

↓

Department Recommendation

↓

Upload Evidence

↓

OCR Processing

↓

Generate Complaint

↓

Download PDF

```

---

# 25. Business Rules

## Authentication

- Every complaint belongs to one user.
- Guest users cannot create complaints.

---

## Complaint Rules

- Complaint description is mandatory.
- Empty complaints are not allowed.

---

## AI Rules

- Confidence score must be displayed.
- If confidence < 60%, recommend manual verification.

---

## Evidence Rules

- File size must not exceed 20 MB.
- Unsupported file formats rejected.
- OCR only for Images and PDFs.

---

## PDF Rules

Generated complaint must always include:

- Date
- Subject
- Complaint Body
- Signature Section

---

# 26. Data Requirements

## User Data

- Name
- Email
- Mobile
- Password (Hashed)

---

## Complaint Data

- Complaint ID
- User ID
- Title
- Description
- Category
- Department
- Status
- Created Date

---

## Evidence Data

- Evidence ID
- Complaint ID
- File Name
- File Type
- OCR Text
- Category
- Upload Date

---

## Generated Document

- Document ID
- Complaint ID
- File Path
- Generated Date

---

# 27. Error Handling

| Scenario | System Response |
|-----------|----------------|
| Empty Complaint | Validation Error |
| Invalid Login | Authentication Failed |
| Unsupported File | Upload Rejected |
| OCR Failure | Allow Manual Entry |
| AI Prediction Failure | Ask User to Select Category |
| Database Error | Generic Error Message |

---

# 28. Logging Requirements

The system shall log:

- User Login
- Complaint Creation
- File Upload
- OCR Processing
- AI Prediction
- PDF Generation
- Authentication Failures
- System Errors

---

# 29. Performance Goals

| Module | Target |
|----------|--------|
| Login | <1 sec |
| Dashboard | <2 sec |
| Complaint Classification | <2 sec |
| OCR | <5 sec |
| PDF Generation | <3 sec |
| Evidence Upload | <5 sec |

---

## End of Part 3

**Next:** **Part 4 — Database Requirements, API Overview, Security Requirements, Deployment Plan, Testing Strategy, Future Roadmap, Appendix & Final Approval Checklist.**


# Part 4 — Database Requirements, API Overview, Security Requirements, Deployment Plan, Testing Strategy, Future Roadmap & Appendix

---

# 30. Database Requirements

The application uses **MySQL** as the primary relational database.

## Database Goals

- Store user information securely.
- Maintain complaint records.
- Store uploaded evidence metadata.
- Track generated complaint documents.
- Support future scalability.

---

## Core Database Tables

| Table | Description |
|---------|-------------|
| users | User accounts |
| complaints | Complaint records |
| departments | Government authorities |
| complaint_categories | Complaint types |
| evidence | Uploaded files |
| generated_documents | Generated complaint PDFs |
| activity_logs | User activity logs |

---

## Entity Relationship

```
User
 │
 ├──────────────┐
 │              │
 ▼              ▼
Complaints   Activity Logs
 │
 ├──────────────┐
 │              │
 ▼              ▼
Evidence    Generated Documents
 │
 ▼
Complaint Category
 │
 ▼
Department
```

---

## Primary Keys

| Table | Primary Key |
|---------|-------------|
| users | user_id |
| complaints | complaint_id |
| departments | department_id |
| evidence | evidence_id |
| generated_documents | document_id |

---

## Foreign Keys

| Child Table | Parent Table |
|-------------|--------------|
| complaints | users |
| complaints | complaint_categories |
| complaints | departments |
| evidence | complaints |
| generated_documents | complaints |

---

## Database Constraints

- Email must be unique.
- Complaint must belong to a valid user.
- Evidence must belong to an existing complaint.
- Generated document must belong to an existing complaint.
- Cascade delete disabled to prevent accidental data loss.

---

## Indexes

Create indexes on:

- Email
- Complaint Category
- Complaint Status
- Department
- Upload Date

---

# 31. API Overview

The backend follows RESTful API principles.

Base URL

```
/api/v1/
```

---

## Authentication APIs

### Register

```
POST /auth/register
```

---

### Login

```
POST /auth/login
```

---

### Logout

```
POST /auth/logout
```

---

## Complaint APIs

### Create Complaint

```
POST /complaints
```

---

### Get Complaints

```
GET /complaints
```

---

### Get Complaint

```
GET /complaints/{id}
```

---

### Update Complaint

```
PUT /complaints/{id}
```

---

### Delete Complaint

```
DELETE /complaints/{id}
```

---

## AI APIs

### Classify Complaint

```
POST /ai/classify
```

---

### Department Recommendation

```
POST /ai/recommend
```

---

### OCR Processing

```
POST /ocr/extract
```

---

### Timeline Generation

```
POST /timeline/generate
```

---

## Document APIs

Generate Complaint

```
POST /documents/generate
```

Download PDF

```
GET /documents/{id}
```

---

## Evidence APIs

Upload Evidence

```
POST /evidence/upload
```

List Evidence

```
GET /evidence/{complaint_id}
```

Delete Evidence

```
DELETE /evidence/{id}
```

---

# 32. Security Requirements

## Authentication

- JWT Authentication
- Secure Session Management
- Token Expiration
- Refresh Tokens (Future)

---

## Authorization

Users can only:

- View their own complaints.
- Upload their own evidence.
- Download their own documents.
- Delete their own records.

---

## Password Security

Passwords must:

- Be hashed using bcrypt.
- Never be stored in plain text.
- Never be returned by APIs.

---

## Input Validation

Validate:

- Email
- Password
- Complaint text
- Uploaded files
- File names
- MIME types

---

## SQL Injection Prevention

Use:

- Parameterized Queries
- SQLAlchemy ORM (or parameterized MySQL connector)
- Input Sanitization

---

## Cross-Site Scripting (XSS)

Prevent by:

- Escaping HTML output
- Sanitizing user input
- Content Security Policy (Future)

---

## CSRF Protection

- CSRF Tokens
- SameSite Cookies

---

## File Upload Security

Allowed Types

- JPG
- JPEG
- PNG
- PDF
- MP3
- WAV

Maximum Size

20 MB

Reject

- Executables
- Scripts
- ZIP files
- Unknown formats

---

## Logging

Log:

- Login attempts
- Failed authentication
- File uploads
- AI requests
- Errors
- PDF generation

---

## Privacy

User data must:

- Remain confidential.
- Be accessible only by the owner.
- Not be shared with third parties.

---

## Legal Notice

Judiciary Flow provides:

- Legal information
- Complaint preparation assistance

It does **not** provide legal advice.

---

# 33. Deployment Plan

## Development Environment

- VS Code
- Python
- Flask
- MySQL
- Git

---

## Version Control

GitHub Repository

```
Judiciary-Flow
```

---

## Future Deployment

Backend

- Render
- Railway

Frontend

- Netlify

Database

- MySQL

---

## Environment Variables

```
SECRET_KEY

JWT_SECRET_KEY

MYSQL_HOST

MYSQL_USER

MYSQL_PASSWORD

MYSQL_DB

MAIL_USERNAME

MAIL_PASSWORD
```

---

# 34. Testing Strategy

## Unit Testing

Test

- Authentication
- Complaint APIs
- OCR
- AI Module
- PDF Generation

---

## Integration Testing

Test

- Login → Dashboard
- Complaint → AI
- AI → Document Generator
- Upload → OCR
- OCR → Timeline

---

## System Testing

Verify:

- Complete workflow.
- Performance.
- Reliability.
- Stability.

---

## Security Testing

- SQL Injection
- XSS
- JWT Authentication
- Unauthorized Access
- File Upload Validation

---

## Manual Testing

Test:

- Registration
- Login
- Complaint Submission
- AI Recommendation
- Evidence Upload
- OCR
- PDF Download

---

## Sample Test Cases

| ID | Test Case | Expected Result |
|----|-----------|-----------------|
| TC-001 | Register User | Success |
| TC-002 | Login | JWT Generated |
| TC-003 | Submit Complaint | Complaint Saved |
| TC-004 | AI Classification | Category Returned |
| TC-005 | Upload Image | Success |
| TC-006 | OCR Extraction | Text Extracted |
| TC-007 | Generate PDF | PDF Downloaded |
| TC-008 | Invalid Login | Error Message |
| TC-009 | Invalid File Upload | Upload Rejected |
| TC-010 | Unauthorized Access | Access Denied |

---

# 35. Future Roadmap

## Phase 1 (Hackathon MVP)

- User Authentication
- Complaint Routing
- Complaint Generator
- Evidence Organizer
- OCR
- Timeline
- Dashboard

---

## Phase 2

- Multilingual Support
- Voice-to-Text
- Additional Complaint Templates
- Government Office Directory
- Complaint Status Tracking

---

## Phase 3

- Government Portal Integration
- AI Chat Assistant
- Mobile Application
- Digital Signature
- Lawyer Directory

---

## Phase 4

- Analytics Dashboard
- Admin Panel
- AI Model Improvements
- Regional Language OCR
- Cloud Storage Integration

---

# 36. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low AI Accuracy | Incorrect recommendation | Show confidence score and allow manual category selection |
| OCR Failure | Missing extracted information | Allow users to edit extracted text manually |
| Poor Internet Connection | Interrupted uploads | Retry upload and display progress |
| Invalid User Input | Processing errors | Strong frontend and backend validation |
| Large Files | Slow response | File size limits and compression |
| Server Failure | Downtime | Error handling and backup deployment plan |

---

# 37. Success Criteria

The MVP will be considered successful if:

- Users can register and log in securely.
- Complaint classification works reliably.
- Department recommendations are generated.
- Complaint PDFs are created successfully.
- OCR extracts usable text.
- Evidence is organized into a timeline.
- The complete workflow finishes within a few minutes during the demo.

---

# 38. References

### Government Platforms

- CPGRAMS
- National Consumer Helpline
- eCourts
- DigiLocker
- UMANG
- RTI Online
- National Cyber Crime Reporting Portal

### Technologies

- Flask
- MySQL
- Scikit-learn
- spaCy
- OpenCV
- Tesseract OCR
- ReportLab

---

# 39. Appendix

## Glossary

| Term | Meaning |
|------|---------|
| OCR | Optical Character Recognition |
| JWT | JSON Web Token |
| REST API | Representational State Transfer API |
| PDF | Portable Document Format |
| NLP | Natural Language Processing |
| TF-IDF | Term Frequency–Inverse Document Frequency |

---

## Project Summary

**Project Name:** Judiciary Flow

**Category:** AI-Powered Citizen Complaint Routing & Legal Document Generator

**Technology Stack:**

- Python
- Flask
- HTML5
- CSS3
- Vanilla JavaScript
- MySQL
- Scikit-learn
- spaCy
- OpenCV
- Tesseract OCR

---

## Conclusion

Judiciary Flow aims to simplify legal complaint preparation by helping citizens identify the correct authority, generate structured complaint documents, and organize supporting evidence. By focusing on a practical three-step workflow—complaint routing, document generation, and evidence organization—the project delivers a realistic, impactful, and technically achievable hackathon MVP while remaining extensible for future enhancements.

---

**End of Product Requirements Document (PRD)**