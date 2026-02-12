# ProjectTrace

### Intelligent Digital Archival & Semantic Search System

**Robust Materials Technology Pvt. Ltd.**

---

## 🚀 Overview

**ProjectTrace** is an AI-powered digital archival platform designed for structured storage, semantic retrieval, and lifecycle tracking of laboratory project documentation.

The system enables:

* Secure ingestion of project metadata via Excel/CSV upload
* Version-controlled document updates
* Context-based semantic search using transformer embeddings
* Intelligent ranking of archival records
* Structured metadata display with OCR text integration

The platform is built using **FastAPI + PostgreSQL + Sentence Transformers**, following a production-style full-stack architecture.

---

## 🏗 System Architecture

```
project-trace/
│
├── backend/
│   ├── main.py
│   ├── db.py
│   ├── uploads/
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── assets/
```

### Key Design Decisions

* Frontend served directly from FastAPI (`/static`)
* Unified server (no separate frontend runtime required)
* Semantic embeddings computed dynamically
* Version-aware UPSERT logic for document updates
* Clean separation of UI, API, and database layers

---

## ⚙️ Technology Stack

| Layer       | Technology                                 |
| ----------- | ------------------------------------------ |
| Backend API | FastAPI                                    |
| Database    | PostgreSQL                                 |
| DB Driver   | Psycopg                                    |
| ML Model    | sentence-transformers (`all-MiniLM-L6-v2`) |
| Frontend    | HTML, CSS, JavaScript                      |
| Server      | Uvicorn                                    |

---

## 🧠 Core Features

### 1️⃣ Semantic Search

* Context-based search using transformer embeddings
* Cosine similarity ranking
* Top-K result retrieval
* Google-style UX collapse behavior

### 2️⃣ Metadata Ingestion

* Upload `.csv`, `.xls`, `.xlsx`
* Automatic schema validation
* Required columns enforced
* Insert or version-aware update using:

```sql
ON CONFLICT (project_id, document_title)
DO UPDATE
WHERE document_metadata.version < EXCLUDED.version
```

### 3️⃣ Version Control

* Updates only when incoming version is greater
* Prevents accidental overwrites
* Maintains project lifecycle integrity

### 4️⃣ Document Detail View

* Full metadata display
* OCR text preview
* Structured project information
* Scroll-to-detail UX behavior

### 5️⃣ Unified Server Execution

Frontend and backend run using a single command:

```bash
uvicorn main:app --reload
```

No separate frontend server is required.

---

## 🗄 Database Schema

Table: `document_metadata`

| Column            | Type               |
| ----------------- | ------------------ |
| record_id         | UUID (Primary Key) |
| document_title    | TEXT               |
| project_documents | TEXT               |
| project_id        | CHAR               |
| product_api_name  | CHAR               |
| technique         | CHAR               |
| document_date     | DATE               |
| archived_date     | DATE               |
| version           | INTEGER            |
| ocr_text          | TEXT               |
| keywords          | TEXT               |
| summary           | TEXT               |

---

## 📦 Installation Guide

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd project-trace/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure PostgreSQL

Ensure PostgreSQL is running and update `db.py` with your database credentials.

---

## ▶️ Running the Application

From inside the `backend/` directory:

```bash
uvicorn main:app --reload
```

Then open in browser:

```
http://127.0.0.1:8000
```

---

## 📤 Upload Format Requirements

Excel/CSV file must contain the following columns:

```
document_title
project_documents
project_id
product_api_name
technique
document_date
archived_date
version
ocr_text
keywords
summary
```

---

## 🔎 Semantic Search Flow

1. User enters contextual query
2. Backend fetches document metadata
3. Combined searchable text constructed from:

   * Title
   * API
   * Technique
   * Keywords
   * Summary
   * OCR text
4. Embeddings generated
5. Cosine similarity computed
6. Ranked results returned

---

## 🎨 UI/UX Highlights

* Google-style search experience
* Collapsible hero section
* Smooth animations
* Enterprise-style footer
* Upload feedback handling
* Responsive layout
* Clean industrial design aesthetic

---

## 👨‍💻 Developed By

**VR Institute**
IT Department
Robust Materials Technology Pvt. Ltd.

---

## 📜 License

Internal enterprise tool for Robust Materials Technology Pvt. Ltd.

---
