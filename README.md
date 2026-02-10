# Project--Trace 🔍  
### Intelligent Digital Archival & Semantic Search System

**Project--Trace** is an AI-powered digital archival platform designed for **Robust Materials Technology Pvt. Ltd.**  
It enables **context-based semantic search**, **OCR metadata exploration**, and **project lifecycle tracking** for laboratory and research documents.

---

## 🚀 Key Features

- 🔎 **Semantic Search (Context-Based)**
  - Search documents using natural language queries
  - Powered by Sentence Transformers (`all-MiniLM-L6-v2`)
  
- 📄 **OCR Metadata Utilization**
  - Search across extracted OCR text, summaries, keywords, techniques, and APIs

- 📆 **Date-Based Filtering**
  - Exact date search
  - Date range filtering (From–To)

- 🗂️ **Version-Aware Document Management**
  - Automatically updates documents based on project ID + title
  - Retains only the latest version

- 🖥️ **Interactive UI/UX**
  - Google-like search flow
  - Clickable results → detailed document view
  - Modern industry-grade UI inspired by Dribbble designs

- 📤 **Bulk Upload**
  - Upload CSV / Excel files for metadata ingestion

---

## 🧠 Tech Stack

### Backend
- **FastAPI**
- **PostgreSQL**
- **psycopg**
- **Sentence Transformers**
- **Scikit-learn**
- **Pandas**

### Frontend
- **HTML5**
- **CSS3**
- **Vanilla JavaScript**
- Custom UI/UX (Industry-focused)

---

## 🧠 Technology Stack

### Backend
- **FastAPI** – High-performance API framework
- **PostgreSQL** – Relational database
- **psycopg** – PostgreSQL adapter
- **Pandas** – Data ingestion & validation

### AI / ML
- **Sentence-Transformers**
- Model: `all-MiniLM-L6-v2`
- **Cosine Similarity** for ranking

### Frontend
- **HTML5 / CSS3 / JavaScript**
- Modular file structure
- Fully decoupled frontend & backend

---

## 🗄 Database Design

### Table: `document_metadata`

| Column | Description |
|------|-------------|
| record_id | UUID (Primary Key) |
| document_title | Document name |
| project_documents | Source type |
| project_id | Project identifier |
| product_api_name | API / Product |
| technique | Experimental technique |
| document_date | Document date |
| archived_date | Archive date |
| version | Version number |
| ocr_text | OCR extracted text |
| keywords | Indexed keywords |
| summary | Short document summary |

---

## 🔁 Upload Logic

- Documents are **inserted or updated automatically**
- Updates occur **only if uploaded version is higher**
- Prevents duplicate records
- Maintains clean project history

---

## 🔍 Semantic Search Workflow

1. User submits natural language query
2. Query converted to embedding
3. Documents combined text fields:
   - Title
   - Technique
   - Keywords
   - Summary
   - OCR text
4. Cosine similarity computed
5. Top-K ranked results returned

---

## Running the Project

### Backend Setup
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs at:
http://127.0.0.1:8000

Frontend Setup:
python -m http.server 5500

Open in browser:
http://127.0.0.1:5500/index.html

👩‍💻 Author

VR Institute
IT Department

Designed and developed for
Robust Materials Technology Pvt. Ltd.

© License & Copyright

Copyright © 2022
Robust Materials Technology Pvt. Ltd.
All Rights Reserved.