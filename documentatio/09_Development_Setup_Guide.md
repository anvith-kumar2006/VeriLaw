# 09_Development_Setup_Guide.md

# Judiciary Flow

## Development Setup Guide

**Version:** 1.0

**Project:** Judiciary Flow

**Document Type:** Development Setup Guide

**Audience**

- Developers
- AI Coding Agents
- Open Source Contributors

**Supported Platforms**

- Windows 10/11
- Ubuntu 22+
- macOS

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | July 2026 | Initial Development Setup Guide |

---

# Table of Contents

1. Introduction
2. System Requirements
3. Required Software
4. Development Environment
5. Project Folder Structure
6. Project Architecture
7. Development Workflow

---

# 1. Introduction

## Purpose

This guide explains how to set up the Judiciary Flow project for development from scratch.

It enables any developer or AI coding assistant to clone the repository, install dependencies, configure the environment, and start building the project quickly.

---

## Target Audience

This guide is intended for:

- Backend Developers
- Frontend Developers
- Database Developers
- AI/ML Engineers
- QA Engineers
- Hackathon Team Members
- AI Coding Agents (Cursor, Claude Code, GitHub Copilot, Gemini CLI)

---

## Objectives

After completing this guide, you will be able to:

- Clone the repository
- Configure the development environment
- Install all dependencies
- Run the backend
- Run the frontend
- Connect the database
- Begin feature development

---

# 2. System Requirements

## Minimum Requirements

| Component | Requirement |
|------------|-------------|
| Processor | Dual Core |
| RAM | 8 GB |
| Storage | 5 GB Free |
| Internet | Required |

---

## Recommended

| Component | Recommendation |
|------------|----------------|
| Processor | Intel i5 / Ryzen 5 or Better |
| RAM | 16 GB |
| Storage | SSD with 20 GB Free |
| Internet | Stable Broadband |

---

# 3. Required Software

## Code Editor

Recommended

```
Visual Studio Code
```

### Recommended VS Code Extensions

- Python
- Pylance
- GitLens
- Error Lens
- Prettier
- Better Comments
- Live Server
- Material Icon Theme

---

## Backend

Install

```
Python 3.11+
```

Verify

```bash
python --version
```

---

## Database

Install

```
MySQL 8.x
```

Also install

```
MySQL Workbench
```

---

## Version Control

Install

```
Git
```

Verify

```bash
git --version
```

---

## Browser

Recommended

- Google Chrome
- Microsoft Edge

---

## OCR Engine

Install

```
Tesseract OCR
```

Verify

```bash
tesseract --version
```

---

# 4. Development Environment

## Backend Stack

- Python
- Flask
- Flask REST API
- Flask-JWT-Extended
- Flask-Mail
- bcrypt

---

## Frontend Stack

- HTML5
- CSS3
- Vanilla JavaScript
- Jinja2 Templates

---

## Database

- MySQL
- MySQL Workbench

---

## AI & Machine Learning

- NumPy
- Pandas
- Scikit-learn
- spaCy
- OpenCV
- Pillow
- Tesseract OCR

---

## PDF Generation

- ReportLab
- python-docx
- PyMuPDF

---

# 5. Project Folder Structure

```text
Judiciary-Flow/

│

├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── middleware/
│   ├── ai/
│   ├── utils/
│   └── uploads/

│
├── frontend/
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       ├── images/
│       ├── fonts/
│       └── icons/

│
├── database/
│   ├── schema.sql
│   └── seed.sql

│
├── datasets/

│
├── trained_models/

│
├── docs/

│
├── README.md

├── .env

├── .gitignore

└── LICENSE
```

---

# Folder Description

| Folder | Purpose |
|----------|----------|
| backend | Flask Backend |
| frontend | User Interface |
| database | SQL Scripts |
| datasets | AI Training Data |
| trained_models | Saved ML Models |
| uploads | Uploaded Evidence |
| docs | Project Documentation |

---

# 6. Project Architecture

```text
                Judiciary Flow

                     User

                       │

                       ▼

          HTML + CSS + JavaScript

                       │

                       ▼

               Flask REST API

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

 Authentication   Complaint API     AI Module

                                        │

                                 OCR Processing

                                        │

                                        ▼

                              MySQL Database

                                        │

                                        ▼

                            PDF Generation Engine
```

---

## Application Modules

### Authentication Module

Responsible for

- Registration
- Login
- JWT Authentication
- Profile Management

---

### Complaint Module

Responsible for

- Complaint Creation
- Complaint History
- Complaint Editing
- Complaint Status

---

### AI Module

Responsible for

- Complaint Classification
- Department Recommendation

---

### OCR Module

Responsible for

- Image Processing
- Text Extraction
- Entity Recognition

---

### Document Module

Responsible for

- Complaint Templates
- PDF Generation
- Document Download

---

# 7. Development Workflow

```text
Clone Repository

↓

Create Virtual Environment

↓

Install Dependencies

↓

Configure Database

↓

Configure .env

↓

Run Flask Backend

↓

Run Frontend

↓

Develop Features

↓

Test

↓

Commit

↓

Push

↓

Pull Request
```

---

# Development Guidelines

## Backend

- Keep controllers lightweight
- Business logic inside services
- Validate all requests
- Return JSON responses
- Use Flask Blueprints

---

## Frontend

- Mobile First
- Responsive Design
- Vanilla JavaScript
- Reusable Components
- Accessible Forms

---

## Database

- Use Foreign Keys
- Use Indexes
- Parameterized Queries Only
- Avoid Duplicate Data

---

## Git Commit Convention

Examples

```text
feat: add complaint classification API

fix: resolve JWT authentication issue

docs: update README

style: improve dashboard layout

refactor: optimize OCR module
```

---

# Development Checklist

- [ ] Install Python
- [ ] Install Git
- [ ] Install MySQL
- [ ] Install MySQL Workbench
- [ ] Install VS Code
- [ ] Install Tesseract OCR
- [ ] Clone Repository
- [ ] Create Virtual Environment

---

## End of Part 1

**Next:** **Part 2 — Repository Cloning, Virtual Environment Setup, Dependency Installation, MySQL Configuration, Environment Variables (.env), and Running the Flask Backend.**

# Part 2 — Repository Setup, Virtual Environment, Dependencies, MySQL & Environment Configuration

---

# 8. Clone the Repository

## Clone from GitHub

```bash
git clone https://github.com/<your-username>/Judiciary-Flow.git
```

---

## Move into Project

```bash
cd Judiciary-Flow
```

---

## Verify Project Structure

```text
Judiciary-Flow/

backend/

frontend/

database/

docs/

README.md
```

---

# 9. Create Python Virtual Environment

Using a virtual environment keeps project dependencies isolated.

---

## Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## Verify Activation

You should see

```text
(venv)
```

before the terminal prompt.

---

# 10. Upgrade pip

Always upgrade pip before installing packages.

```bash
python -m pip install --upgrade pip
```

Verify

```bash
pip --version
```

---

# 11. Install Project Dependencies

Inside the backend folder

```bash
cd backend
```

Install packages

```bash
pip install -r requirements.txt
```

---

## Expected Packages

```text
Flask

Flask-JWT-Extended

Flask-Mail

bcrypt

mysql-connector-python

python-dotenv

numpy

pandas

scikit-learn

spacy

opencv-python

pillow

pytesseract

reportlab

python-docx

PyMuPDF

pdfplumber
```

---

## Verify Installation

```bash
pip list
```

---

# 12. Install spaCy Language Model

Download the English language model.

```bash
python -m spacy download en_core_web_sm
```

Verify

```bash
python -m spacy validate
```

---

# 13. Configure MySQL

Start MySQL Server.

Open MySQL Workbench.

Create a new database.

```sql
CREATE DATABASE judiciary_flow;
```

Verify

```sql
SHOW DATABASES;
```

Expected

```text
judiciary_flow
```

---

# 14. Import Database Schema

When the SQL schema is available,

Run

```sql
SOURCE database/schema.sql;
```

Or import using MySQL Workbench.

After importing,

Verify

```sql
SHOW TABLES;
```

Expected

```text
users

complaints

complaint_categories

departments

evidence

generated_documents

activity_logs
```

---

# 15. Configure Environment Variables

Create a file named

```text
.env
```

inside

```text
backend/
```

---

## Example .env

```env
SECRET_KEY=your_secret_key_here

JWT_SECRET_KEY=your_jwt_secret_key_here

DB_HOST=localhost

DB_PORT=3306

DB_NAME=judiciary_flow

DB_USER=root

DB_PASSWORD=your_mysql_password

MAIL_SERVER=smtp.gmail.com

MAIL_PORT=587

MAIL_USE_TLS=True

MAIL_USERNAME=your_email@gmail.com

MAIL_PASSWORD=your_app_password

UPLOAD_FOLDER=uploads/

MAX_CONTENT_LENGTH=20971520
```

---

## Environment Variable Description

| Variable | Purpose |
|----------|----------|
| SECRET_KEY | Flask Secret Key |
| JWT_SECRET_KEY | JWT Signing Key |
| DB_HOST | Database Host |
| DB_PORT | MySQL Port |
| DB_NAME | Database Name |
| DB_USER | MySQL Username |
| DB_PASSWORD | MySQL Password |
| MAIL_SERVER | SMTP Server |
| UPLOAD_FOLDER | Evidence Storage Folder |

---

# 16. Backend Configuration

Example

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DB_HOST = os.getenv("DB_HOST")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
```

---

# 17. Run Flask Backend

Move into backend

```bash
cd backend
```

Start Flask

```bash
python app.py
```

or

```bash
flask run
```

---

## Expected Output

```text
* Running on

http://127.0.0.1:5000
```

---

# 18. Verify Backend

Open browser

```text
http://localhost:5000
```

Or test using Postman

```http
GET /api/v1/health
```

Expected Response

```json
{
    "success": true,

    "message": "Judiciary Flow API is running."
}
```

---

# 19. Common Installation Issues

## Python Not Found

Solution

```bash
python --version
```

If not installed,

Install Python 3.11+

---

## MySQL Connection Error

Check

- MySQL Service Running
- Username
- Password
- Database Name

---

## Module Not Found

Run

```bash
pip install -r requirements.txt
```

again.

---

## spaCy Model Missing

Install

```bash
python -m spacy download en_core_web_sm
```

---

## Tesseract Not Found

Verify

```bash
tesseract --version
```

Add Tesseract to the system PATH if necessary.

---

# 20. Backend Setup Checklist

- [ ] Repository Cloned
- [ ] Virtual Environment Created
- [ ] Virtual Environment Activated
- [ ] pip Updated
- [ ] Dependencies Installed
- [ ] spaCy Model Installed
- [ ] MySQL Installed
- [ ] Database Created
- [ ] Schema Imported
- [ ] .env Configured
- [ ] Flask Running Successfully
- [ ] Backend Verified

---

## End of Part 2

**Next:** **Part 3 — Frontend Setup, AI/OCR Configuration, Running the Complete Application, Testing the Workflow, and Local Development Best Practices.**

# Part 3 — Frontend Setup, AI/OCR Configuration & Running the Complete Application

---

# 21. Frontend Setup

The Judiciary Flow frontend is built using:

- HTML5
- CSS3
- Vanilla JavaScript
- Jinja2 Templates

---

## Navigate to Frontend Folder

```bash
cd frontend
```

---

## Verify Folder Structure

```text
frontend/

│

├── templates/

│   ├── index.html

│   ├── login.html

│   ├── register.html

│   ├── dashboard.html

│   ├── complaint.html

│   ├── evidence.html

│   └── profile.html

│

└── static/

    ├── css/

    ├── js/

    ├── images/

    ├── icons/

    └── fonts/
```

---

# 22. Configure Frontend API URL

Inside

```text
frontend/static/js/config.js
```

Example

```javascript
const API_BASE_URL = "http://localhost:5000/api/v1";
```

For production

```javascript
const API_BASE_URL = "https://your-domain.com/api/v1";
```

---

# 23. Running the Frontend

If using Flask Templates

```bash
python app.py
```

Open

```
http://localhost:5000
```

---

If using Live Server

Install VS Code Extension

```
Live Server
```

Then

Right Click

```
index.html

↓

Open with Live Server
```

---

# 24. Connect Frontend with Backend

Example Login API

```javascript
fetch(`${API_BASE_URL}/auth/login`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email,

password

})

})
```

---

## Store JWT

```javascript
localStorage.setItem(

"token",

response.token

);
```

---

## Send JWT

```javascript
headers:{

Authorization:

`Bearer ${localStorage.getItem("token")}`

}
```

---

# 25. Configure File Uploads

Backend Upload Folder

```
backend/uploads/
```

Recommended Structure

```text
uploads/

│

├── images/

├── pdf/

├── audio/

└── generated_documents/
```

---

## Maximum Upload Size

```
20 MB
```

Allowed Types

- JPG
- PNG
- JPEG
- PDF
- MP3
- WAV

---

# 26. Configure OCR

Install Tesseract

Verify

```bash
tesseract --version
```

---

## Windows Path

Example

```python
pytesseract.pytesseract.tesseract_cmd =

r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## Linux

Usually

```text
/usr/bin/tesseract
```

---

## Test OCR

```python
import pytesseract

print(

pytesseract.get_tesseract_version()

)
```

---

# 27. Configure OpenCV

Verify Installation

```python
import cv2

print(cv2.__version__)
```

---

## Sample Image Processing

```python
image = cv2.imread("sample.jpg")

gray = cv2.cvtColor(

image,

cv2.COLOR_BGR2GRAY

)
```

---

# 28. Configure AI Model

Place trained model inside

```text
trained_models/
```

Example

```text
trained_models/

│

├── complaint_classifier.pkl

├── tfidf_vectorizer.pkl

└── label_encoder.pkl
```

---

## Load Model

```python
import joblib

model = joblib.load(

"trained_models/complaint_classifier.pkl"

)
```

---

## Load TF-IDF

```python
vectorizer = joblib.load(

"trained_models/tfidf_vectorizer.pkl"

)
```

---

# 29. Running Complete Application

Start MySQL

↓

Activate Virtual Environment

↓

Run Flask

↓

Open Browser

↓

Login

↓

Create Complaint

↓

Upload Evidence

↓

OCR

↓

Generate PDF

↓

Download

---

# 30. Verify Complete Workflow

## Authentication

- Register

- Login

- JWT Generated

---

## Complaint Module

- Create Complaint

- View Complaint

- Edit Complaint

---

## AI Module

- Complaint Classification

- Department Recommendation

---

## Evidence

- Upload

- Preview

- Delete

---

## OCR

- Text Extraction

- Entity Extraction

---

## Documents

- Generate PDF

- Download PDF

---

# 31. Local Testing Checklist

## Backend

- [ ] Flask Running

- [ ] APIs Responding

- [ ] JWT Working

---

## Frontend

- [ ] Dashboard Opens

- [ ] Responsive Layout

- [ ] API Calls Successful

---

## Database

- [ ] MySQL Connected

- [ ] Data Saved

- [ ] Queries Working

---

## AI

- [ ] Model Loaded

- [ ] Prediction Successful

---

## OCR

- [ ] Images Processed

- [ ] Text Extracted

---

## PDF

- [ ] Complaint Generated

- [ ] Download Successful

---

# 32. Recommended VS Code Workspace

```text
Judiciary-Flow.code-workspace

backend/

frontend/

database/

docs/

datasets/

trained_models/
```

---

# 33. Useful VS Code Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + Shift + P | Command Palette |
| Ctrl + ` | Open Terminal |
| Ctrl + Shift + F | Global Search |
| Ctrl + P | Quick File Open |
| F5 | Debug |
| Alt + Shift + F | Format Document |

---

# 34. AI Coding Agent Instructions

When using AI coding assistants:

### Cursor

- Generate one feature at a time.
- Follow the API documentation.
- Do not modify database schema without approval.

---

### GitHub Copilot

Use for:

- Boilerplate code
- CRUD operations
- Validation
- Unit tests

---

### Claude Code

Use for:

- Architecture improvements
- Refactoring
- Bug fixing
- Documentation

---

### Gemini CLI

Use for:

- Code explanation
- Debugging
- Optimization

---

# 35. Development Best Practices

✅ Write modular code

✅ Keep controllers small

✅ Store business logic in services

✅ Validate every request

✅ Handle all exceptions

✅ Use meaningful commit messages

✅ Test every feature before pushing

✅ Keep documentation updated

---

# Part 3 Completion Checklist

- [ ] Frontend Configured
- [ ] API URL Configured
- [ ] JWT Connected
- [ ] File Upload Configured
- [ ] OCR Working
- [ ] AI Model Loaded
- [ ] Flask Running
- [ ] Full Workflow Tested
- [ ] VS Code Ready
- [ ] AI Coding Agents Ready

---

## End of Part 3

**Next:** **Part 4 — Git Workflow, Project Standards, Debugging, Troubleshooting, Deployment Preparation & Final Development Checklist.**

# Part 4 — Git Workflow, Debugging, Deployment Preparation & Final Development Checklist

---

# 36. Git Workflow

Judiciary Flow follows a simple Git workflow suitable for hackathons.

---

## Branch Strategy

```text
main

│

develop

│

feature/authentication

feature/dashboard

feature/complaints

feature/ai

feature/evidence

feature/ocr

feature/pdf
```

---

## Clone Repository

```bash
git clone https://github.com/<your-username>/Judiciary-Flow.git
```

---

## Create Feature Branch

```bash
git checkout -b feature/authentication
```

---

## Check Status

```bash
git status
```

---

## Add Files

```bash
git add .
```

---

## Commit Changes

```bash
git commit -m "feat: implement complaint creation API"
```

---

## Push Branch

```bash
git push origin feature/authentication
```

---

## Merge Workflow

```text
Feature Branch

↓

Develop Branch

↓

Main Branch
```

---

# 37. Project Coding Standards

## Python Standards

Follow

- PEP 8
- Snake Case Naming
- Type Hints (where appropriate)

Example

```python
def create_complaint(user_id, data):
    pass
```

---

## HTML Standards

- Semantic HTML
- Accessible Forms
- Responsive Layout
- Proper Labels

---

## CSS Standards

Use

```css
.kf-btn-primary {}

.kf-card {}

.kf-sidebar {}

.kf-input {}
```

Avoid inline CSS.

---

## JavaScript Standards

Use

```javascript
const

let
```

Avoid

```javascript
var
```

Use

- Async/Await
- Modular Functions
- Event Listeners

---

# 38. Logging Standards

Log important events.

Example

```text
INFO

User Login

Complaint Created

OCR Started

PDF Generated
```

---

Never log

- Passwords
- JWT Tokens
- Secret Keys
- Database Passwords

---

# 39. Debugging Guide

## Flask Debug Mode

```python
app.run(debug=True)
```

---

## Check Logs

```bash
python app.py
```

Watch for

- Database Errors
- JWT Errors
- OCR Errors
- AI Prediction Errors

---

## Database Debugging

Check Connection

```sql
SHOW TABLES;
```

Verify Data

```sql
SELECT * FROM users;
```

---

## API Debugging

Use

- Postman
- Thunder Client
- Browser Developer Tools

Verify

- HTTP Status Codes
- JSON Response
- Headers
- JWT Token

---

# 40. Common Errors & Solutions

---

## MySQL Connection Failed

### Cause

- MySQL Server Not Running
- Wrong Credentials
- Wrong Port

### Solution

- Start MySQL
- Verify `.env`
- Test Database Connection

---

## JWT Authentication Failed

### Cause

- Expired Token
- Invalid Token
- Missing Authorization Header

### Solution

Generate a new token by logging in again.

---

## OCR Not Working

### Cause

- Tesseract Not Installed
- Wrong Path

### Solution

Verify

```bash
tesseract --version
```

Configure correct path in Python.

---

## AI Model Not Found

### Cause

Missing model files

### Solution

Verify

```text
trained_models/

complaint_classifier.pkl

tfidf_vectorizer.pkl

label_encoder.pkl
```

---

## PDF Generation Failed

### Cause

Missing ReportLab

### Solution

```bash
pip install reportlab
```

---

# 41. Deployment Preparation

Before deployment verify:

---

## Backend

- [ ] Flask Running
- [ ] APIs Tested
- [ ] JWT Working
- [ ] Error Handling Added

---

## Frontend

- [ ] Responsive
- [ ] Mobile Friendly
- [ ] API Connected
- [ ] No Console Errors

---

## Database

- [ ] Schema Imported
- [ ] Seed Data Added
- [ ] Foreign Keys Verified

---

## AI

- [ ] Model Loaded
- [ ] Prediction Tested
- [ ] Confidence Score Verified

---

## OCR

- [ ] Image Processing Tested
- [ ] OCR Extraction Working

---

## PDF

- [ ] Complaint Generated
- [ ] Download Working

---

# 42. Environment Checklist

```text
Python

✓ Installed

↓

Git

✓ Installed

↓

MySQL

✓ Running

↓

Tesseract

✓ Installed

↓

Flask

✓ Running

↓

Frontend

✓ Connected

↓

Application Ready
```

---

# 43. Final Project Checklist

## Authentication

- [ ] Register
- [ ] Login
- [ ] Logout
- [ ] JWT Authentication

---

## Complaint Module

- [ ] Create Complaint
- [ ] Edit Complaint
- [ ] Delete Complaint
- [ ] History

---

## AI

- [ ] Complaint Classification
- [ ] Department Recommendation

---

## Evidence

- [ ] Upload
- [ ] Preview
- [ ] Delete

---

## OCR

- [ ] Text Extraction
- [ ] Entity Extraction

---

## Documents

- [ ] Generate PDF
- [ ] Download PDF

---

## Security

- [ ] Password Hashing
- [ ] JWT
- [ ] Input Validation
- [ ] SQL Injection Prevention

---

## Testing

- [ ] Backend Tested
- [ ] Frontend Tested
- [ ] Database Tested
- [ ] AI Tested
- [ ] OCR Tested

---

# 44. Hackathon Submission Checklist

## Repository

- [ ] GitHub Repository Public
- [ ] README Updated
- [ ] Documentation Uploaded

---

## Demo

- [ ] Backend Running
- [ ] Frontend Running
- [ ] Database Ready
- [ ] AI Working
- [ ] OCR Working
- [ ] PDF Generation Working

---

## Presentation

- [ ] Slides Ready
- [ ] Demo Data Prepared
- [ ] Sample Evidence Available
- [ ] Internet Backup Available

---

# 45. AI Coding Agent Prompt

Use this prompt while developing with AI agents.

```text
You are the senior software engineer for Judiciary Flow.

Technology Stack:
- Python
- Flask
- MySQL
- HTML
- CSS
- Vanilla JavaScript

Rules:

- Follow the PRD.
- Follow the API documentation.
- Follow the Database Design.
- Follow the Frontend Specification.
- Write modular code.
- Use Flask Blueprints.
- Use parameterized SQL queries.
- Validate every request.
- Use JWT authentication.
- Generate production-quality code.
- Do not change the database schema unless instructed.
```

---

# 46. Recommended Development Order

```text
Project Setup

↓

Authentication

↓

Dashboard

↓

Complaint Module

↓

AI Classification

↓

Department Recommendation

↓

Evidence Upload

↓

OCR

↓

Document Generation

↓

Testing

↓

Deployment
```

---

# 47. Conclusion

This Development Setup Guide provides a complete roadmap for configuring, developing, testing, and preparing Judiciary Flow for hackathon submission.

By following this guide, any developer or AI coding agent can:

- Set up the development environment
- Configure dependencies
- Implement features consistently
- Debug issues efficiently
- Prepare the application for deployment and demonstration

---

# Document Summary

**Document Name:** `09_Development_Setup_Guide.md`

**Version:** 1.0

**Status:** Complete

**Purpose:** Provides complete setup instructions, development standards, Git workflow, debugging guidance, deployment preparation, and AI coding instructions for Judiciary Flow.

---

# ✅ Development Setup Guide Complete

This document is now ready for:

- 👨‍💻 Developers
- 🤖 Cursor AI
- 🤖 Claude Code
- 🤖 GitHub Copilot
- 🤖 Gemini CLI
- 🏆 Hackathon Team Collaboration