# 07_API_Documentation.md

# Judiciary Flow

## REST API Documentation

**Version:** 1.0

**Project:** Judiciary Flow

**Document Type:** API Documentation

**API Style:** REST API

**Authentication:** JWT (JSON Web Token)

**Response Format:** JSON

**Status:** Draft

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | July 2026 | Initial API Documentation |

---

# Table of Contents

1. Introduction
2. API Design Principles
3. Base URL
4. API Versioning
5. Authentication
6. Standard Request Format
7. Standard Response Format
8. HTTP Status Codes
9. Error Codes
10. Authentication APIs

---

# 1. Introduction

## Purpose

This document defines every REST API used by Judiciary Flow.

It serves as the implementation guide for:

- Backend Developers
- Frontend Developers
- Mobile Developers (Future)
- AI Coding Agents
- QA Engineers

---

## API Architecture

```
Frontend

↓

REST API

↓

Flask Backend

↓

Service Layer

↓

MySQL Database

↓

JSON Response
```

---

# 2. API Design Principles

Judiciary Flow follows RESTful API standards.

### Principles

- Stateless APIs
- JSON Request & Response
- JWT Authentication
- Consistent URL Naming
- Proper HTTP Methods
- Standard Error Responses

---

## URL Naming Convention

Use lowercase with hyphens.

Example

```
/api/v1/complaints

/api/v1/evidence/upload

/api/v1/auth/login
```

---

## HTTP Methods

| Method | Purpose |
|----------|----------|
| GET | Retrieve Data |
| POST | Create Data |
| PUT | Update Data |
| DELETE | Remove Data |

---

# 3. Base URL

## Development

```
http://localhost:5000/api/v1
```

---

## Production (Example)

```
https://api.judiciaryflow.com/api/v1
```

---

# 4. API Versioning

Current Version

```
v1
```

Example

```
/api/v1/auth/login

/api/v1/complaints
```

Future

```
/api/v2/
```

---

# 5. Authentication

Judiciary Flow uses **JWT Authentication**.

---

## Authentication Flow

```
Register

↓

Login

↓

JWT Token Generated

↓

Store Token

↓

Send Token with Every Request

↓

Access Protected APIs
```

---

## Authorization Header

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Protected APIs

Require JWT

- Dashboard
- Complaint APIs
- Upload APIs
- OCR APIs
- Document APIs
- Profile APIs

---

## Public APIs

No Authentication Required

- Register
- Login
- Health Check

---

# 6. Standard Request Format

## GET Request

```
GET

/api/v1/profile
```

---

## POST Request

Example

```json
{
    "title":"Complaint Title",

    "description":"Complaint Description"
}
```

---

## PUT Request

```json
{
    "full_name":"John Doe"
}
```

---

## DELETE Request

```
DELETE

/api/v1/complaints/15
```

---

# 7. Standard Response Format

## Success Response

```json
{
    "success": true,

    "message": "Operation completed successfully.",

    "data": {}
}
```

---

## Error Response

```json
{
    "success": false,

    "message": "Validation failed.",

    "errors": {}
}
```

---

## Pagination Response

```json
{
    "success": true,

    "page":1,

    "page_size":10,

    "total_records":55,

    "data":[]
}
```

---

# 8. HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Failed |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

# 9. Error Codes

| Error Code | Description |
|------------|-------------|
| AUTH001 | Invalid Credentials |
| AUTH002 | Token Expired |
| AUTH003 | Unauthorized |
| USER001 | Email Already Exists |
| USER002 | Invalid Mobile Number |
| CMP001 | Complaint Not Found |
| CMP002 | Invalid Complaint Data |
| FILE001 | Unsupported File Type |
| FILE002 | File Too Large |
| OCR001 | OCR Failed |
| DOC001 | PDF Generation Failed |
| SYS001 | Internal Server Error |

---

# 10. Authentication APIs

---

# API-001 — User Registration

## Endpoint

```
POST

/api/v1/auth/register
```

---

## Description

Registers a new user.

---

## Authentication

Not Required

---

## Request Body

```json
{
    "full_name":"John Doe",

    "email":"john@example.com",

    "mobile":"9876543210",

    "password":"Password123"
}
```

---

## Validation Rules

| Field | Rule |
|--------|------|
| Full Name | Required |
| Email | Valid + Unique |
| Mobile | 10 Digits |
| Password | Minimum 8 Characters |

---

## Success Response

**HTTP 201**

```json
{
    "success":true,

    "message":"Registration successful."
}
```

---

## Error Response

```json
{
    "success":false,

    "message":"Email already exists."
}
```

---

# API-002 — User Login

## Endpoint

```
POST

/api/v1/auth/login
```

---

## Description

Authenticates a user and returns a JWT.

---

## Authentication

Not Required

---

## Request Body

```json
{
    "email":"john@example.com",

    "password":"Password123"
}
```

---

## Success Response

**HTTP 200**

```json
{
    "success":true,

    "token":"JWT_TOKEN",

    "user":{

        "user_id":1,

        "full_name":"John Doe",

        "role":"citizen"

    }
}
```

---

## Error Response

```json
{
    "success":false,

    "message":"Invalid email or password."
}
```

---

# API-003 — Logout

## Endpoint

```
POST

/api/v1/auth/logout
```

---

## Authentication

JWT Required

---

## Description

Logs out the current user.

---

## Success Response

```json
{
    "success":true,

    "message":"Logout successful."
}
```

---

# API-004 — Get User Profile

## Endpoint

```
GET

/api/v1/profile
```

---

## Authentication

JWT Required

---

## Success Response

```json
{
    "success":true,

    "data":{

        "user_id":1,

        "full_name":"John Doe",

        "email":"john@example.com",

        "mobile":"9876543210"

    }
}
```

---

# API-005 — Update User Profile

## Endpoint

```
PUT

/api/v1/profile
```

---

## Authentication

JWT Required

---

## Request Body

```json
{
    "full_name":"John Doe",

    "mobile":"9876543210"
}
```

---

## Success Response

```json
{
    "success":true,

    "message":"Profile updated successfully."
}
```

---

## Validation Rules

| Field | Rule |
|--------|------|
| Full Name | Required |
| Mobile | 10 Digits |

---

## Authentication Summary

| API | Method | JWT |
|------|--------|-----|
| Register | POST | ❌ |
| Login | POST | ❌ |
| Logout | POST | ✅ |
| Get Profile | GET | ✅ |
| Update Profile | PUT | ✅ |

---

## End of Part 1

**Next:** **Part 2 — Complaint APIs, Categories API, Department API, AI Classification API, Department Recommendation API, Complaint History, Update/Delete Complaint APIs.**

# Part 2 — Complaint APIs, AI Classification & Department Recommendation

---

# 11. Complaint APIs

---

# API-101 — Create Complaint

## Endpoint

```http
POST /api/v1/complaints
```

---

## Description

Creates a new complaint submitted by the authenticated user.

---

## Authentication

✅ JWT Required

---

## Request Body

```json
{
    "title": "Faulty Mobile Phone",

    "description": "I purchased a mobile phone that stopped working within one week and the seller refused replacement.",

    "state": "Gujarat",

    "district": "Ahmedabad",

    "incident_date": "2026-07-15"
}
```

---

## Validation Rules

| Field | Rule |
|--------|------|
| title | Required, Max 200 characters |
| description | Required, Minimum 30 characters |
| state | Required |
| district | Required |
| incident_date | Valid Date |

---

## Success Response

**HTTP 201**

```json
{
    "success": true,

    "message": "Complaint created successfully.",

    "data": {

        "complaint_id": 101,

        "status": "Draft"

    }
}
```

---

## Error Response

```json
{
    "success": false,

    "message": "Validation failed."
}
```

---

# API-102 — Get Complaint

## Endpoint

```http
GET /api/v1/complaints/{complaint_id}
```

---

## Authentication

✅ JWT Required

---

## Description

Returns complete complaint information.

---

## Success Response

```json
{
    "success": true,

    "data": {

        "complaint_id": 101,

        "title": "Faulty Mobile Phone",

        "description": "...",

        "category": "Consumer Complaint",

        "department": "Consumer Commission",

        "status": "Processing"
    }
}
```

---

## Error Response

```json
{
    "success": false,

    "message": "Complaint not found."
}
```

---

# API-103 — Update Complaint

## Endpoint

```http
PUT /api/v1/complaints/{complaint_id}
```

---

## Authentication

✅ JWT Required

---

## Request Body

```json
{
    "title": "Updated Complaint",

    "description": "Updated complaint description.",

    "state": "Gujarat",

    "district": "Ahmedabad"
}
```

---

## Success Response

```json
{
    "success": true,

    "message": "Complaint updated successfully."
}
```

---

# API-104 — Delete Complaint

## Endpoint

```http
DELETE /api/v1/complaints/{complaint_id}
```

---

## Authentication

✅ JWT Required

---

## Success Response

```json
{
    "success": true,

    "message": "Complaint deleted successfully."
}
```

---

# API-105 — Complaint History

## Endpoint

```http
GET /api/v1/complaints
```

---

## Authentication

✅ JWT Required

---

## Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| page | No | Page Number |
| limit | No | Records Per Page |
| status | No | Filter by Status |
| category | No | Filter by Category |

---

## Example

```http
GET /api/v1/complaints?page=1&limit=10
```

---

## Success Response

```json
{
    "success": true,

    "page": 1,

    "total_records": 20,

    "data": [

        {

            "complaint_id": 101,

            "title": "Faulty Mobile",

            "status": "Completed"

        }

    ]
}
```

---

# 12. Complaint Categories API

---

# API-106 — Get Categories

## Endpoint

```http
GET /api/v1/categories
```

---

## Authentication

❌ Not Required

---

## Success Response

```json
{
    "success": true,

    "data": [

        {

            "category_id": 1,

            "category_name": "Consumer Complaint"

        },

        {

            "category_id": 2,

            "category_name": "Labour Complaint"

        }

    ]
}
```

---

# 13. Department APIs

---

# API-107 — Get Departments

## Endpoint

```http
GET /api/v1/departments
```

---

## Authentication

❌ Not Required

---

## Success Response

```json
{
    "success": true,

    "data": [

        {

            "department_id": 1,

            "department_name": "Consumer Commission"

        },

        {

            "department_id": 2,

            "department_name": "Cyber Crime Cell"

        }

    ]
}
```

---

# API-108 — Get Department Details

## Endpoint

```http
GET /api/v1/departments/{department_id}
```

---

## Authentication

❌ Not Required

---

## Success Response

```json
{
    "success": true,

    "data": {

        "department_name": "Consumer Commission",

        "website": "https://example.gov.in",

        "helpline": "1800-111-222",

        "email": "support@example.gov.in"

    }
}
```

---

# 14. AI APIs

---

# API-201 — Complaint Classification

## Endpoint

```http
POST /api/v1/ai/classify
```

---

## Authentication

✅ JWT Required

---

## Description

Uses the trained machine learning model to classify the complaint.

---

## Request Body

```json
{
    "description":"The seller refused to replace my damaged product."
}
```

---

## Processing Pipeline

```
Complaint

↓

Text Cleaning

↓

TF-IDF

↓

Logistic Regression

↓

Prediction
```

---

## Success Response

```json
{
    "success": true,

    "data": {

        "category": "Consumer Complaint",

        "confidence": 94.62
    }
}
```

---

## Error Response

```json
{
    "success": false,

    "message": "Unable to classify complaint."
}
```

---

# API-202 — Department Recommendation

## Endpoint

```http
POST /api/v1/ai/recommend
```

---

## Authentication

✅ JWT Required

---

## Description

Returns the recommended government department based on complaint category.

---

## Request Body

```json
{
    "category":"Consumer Complaint"
}
```

---

## Success Response

```json
{
    "success": true,

    "data": {

        "department": "Consumer Commission",

        "reason": "Consumer disputes are handled by the Consumer Commission.",

        "confidence": 95.80
    }
}
```

---

# API-203 — Manual Category Override

## Endpoint

```http
PUT /api/v1/complaints/{complaint_id}/category
```

---

## Authentication

✅ JWT Required

---

## Description

Allows users to manually select a complaint category if the AI prediction is incorrect.

---

## Request Body

```json
{
    "category_id": 3
}
```

---

## Success Response

```json
{
    "success": true,

    "message": "Complaint category updated successfully."
}
```

---

# Complaint API Summary

| API | Method | JWT |
|------|--------|-----|
| Create Complaint | POST | ✅ |
| Get Complaint | GET | ✅ |
| Update Complaint | PUT | ✅ |
| Delete Complaint | DELETE | ✅ |
| Complaint History | GET | ✅ |
| Get Categories | GET | ❌ |
| Get Departments | GET | ❌ |
| Department Details | GET | ❌ |
| AI Classification | POST | ✅ |
| Department Recommendation | POST | ✅ |
| Manual Category Override | PUT | ✅ |

---

## End of Part 2

**Next:** **Part 3 — Evidence Upload APIs, OCR APIs, Entity Extraction APIs, Timeline APIs, PDF Generation APIs, Download APIs & Document History APIs.**

# Part 3 — Evidence APIs, OCR APIs, Timeline APIs & Document Generation APIs

---

# 15. Evidence Management APIs

---

# API-301 — Upload Evidence

## Endpoint

```http
POST /api/v1/evidence/upload
```

---

## Description

Uploads one or more supporting evidence files for a complaint.

---

## Authentication

✅ JWT Required

---

## Content Type

```
multipart/form-data
```

---

## Request Parameters

| Field | Type | Required |
|---------|------|----------|
| complaint_id | Integer | Yes |
| files | File[] | Yes |

---

## Supported Formats

- JPG
- JPEG
- PNG
- PDF
- MP3
- WAV

---

## Maximum Size

```
20 MB per file
```

---

## Success Response

**HTTP 201**

```json
{
    "success": true,

    "message": "Evidence uploaded successfully.",

    "data": {

        "uploaded_files": 3,

        "failed_files": 0

    }
}
```

---

## Error Response

```json
{
    "success": false,

    "message": "Unsupported file format."
}
```

---

# API-302 — List Evidence

## Endpoint

```http
GET /api/v1/evidence/{complaint_id}
```

---

## Authentication

✅ JWT Required

---

## Description

Returns all uploaded evidence for a complaint.

---

## Success Response

```json
{
    "success": true,

    "data":[

        {

            "evidence_id":10,

            "file_name":"bill.pdf",

            "file_type":"PDF",

            "upload_time":"2026-07-20"

        }

    ]
}
```

---

# API-303 — Delete Evidence

## Endpoint

```http
DELETE /api/v1/evidence/{evidence_id}
```

---

## Authentication

✅ JWT Required

---

## Success Response

```json
{
    "success": true,

    "message":"Evidence deleted successfully."
}
```

---

# API-304 — Download Evidence

## Endpoint

```http
GET /api/v1/evidence/download/{evidence_id}
```

---

## Authentication

✅ JWT Required

---

## Success Response

Returns the requested file for download.

---

# 16. OCR APIs

---

# API-401 — Extract Text

## Endpoint

```http
POST /api/v1/ocr/extract
```

---

## Authentication

✅ JWT Required

---

## Description

Extracts text from uploaded images or PDF files.

---

## Request

```json
{
    "evidence_id":15
}
```

---

## OCR Pipeline

```
Image

↓

OpenCV

↓

Noise Removal

↓

Grayscale

↓

Threshold

↓

Tesseract OCR

↓

Extracted Text
```

---

## Success Response

```json
{
    "success":true,

    "data":{

        "ocr_text":"Invoice No. 1205...",

        "confidence":96.12

    }
}
```

---

## Error Response

```json
{
    "success":false,

    "message":"OCR processing failed."
}
```

---

# API-402 — OCR Status

## Endpoint

```http
GET /api/v1/ocr/status/{evidence_id}
```

---

## Authentication

✅ JWT Required

---

## Response

```json
{
    "success":true,

    "status":"Completed"
}
```

---

# 17. Entity Extraction APIs

---

# API-403 — Extract Entities

## Endpoint

```http
POST /api/v1/ocr/entities
```

---

## Authentication

✅ JWT Required

---

## Description

Extracts important entities from OCR text.

---

## Extracted Entities

- Names
- Dates
- Organizations
- Currency Amounts
- Addresses

---

## Request

```json
{
    "evidence_id":15
}
```

---

## Success Response

```json
{
    "success":true,

    "data":{

        "persons":[
            "John Doe"
        ],

        "dates":[
            "12-07-2026"
        ],

        "amounts":[
            "₹18,500"
        ],

        "organizations":[
            "ABC Electronics"
        ]

    }
}
```

---

# 18. Timeline APIs

---

# API-501 — Generate Timeline

## Endpoint

```http
POST /api/v1/timeline/generate
```

---

## Authentication

✅ JWT Required

---

## Description

Creates a chronological timeline from uploaded evidence.

---

## Request

```json
{
    "complaint_id":101
}
```

---

## Success Response

```json
{
    "success":true,

    "timeline":[

        {

            "date":"2026-07-12",

            "event":"Product Purchased"

        },

        {

            "date":"2026-07-18",

            "event":"Seller Refused Replacement"

        }

    ]
}
```

---

# 19. Document Generation APIs

---

# API-601 — Generate Complaint Document

## Endpoint

```http
POST /api/v1/documents/generate
```

---

## Authentication

✅ JWT Required

---

## Description

Generates a formatted complaint document.

---

## Request

```json
{
    "complaint_id":101,

    "document_type":"PDF"
}
```

---

## Supported Formats

- PDF
- HTML

(DOCX planned for future versions.)

---

## Success Response

```json
{
    "success":true,

    "data":{

        "document_id":55,

        "download_url":"/api/v1/documents/download/55"

    }
}
```

---

# API-602 — Download Document

## Endpoint

```http
GET /api/v1/documents/download/{document_id}
```

---

## Authentication

✅ JWT Required

---

## Description

Downloads a generated complaint document.

---

## Success

Returns the PDF or HTML document.

---

# API-603 — Document History

## Endpoint

```http
GET /api/v1/documents
```

---

## Authentication

✅ JWT Required

---

## Success Response

```json
{
    "success":true,

    "data":[

        {

            "document_id":55,

            "document_type":"PDF",

            "generated_at":"2026-07-20"

        }

    ]
}
```

---

# API-604 — Delete Generated Document

## Endpoint

```http
DELETE /api/v1/documents/{document_id}
```

---

## Authentication

✅ JWT Required

---

## Success Response

```json
{
    "success":true,

    "message":"Document deleted successfully."
}
```

---

# API Summary

| API | Method | JWT |
|------|--------|-----|
| Upload Evidence | POST | ✅ |
| List Evidence | GET | ✅ |
| Delete Evidence | DELETE | ✅ |
| Download Evidence | GET | ✅ |
| OCR Extract | POST | ✅ |
| OCR Status | GET | ✅ |
| Entity Extraction | POST | ✅ |
| Timeline Generation | POST | ✅ |
| Generate Document | POST | ✅ |
| Download Document | GET | ✅ |
| Document History | GET | ✅ |
| Delete Document | DELETE | ✅ |

---

## End of Part 3

**Next:** **Part 4 — Admin APIs (Future), API Security, Validation Rules, Rate Limiting, Error Handling, Postman Collection Structure, API Testing Checklist, and Best Practices.**

# Part 4 — API Security, Validation, Error Handling, Testing & Best Practices

---

# 20. API Security

## Security Objectives

Every API in Judiciary Flow must ensure:

- Authentication
- Authorization
- Input Validation
- Secure Data Transfer
- Secure File Uploads
- Protection against common attacks

---

## Authentication

Protected APIs require a valid JWT token.

Example

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## Authorization

Before processing any request:

1. Validate JWT
2. Verify user exists
3. Verify ownership of resource
4. Execute request

Example

```
User

↓

JWT Validation

↓

Complaint Owner?

↓

Allow / Deny
```

---

## HTTPS

Production APIs must only be accessible over HTTPS.

```
https://api.judiciaryflow.com/api/v1/
```

---

# 21. API Validation Rules

---

## Registration Validation

| Field | Validation |
|---------|------------|
| Full Name | Required |
| Email | Valid Email |
| Mobile | 10 Digits |
| Password | Minimum 8 Characters |

---

## Complaint Validation

| Field | Validation |
|---------|------------|
| Title | Required |
| Description | Minimum 30 Characters |
| State | Required |
| District | Required |

---

## File Upload Validation

| Rule | Value |
|------|-------|
| Allowed Files | JPG, PNG, PDF, MP3, WAV |
| Maximum Size | 20 MB |
| MIME Validation | Required |
| Virus Scan | Future Enhancement |

---

## AI Validation

Before classification

- Complaint description cannot be empty.
- Minimum length: 30 characters.
- Maximum length: 5000 characters.

---

# 22. Rate Limiting

To protect against abuse, APIs should enforce request limits.

---

## Login API

```
Maximum

5 Requests

per Minute

per IP
```

---

## Complaint APIs

```
100 Requests

per Hour

per User
```

---

## Upload APIs

```
20 Uploads

per Hour

per User
```

---

## Error Response

```json
{
    "success": false,

    "message": "Rate limit exceeded. Please try again later."
}
```

HTTP Status

```
429 Too Many Requests
```

---

# 23. API Error Handling

Every API should return consistent error responses.

---

## Validation Error

HTTP

```
422
```

Response

```json
{
    "success": false,

    "message": "Validation failed.",

    "errors": {

        "email":"Invalid email format."

    }
}
```

---

## Unauthorized

HTTP

```
401
```

```json
{
    "success": false,

    "message":"Authentication required."
}
```

---

## Forbidden

HTTP

```
403
```

```json
{
    "success": false,

    "message":"Access denied."
}
```

---

## Resource Not Found

HTTP

```
404
```

```json
{
    "success": false,

    "message":"Complaint not found."
}
```

---

## Internal Server Error

HTTP

```
500
```

```json
{
    "success": false,

    "message":"Internal server error."
}
```

---

# 24. API Logging

The backend should log important API events.

---

## Log Authentication

- Login
- Logout
- Invalid Login
- Invalid JWT

---

## Log Complaints

- Complaint Created
- Complaint Updated
- Complaint Deleted

---

## Log Documents

- PDF Generated
- Document Downloaded

---

## Log Uploads

- Upload Started
- Upload Completed
- OCR Started
- OCR Failed

---

## Never Log

- Passwords
- JWT Tokens
- API Secrets
- Database Passwords

---

# 25. API Versioning Strategy

Current Version

```
/api/v1/
```

Future

```
/api/v2/
```

Older versions should remain supported until deprecated.

---

# 26. API Testing

## Manual Testing

Use

- Postman
- Insomnia

---

## Automated Testing

Recommended

```python
unittest
```

---

## Authentication Tests

- Register
- Login
- Invalid Login
- Expired Token
- Missing Token

---

## Complaint Tests

- Create Complaint
- Update Complaint
- Delete Complaint
- View Complaint
- History

---

## Upload Tests

- JPG Upload
- PDF Upload
- Invalid File
- Large File

---

## OCR Tests

- Clear Image
- Blurry Image
- Rotated Image
- Corrupted Image

---

## Document Tests

- Generate PDF
- Download PDF
- Invalid Document ID

---

# 27. Suggested Postman Collection

```
Authentication

├── Register
├── Login
├── Logout
├── Get Profile
└── Update Profile

Complaints

├── Create Complaint
├── Get Complaint
├── Update Complaint
├── Delete Complaint
├── Complaint History
├── Categories
└── Departments

AI

├── Classify Complaint
└── Department Recommendation

Evidence

├── Upload
├── List
├── Download
└── Delete

OCR

├── Extract Text
├── OCR Status
└── Extract Entities

Timeline

└── Generate Timeline

Documents

├── Generate PDF
├── Download PDF
├── History
└── Delete
```

---

# 28. API Best Practices

Developers should:

- Use RESTful naming conventions.
- Return consistent JSON responses.
- Validate all inputs.
- Authenticate every protected endpoint.
- Use parameterized SQL queries.
- Return meaningful HTTP status codes.
- Avoid exposing internal server errors.
- Document every new endpoint.
- Maintain backward compatibility for API versions.

---

# 29. API Checklist

## Authentication

- [ ] Register API
- [ ] Login API
- [ ] Logout API
- [ ] JWT Validation

---

## Complaint

- [ ] CRUD APIs
- [ ] Complaint History
- [ ] Categories
- [ ] Departments

---

## AI

- [ ] Complaint Classification
- [ ] Department Recommendation
- [ ] Manual Category Override

---

## Evidence

- [ ] Upload
- [ ] Download
- [ ] Delete
- [ ] List

---

## OCR

- [ ] OCR Extraction
- [ ] Entity Extraction
- [ ] OCR Status

---

## Documents

- [ ] Generate PDF
- [ ] Download
- [ ] History
- [ ] Delete

---

## Security

- [ ] JWT
- [ ] Validation
- [ ] HTTPS
- [ ] Rate Limiting
- [ ] Error Handling

---

# 30. Future APIs

The following APIs are planned for future versions:

### Government Integration

```
GET /api/v2/government/departments
```

---

### Complaint Tracking

```
GET /api/v2/complaints/status
```

---

### Email Notifications

```
POST /api/v2/notifications/email
```

---

### SMS Notifications

```
POST /api/v2/notifications/sms
```

---

### Feedback API

```
POST /api/v2/feedback
```

---

# 31. API Documentation Summary

| Module | Status |
|----------|--------|
| Authentication APIs | ✅ |
| Complaint APIs | ✅ |
| AI APIs | ✅ |
| Evidence APIs | ✅ |
| OCR APIs | ✅ |
| Timeline APIs | ✅ |
| Document APIs | ✅ |
| Validation Rules | ✅ |
| Security | ✅ |
| Testing | ✅ |
| Error Handling | ✅ |

---

# 32. Conclusion

The Judiciary Flow REST API is designed using RESTful principles with JWT-based authentication, consistent JSON responses, and modular endpoints. It provides a clean separation between the frontend and backend, making development straightforward for both human developers and AI coding agents.

The API architecture supports the complete Judiciary Flow workflow:

- User Authentication
- Complaint Management
- AI-Based Complaint Classification
- Department Recommendation
- Evidence Upload
- OCR Processing
- Timeline Generation
- Complaint Document Generation
- PDF Download

The design is scalable, secure, and ready for future integrations with government portals and additional AI capabilities.

---

# Document Summary

**Document Name:** `07_API_Documentation.md`

**Version:** 1.0

**API Style:** REST

**Authentication:** JWT

**Response Format:** JSON

**Status:** Complete

**Purpose:** Defines the complete REST API contract for Judiciary Flow, including endpoint specifications, authentication, request/response formats, validation, security, testing, and best practices.

---

# ✅ API Documentation Complete

You now have a complete API specification with:
- **24+ REST endpoints**
- **JWT authentication flow**
- **Request & response examples**
- **Validation rules**
- **Security guidelines**
- **Testing checklist**
- **Postman collection structure**

This document can be used directly by frontend developers, backend developers, QA engineers, and AI coding agents to implement the entire Judiciary Flow backend.