# ⚖️ Judiciary Flow

## AI-Powered Citizen Complaint Routing & Legal Document Generator

> Simplifying legal complaint preparation by helping citizens identify the correct authority, generate structured complaint documents, and organize supporting evidence.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-green)
![License](https://img.shields.io/badge/License-Hackathon-purple)

---

# 📖 Table of Contents

- Overview
- Problem Statement
- Solution
- Key Features
- Technology Stack
- System Workflow
- Project Architecture
- Folder Structure
- Installation
- Usage
- AI Modules
- Security
- Future Scope
- Contributing
- Legal Disclaimer
- Team

---

# 📌 Overview

**Judiciary Flow** is an AI-powered legal assistance platform designed to help Indian citizens prepare complaints correctly before submitting them to government authorities.

Many complaints fail because people:

- File them in the wrong department
- Use incorrect formats
- Forget important evidence
- Don't know their legal rights

Judiciary Flow simplifies this process through intelligent complaint routing, document generation, and evidence organization.

> **Note:** Judiciary Flow provides legal information and procedural guidance only. It does not replace advocates or licensed legal professionals.

---

# ❗ Problem Statement

Citizens often struggle with legal grievance procedures because they lack:

- Knowledge of the correct government authority
- Understanding of complaint formats
- Proper evidence organization
- Awareness of applicable laws
- Confidence in navigating government systems

As a result, many genuine complaints are delayed, rejected, or never submitted.

---

# 💡 Solution

Judiciary Flow streamlines the complaint preparation process through an AI-assisted workflow.

```

Describe Your Problem
│
▼
Complaint Classification
│
▼
Department Recommendation
│
▼
Complaint Generation
│
▼
Evidence Organization
│
▼
Ready-to-Submit Complaint Package

```

---

# ✨ Key Features

## 1. AI Complaint Routing

- Classifies complaints using Machine Learning
- Recommends the appropriate government department
- Displays relevant legal information
- Suggests alternative authorities when applicable
- Provides confidence score

---

## 2. Smart Complaint Generator

Generate structured complaint documents for:

- Consumer Complaints
- Labour Complaints
- Tenant-Landlord Disputes
- RTI Applications
- FIR Requests
- Cyber Crime Complaints
- Domestic Violence Complaints
- Municipal Complaints
- Banking Complaints
- Insurance Complaints

Export formats:

- PDF
- Printable Document
- Email Draft

---

## 3. Evidence Organizer

Upload:

- Images
- PDFs
- Bills
- Screenshots
- Audio Files

The system automatically:

- Extracts text using OCR
- Detects dates and important entities
- Categorizes evidence
- Creates chronological timelines
- Suggests missing supporting documents

---

# 🛠 Technology Stack

## Backend

- Python
- Flask
- Flask REST API
- Flask-Mail
- Jinja2
- JWT Authentication
- bcrypt

---

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

---

## Database

- MySQL
- MySQL Workbench

---

## AI & Machine Learning

- Scikit-learn
- Pandas
- NumPy
- spaCy
- OpenCV
- Pillow
- Tesseract OCR
- Regex

---

## Document Processing

- ReportLab
- python-docx
- FPDF
- PyMuPDF
- pdfplumber

---

## Development Tools

- Git
- GitHub
- VS Code

---

# ⚙️ System Workflow

```

User
│
▼
Describe Complaint
│
▼
Complaint Classification Model
│
▼
Recommended Authority
│
▼
Complaint Template Selection
│
▼
Complaint Document Generation
│
▼
Evidence Upload
│
▼
OCR + Information Extraction
│
▼
Evidence Timeline
│
▼
Final Complaint Package

```

---

# 🏗 Project Architecture

```

Frontend (HTML • CSS • JavaScript)
│
▼
Flask REST Backend
│
├── Authentication Module
├── Complaint Classification Module
├── Document Generator
├── Evidence Manager
├── OCR Engine
└── API Layer
│
▼
MySQL Database

```

---

# 📂 Project Structure

```

Judiciary-Flow/

├── app.py
├── requirements.txt
├── README.md
│
├── backend/
│ ├── routes/
│ ├── models/
│ ├── services/
│ ├── ai/
│ ├── utils/
│ └── templates/
│
├── frontend/
│ ├── css/
│ ├── js/
│ └── assets/
│
├── database/
│ ├── schema.sql
│ └── seed.sql
│
├── uploads/
│
├── generated_documents/
│
├── datasets/
│
└── docs/

```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Judiciary-Flow.git
```

```bash
cd Judiciary-Flow
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

MYSQL_HOST=localhost

MYSQL_USER=root

MYSQL_PASSWORD=password

MYSQL_DB=judiciary_flow

MAIL_USERNAME=example@gmail.com

MAIL_PASSWORD=your_password
```

---

## Run Application

```bash
python app.py
```

---

# 💻 Usage

1. Register or log in.
2. Describe your complaint.
3. Review the recommended authority.
4. Upload supporting evidence.
5. Generate a structured complaint.
6. Download the final complaint package.

---

# 🤖 AI Modules

### Complaint Classification

- TF-IDF Vectorization
- Scikit-learn Classifier
- Department Recommendation

---

### OCR Processing

- Tesseract OCR
- OpenCV Image Enhancement
- Text Extraction

---

### Entity Recognition

- spaCy
- Regular Expressions

Extracts:

- Names
- Dates
- Addresses
- Amounts
- Organizations

---

### Evidence Categorization

Automatically groups uploaded files into:

- Bills
- Communication
- Images
- Documents
- Audio

---

### Timeline Generator

Creates a chronological sequence of uploaded evidence for easier case preparation.

---

# 🔒 Security

- JWT Authentication
- Password Hashing using bcrypt
- SQL Injection Prevention
- XSS Protection
- CSRF Protection
- Secure File Upload Validation
- Input Validation
- Authentication Middleware
- Access Control
- Logging

---

# 📈 Future Scope

- Multilingual Support
- Voice Complaint Submission
- Government Portal Integration
- Complaint Status Tracking
- Mobile Application
- AI Legal Assistant
- Legal Aid Integration
- Digital Signature Support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# ⚠️ Legal Disclaimer

Judiciary Flow is an educational and citizen assistance platform.

The platform provides:

- Legal information
- Complaint preparation assistance
- Document organization guidance

The platform **does not provide legal advice** and should not be considered a substitute for professional legal counsel.

Users should consult qualified legal professionals for case-specific legal advice.

---

# 👨‍💻 Team

**Project Name**

**Judiciary Flow**

**Category**

AI-Powered Citizen Complaint Routing & Legal Document Generator

**Developed For**

Hackathon Project

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

**Empowering citizens with accessible legal technology.**