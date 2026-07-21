# 03_Security_Access_Document.md

# Judiciary Flow

## Security & Access Control Document

**Version:** 1.0

**Project:** Judiciary Flow

**Document Type:** Security & Access Control

**Technology Stack**

- Python
- Flask
- MySQL
- JWT Authentication
- bcrypt
- HTML5
- CSS3
- JavaScript

**Status:** Draft

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | July 2026 | Initial Security Document |

---

# Table of Contents

1. Introduction
2. Security Objectives
3. Security Principles
4. Threat Model
5. Authentication
6. Authorization
7. User Roles
8. Session Management

---

# 1. Introduction

## Purpose

This document defines the security architecture and access control mechanisms for **Judiciary Flow**.

The objective is to protect:

- User Accounts
- Complaint Information
- Uploaded Evidence
- Generated Documents
- APIs
- Database

This document also serves as the implementation guide for developers during the hackathon.

---

## Scope

This document covers

- Authentication
- Authorization
- Access Control
- Password Security
- JWT Authentication
- API Security
- Secure File Upload
- Privacy
- Logging
- Security Testing

---

# 2. Security Objectives

The primary objectives are:

## Confidentiality

Only authorized users should access their own information.

---

## Integrity

User complaints and uploaded evidence must not be modified without authorization.

---

## Availability

The application should remain available during normal operation and recover gracefully from failures.

---

## Accountability

Important user actions should be logged for auditing and debugging.

---

## Privacy

Personal information should be stored securely and only used for the intended purpose.

---

# 3. Security Principles

Judiciary Flow follows these security principles.

## Principle 1

### Least Privilege

Every user receives only the permissions required to perform their actions.

---

## Principle 2

### Secure by Default

Sensitive operations require authentication.

---

## Principle 3

### Defense in Depth

Security is implemented at multiple layers:

- Frontend
- API
- Backend
- Database
- File Storage

---

## Principle 4

### Input Validation

Never trust user input.

All data must be validated on both the client and server.

---

## Principle 5

### Fail Securely

If an error occurs, the system should deny access rather than expose sensitive information.

---

# 4. Threat Model

The following threats have been considered during the design.

| Threat | Risk Level | Mitigation |
|---------|------------|------------|
| Unauthorized Login | High | JWT Authentication, bcrypt |
| SQL Injection | High | Parameterized Queries |
| Cross-Site Scripting (XSS) | Medium | Input Sanitization, Output Escaping |
| Cross-Site Request Forgery (CSRF) | Medium | CSRF Tokens |
| File Upload Abuse | High | File Validation |
| Broken Access Control | High | Ownership Checks |
| Password Theft | High | Password Hashing |
| Information Leakage | Medium | Generic Error Messages |

---

# 5. Authentication

## Overview

Authentication verifies the identity of users before granting access.

Judiciary Flow uses **JWT (JSON Web Token)** for stateless authentication.

---

## Authentication Flow

```text
User

↓

Login Form

↓

Credentials Validation

↓

Database Verification

↓

Password Verification

↓

JWT Generation

↓

Dashboard Access
```

---

## Login Process

### Step 1

User enters:

- Email
- Password

---

### Step 2

Backend validates:

- Email format
- Password presence

---

### Step 3

User record is retrieved from MySQL.

---

### Step 4

Password is verified using bcrypt.

---

### Step 5

If valid

Generate JWT Token.

---

### Step 6

Return

- Access Token
- User Information

---

## Registration Process

The registration process includes:

- Full Name
- Email
- Mobile Number
- Password

---

### Validation Rules

| Field | Rule |
|--------|------|
| Name | Required |
| Email | Must be unique |
| Mobile | 10 digits |
| Password | Minimum 8 characters |

---

## Authentication Rules

- Email addresses must be unique.
- Passwords are never stored in plain text.
- Tokens are issued only after successful authentication.
- Protected APIs require a valid JWT.

---

## Login Attempt Policy

To reduce brute-force attacks:

- Limit repeated failed login attempts.
- Introduce a temporary lockout after multiple failures.
- Log suspicious activity for review.

---

# 6. Authorization

## Overview

Authorization determines what an authenticated user is allowed to do.

Judiciary Flow follows **role-based access control (RBAC)**.

---

## Authorization Workflow

```text
User Request

↓

JWT Validation

↓

User Role Check

↓

Permission Check

↓

Allow or Deny Access
```

---

## Authorization Rules

Users may:

- View their own profile
- Create complaints
- Edit their own complaints
- Upload evidence for their complaints
- Download their generated documents

Users may **not**:

- Access another user's data
- Modify another user's complaints
- Delete another user's files
- View another user's documents

---

## Ownership Validation

Every protected resource must verify ownership before allowing access.

Example:

```
Complaint Owner == Logged-in User

YES → Allow

NO → Reject (403 Forbidden)
```

---

# 7. User Roles

The MVP includes two user roles.

---

## Role 1 – Citizen

Permissions

- Register
- Login
- Create Complaint
- Edit Complaint
- Upload Evidence
- Generate Documents
- Download Documents
- View Complaint History

Restrictions

- Cannot access other users' data.
- Cannot perform administrative actions.

---

## Role 2 – Administrator (Future)

Responsibilities

- Manage complaint templates
- Manage complaint categories
- Manage departments
- Review logs
- Monitor AI performance
- Manage users

This role is planned for future versions and is not included in the hackathon MVP.

---

# 8. Session Management

## Session Strategy

Judiciary Flow uses **JWT-based stateless sessions**.

This eliminates the need for server-side session storage.

---

## Token Lifecycle

```text
Login

↓

Generate JWT

↓

Store Token (Client)

↓

API Requests

↓

Validate Token

↓

Return Response

↓

Logout

↓

Discard Token
```

---

## Session Timeout

Recommended token expiration:

- Access Token: **60 minutes**
- Refresh Token: Future enhancement

---

## Logout

On logout:

- Remove JWT from the client.
- Redirect to the login page.
- Protected APIs become inaccessible without a valid token.

---

## Session Security Guidelines

- Use HTTPS in production.
- Do not expose tokens in URLs.
- Store tokens securely on the client.
- Validate the token on every protected request.

---

## End of Part 1

**Next:** **Part 2 — Password Security, JWT Implementation, API Security, SQL Injection Prevention, XSS Protection & CSRF Protection.**

# Part 2 — Password Security, JWT Implementation, API Security, SQL Injection Prevention, XSS Protection & CSRF Protection

---

# 9. Password Security

## Overview

Passwords are one of the most sensitive pieces of user data. Judiciary Flow follows industry best practices to ensure passwords are never stored or transmitted in plain text.

---

## Password Policy

| Rule | Requirement |
|------|-------------|
| Minimum Length | 8 Characters |
| Maximum Length | 64 Characters |
| Uppercase Letter | Recommended |
| Lowercase Letter | Required |
| Number | Required |
| Special Character | Recommended |

---

## Password Storage

Passwords are stored using:

- **bcrypt**

Example Workflow

```
User Password

↓

bcrypt Hashing

↓

Store Hash in Database
```

Example Stored Password

```
$2b$12$J2M3f7k0xG6.............
```

Passwords **cannot be decrypted**, only verified.

---

## Password Verification

```
User Login

↓

Entered Password

↓

bcrypt.compare()

↓

Match?

↓

Access Granted
```

---

## Password Security Rules

- Never store plain-text passwords.
- Never send passwords back in API responses.
- Never log passwords.
- Always hash passwords before database insertion.

---

# 10. JWT Authentication

## Overview

Judiciary Flow uses **JSON Web Tokens (JWT)** for secure, stateless authentication.

---

## JWT Structure

```
Header

↓

Payload

↓

Signature
```

---

## JWT Payload

Example

```json
{
    "user_id": 101,
    "email": "user@example.com",
    "role": "citizen",
    "exp": 1789123456
}
```

---

## Authentication Workflow

```text
User Login

↓

Validate Credentials

↓

Generate JWT

↓

Return Token

↓

Client Stores Token

↓

Include Token in API Request

↓

Backend Verifies Token

↓

Return Response
```

---

## Authorization Header

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Token Expiration

Recommended

| Token | Duration |
|---------|----------|
| Access Token | 60 Minutes |
| Refresh Token | Future Version |

---

## Invalid Token Response

```json
{
    "success": false,
    "message": "Invalid or expired token."
}
```

---

## Expired Token Handling

If token expires

```
401 Unauthorized

↓

Redirect to Login
```

---

# 11. API Security

## Overview

Every API endpoint must validate:

- Authentication
- Authorization
- Request Data
- Input Format

---

## API Security Flow

```text
API Request

↓

JWT Validation

↓

Permission Check

↓

Input Validation

↓

Business Logic

↓

Database

↓

JSON Response
```

---

## Public APIs

No authentication required.

Examples

- Login
- Register
- Home Page

---

## Protected APIs

Require JWT Authentication.

Examples

- Create Complaint
- Upload Evidence
- Generate Document
- Download PDF
- Dashboard

---

## API Response Format

Success

```json
{
    "success": true,
    "message": "Request successful.",
    "data": {}
}
```

---

Failure

```json
{
    "success": false,
    "message": "Unauthorized access."
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting (Recommended)

To reduce abuse:

- Limit login attempts.
- Limit API requests per minute.
- Return **429 Too Many Requests** when limits are exceeded.

---

# 12. SQL Injection Prevention

## Overview

SQL Injection is prevented by ensuring user input is never directly concatenated into SQL queries.

---

## Secure Database Access

Use:

- Parameterized Queries
- Prepared Statements

Example (Pseudo Code)

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

---

## Unsafe Example (Do Not Use)

```python
query = "SELECT * FROM users WHERE email='" + email + "'"
```

---

## Validation Rules

Validate:

- Email
- Complaint Title
- Description
- File Name
- Search Input

---

## Database Security Practices

- Validate all inputs.
- Use least-privilege database accounts.
- Do not expose database errors to users.

---

# 13. Cross-Site Scripting (XSS) Protection

## Overview

XSS attacks occur when malicious scripts are injected into user input and executed in another user's browser.

---

## Protection Strategy

- Escape HTML output.
- Sanitize user input.
- Validate form fields.
- Avoid rendering untrusted HTML.

---

## Safe Rendering

Instead of displaying raw user input:

```
<Complaint>

↓

Escape HTML

↓

Display Text
```

---

## Validation

Reject inputs containing:

- `<script>`
- Inline JavaScript
- Dangerous HTML attributes

---

## Additional Protection

- Content Security Policy (CSP)
- Secure HTTP Headers

---

# 14. Cross-Site Request Forgery (CSRF) Protection

## Overview

CSRF attacks trick authenticated users into submitting unwanted requests.

---

## Protection Mechanisms

- CSRF Tokens
- SameSite Cookies
- Origin Validation

---

## CSRF Workflow

```text
User Opens Form

↓

Server Generates CSRF Token

↓

User Submits Form

↓

Server Verifies Token

↓

Accept or Reject Request
```

---

## SameSite Cookies

Recommended Setting

```
SameSite=Lax
```

or

```
SameSite=Strict
```

---

## Secure Cookies

Enable

- HttpOnly
- Secure (HTTPS)
- SameSite

---

# 15. Security Headers

The application should return the following HTTP security headers.

| Header | Purpose |
|---------|----------|
| X-Frame-Options | Prevent Clickjacking |
| X-Content-Type-Options | Prevent MIME Sniffing |
| Referrer-Policy | Protect Referrer Information |
| Content-Security-Policy | Reduce XSS Risk |
| Strict-Transport-Security | Force HTTPS |

---

# 16. Secure Coding Guidelines

Developers should:

- Validate every input.
- Use parameterized SQL queries.
- Escape HTML before rendering.
- Never trust client-side validation alone.
- Keep secrets in environment variables.
- Use HTTPS in production.
- Log security events without exposing sensitive information.

---

## End of Part 2

**Next:** **Part 3 — File Upload Security, OCR Security, Data Privacy, Logging & Monitoring, Error Handling, Environment Variables & Secure Deployment.**



# Part 3 — File Upload Security, OCR Security, Data Privacy, Logging & Monitoring, Error Handling & Secure Configuration

---

# 17. File Upload Security

## Overview

The Evidence Upload module allows users to upload supporting files for complaint preparation. Since file uploads are one of the most common attack vectors, Judiciary Flow validates every uploaded file before it is stored or processed.

---

## Supported File Types

| Category | Extensions |
|----------|------------|
| Images | JPG, JPEG, PNG |
| Documents | PDF |
| Audio | MP3, WAV |

Any other file type is rejected.

---

## File Size Limits

| File Type | Maximum Size |
|------------|-------------|
| Image | 10 MB |
| PDF | 20 MB |
| Audio | 20 MB |

Maximum files per complaint:

```
10 Files
```

---

## Upload Validation Flow

```text
User Uploads File

↓

Check File Size

↓

Check Extension

↓

Check MIME Type

↓

Generate Unique Filename

↓

Store File

↓

Save Metadata

↓

OCR Processing (if supported)
```

---

## Allowed MIME Types

```
image/jpeg

image/png

application/pdf

audio/mpeg

audio/wav
```

---

## Rejected File Types

The system rejects files such as:

- EXE
- BAT
- CMD
- SH
- JS
- PHP
- ASP
- ZIP
- RAR
- DLL

---

## File Naming Strategy

Original filenames are never stored directly.

Example

Instead of

```
bill.pdf
```

Store

```
evidence_8fd34f9c2.pdf
```

Benefits:

- Prevents filename conflicts.
- Protects user privacy.
- Makes file enumeration difficult.

---

## Upload Directory Structure

```
uploads/

├── images/
├── pdf/
├── audio/
└── temp/
```

Directories should not be publicly accessible.

---

# 18. OCR Security

## Overview

Uploaded images and PDFs are processed using OCR.

Only trusted file types are sent to the OCR engine.

---

## OCR Workflow

```text
Uploaded File

↓

Validation

↓

OpenCV Image Processing

↓

Tesseract OCR

↓

Extracted Text

↓

Entity Extraction

↓

Database
```

---

## OCR Security Measures

Before OCR begins:

- Validate file type.
- Validate file size.
- Scan for corruption.
- Remove metadata (optional).
- Store temporary files securely.

---

## Temporary Files

OCR creates temporary files during processing.

Requirements

- Store in `/uploads/temp`
- Delete after processing
- Never expose temporary files

---

## OCR Failure Handling

If OCR fails:

- Notify the user.
- Allow manual editing.
- Keep the original uploaded file.

---

# 19. Data Privacy

## Overview

Judiciary Flow handles sensitive personal information such as complaint details and supporting evidence.

User data must be handled responsibly.

---

## Personally Identifiable Information (PII)

Examples:

- Full Name
- Email Address
- Mobile Number
- Complaint Description
- Uploaded Evidence

---

## Privacy Principles

- Collect only necessary information.
- Store data securely.
- Do not share user data with third parties.
- Allow users to delete their own complaints (future enhancement).

---

## Data Storage

Sensitive data stored in MySQL:

- User Accounts
- Complaint Records
- Evidence Metadata

Uploaded files stored separately from the database.

---

## Data Retention

For the Hackathon MVP:

- Data remains until manually removed.

Future versions may include:

- Automatic retention policies.
- User-controlled deletion.
- Archive functionality.

---

# 20. Logging & Monitoring

## Purpose

Logs help developers monitor system health, investigate issues, and detect suspicious activity.

Sensitive information must never be written to logs.

---

## Log Categories

### Authentication Logs

Record:

- Login Success
- Login Failure
- Logout
- Invalid Token

---

### Complaint Logs

Record:

- Complaint Created
- Complaint Updated
- Complaint Deleted

---

### Evidence Logs

Record:

- Upload Success
- Upload Failure
- OCR Started
- OCR Completed
- OCR Failed

---

### Document Logs

Record:

- PDF Generated
- Download Started
- Download Completed

---

### System Logs

Record:

- API Errors
- Database Errors
- Server Exceptions
- Unexpected Failures

---

## Do NOT Log

Never log:

- Passwords
- JWT Tokens
- OTPs
- Database Credentials
- API Secrets

---

## Sample Log Entry

```
[2026-07-21 14:32:15]

INFO

User ID: 105

Complaint Created

Complaint ID: CMP-1025
```

---

# 21. Error Handling

## Error Handling Principles

- Never expose stack traces.
- Display user-friendly messages.
- Log technical details internally.
- Return appropriate HTTP status codes.

---

## Common Errors

| Scenario | User Message |
|----------|--------------|
| Invalid Login | Incorrect email or password. |
| Invalid File | Unsupported file format. |
| File Too Large | File exceeds upload limit. |
| Database Error | Something went wrong. Please try again. |
| OCR Failure | Unable to process the uploaded file. |
| Invalid Token | Please log in again. |

---

## Error Response Format

```json
{
  "success": false,
  "message": "Unable to process your request.",
  "error_code": "OCR_001"
}
```

---

# 22. Environment Variables

Sensitive configuration must never be hardcoded.

Store secrets in a `.env` file.

---

## Required Variables

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

MYSQL_HOST=localhost

MYSQL_USER=root

MYSQL_PASSWORD=your_password

MYSQL_DB=judiciary_flow

MAIL_USERNAME=example@gmail.com

MAIL_PASSWORD=your_password
```

---

## Best Practices

- Do not commit `.env` to Git.
- Rotate secrets if compromised.
- Use different credentials for development and production.

---

# 23. Secure Deployment

## Production Checklist

Before deployment:

- Enable HTTPS.
- Disable Flask debug mode.
- Use secure environment variables.
- Configure proper file permissions.
- Restrict database access.
- Enable HTTP security headers.

---

## File Permissions

Recommendations:

- Upload folders: Read/Write by application only.
- Generated documents: Read-only after creation.
- Configuration files: Restricted access.

---

## Backup Strategy

Regularly back up:

- MySQL database.
- Uploaded evidence.
- Generated documents.

---

## Monitoring

Track:

- Server uptime.
- API response times.
- Storage usage.
- Failed login attempts.
- Error rates.

---

## End of Part 3

**Next:** **Part 4 — DPDP Act Considerations, Security Testing, Risk Assessment, Security Checklist, Future Improvements & Conclusion.**

# Part 4 — DPDP Act Considerations, Security Testing, Risk Assessment, Security Checklist & Conclusion

---

# 24. Digital Personal Data Protection (DPDP) Act Considerations

## Overview

Judiciary Flow processes personal information such as user profiles, complaint details, and uploaded evidence. The application should follow the core principles of India's **Digital Personal Data Protection (DPDP) Act, 2023**.

> **Note:** Judiciary Flow is a hackathon MVP and is not intended to provide legal compliance certification. Future production deployments should undergo a legal and security review.

---

## Personal Data Collected

### User Information

- Full Name
- Email Address
- Mobile Number

---

### Complaint Information

- Complaint Title
- Complaint Description
- State
- District
- Incident Date

---

### Uploaded Evidence

- Images
- PDFs
- Audio Files

---

## Privacy Principles

Judiciary Flow should:

- Collect only required information.
- Clearly explain why data is collected.
- Allow users to access their own information.
- Prevent unauthorized access.
- Secure stored data.
- Avoid collecting unnecessary personal information.

---

## User Consent

Before registration, users should agree to:

- Privacy Policy
- Terms of Service

Example

```
☑ I agree to the Privacy Policy and Terms of Service.
```

---

## Future Enhancements

- User Data Download
- Account Deletion
- Consent Withdrawal
- Data Export
- Data Retention Controls

---

# 25. Security Testing Strategy

Security testing should be performed throughout development.

---

## Authentication Testing

Verify

- User Registration
- Login
- Logout
- Invalid Password
- Expired JWT
- Unauthorized API Access

---

## Authorization Testing

Verify users cannot

- View another user's complaints.
- Download another user's documents.
- Delete another user's files.
- Access protected APIs without authentication.

---

## Input Validation Testing

Test

- Empty Fields
- Long Strings
- SQL Injection Payloads
- JavaScript Injection
- Invalid Email
- Invalid File Names

---

## File Upload Testing

Verify

- Invalid extensions rejected.
- Oversized files rejected.
- MIME type validation.
- Duplicate filenames handled correctly.
- Unsupported formats blocked.

---

## OCR Testing

Test

- Clear Images
- Blurry Images
- Rotated Images
- Multi-page PDFs
- Corrupted Files

---

## API Security Testing

Verify

- JWT validation
- Invalid tokens
- Missing tokens
- Expired tokens
- Unauthorized requests

---

## Database Testing

Verify

- Parameterized queries
- Foreign key integrity
- Unique constraints
- Input validation
- Data consistency

---

# 26. Security Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Weak Passwords | High | Password Policy + bcrypt |
| SQL Injection | High | Parameterized Queries |
| Unauthorized Access | High | JWT + Ownership Checks |
| XSS | Medium | Input Sanitization |
| CSRF | Medium | CSRF Tokens |
| File Upload Abuse | High | Validation + MIME Checks |
| OCR Failure | Medium | Manual Editing Option |
| Data Leakage | High | Secure Storage & Access Control |
| Token Theft | High | HTTPS + Token Expiration |
| Server Errors | Medium | Error Handling & Logging |

---

# 27. Security Checklist

## Authentication

- [ ] User Registration
- [ ] Login
- [ ] Logout
- [ ] JWT Authentication
- [ ] Token Expiration
- [ ] Password Hashing

---

## Authorization

- [ ] User Ownership Validation
- [ ] Protected APIs
- [ ] Role-Based Access
- [ ] Access Denied Handling

---

## Database

- [ ] Parameterized Queries
- [ ] Input Validation
- [ ] Foreign Keys
- [ ] Indexes
- [ ] Constraints

---

## File Upload

- [ ] File Extension Validation
- [ ] MIME Type Validation
- [ ] File Size Validation
- [ ] Unique File Names
- [ ] Secure Storage

---

## Frontend

- [ ] Form Validation
- [ ] XSS Prevention
- [ ] CSRF Protection
- [ ] HTTPS

---

## Backend

- [ ] Exception Handling
- [ ] Secure APIs
- [ ] Logging
- [ ] Environment Variables

---

## Deployment

- [ ] Debug Mode Disabled
- [ ] HTTPS Enabled
- [ ] Secure Headers
- [ ] Backup Strategy
- [ ] Monitoring Enabled

---

# 28. Future Security Improvements

The following enhancements are recommended after the hackathon MVP.

## Authentication

- Refresh Tokens
- Multi-Factor Authentication (MFA)
- Password Reset via Email

---

## Monitoring

- Intrusion Detection
- Failed Login Alerts
- Activity Dashboard

---

## File Security

- Malware Scanning
- Cloud Storage Encryption
- Automatic File Cleanup

---

## API Security

- Rate Limiting
- API Keys for External Integrations
- Request Signing

---

## Infrastructure

- Docker Deployment
- Reverse Proxy (Nginx)
- Web Application Firewall (WAF)

---

## Compliance

- Periodic Security Audits
- Privacy Impact Assessment
- Dependency Vulnerability Scans

---

# 29. Security Best Practices

Developers should always:

- Validate every user input.
- Use HTTPS in production.
- Keep dependencies updated.
- Never hardcode credentials.
- Store secrets in environment variables.
- Use secure password hashing.
- Log important security events.
- Avoid exposing internal server errors.
- Follow the principle of least privilege.
- Test security before deployment.

---

# 30. Conclusion

The security architecture of **Judiciary Flow** is designed to provide a strong foundation for a hackathon MVP while following modern web application security practices.

The platform implements:

- JWT-based authentication
- Role-based authorization
- Secure password hashing with bcrypt
- SQL injection prevention
- XSS and CSRF protection
- Secure file upload validation
- OCR processing safeguards
- Structured logging and monitoring
- Privacy-aware data handling

Although the project is intended for demonstration purposes, its architecture is designed to be extensible for production-ready security enhancements in future versions.

---

# Document Summary

**Document Name:** 03_Security_Access_Document.md

**Version:** 1.0

**Status:** Complete

**Purpose:** Defines the authentication model, authorization strategy, data protection mechanisms, secure coding practices, privacy considerations, and security testing approach for Judiciary Flow.

---

**End of Security & Access Control Document**