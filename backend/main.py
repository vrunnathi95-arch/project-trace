from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Path
from datetime import date
import os
import shutil
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from db import get_connection
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---------------- INIT ----------------

app = FastAPI()

# Absolute path to frontend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ---------------- DATE SEARCH ----------------

@app.post("/search")
def search_by_date(
    search_type: str = Form(...),
    exact_date: date | None = Form(None),
    from_date: date | None = Form(None),
    to_date: date | None = Form(None),
):
    conn = get_connection()
    cur = conn.cursor()

    if search_type == "exact":
        cur.execute(
            """
            SELECT document_title, technique, document_date
            FROM document_metadata
            WHERE document_date = %s
            """,
            (exact_date,),
        )
    else:
        cur.execute(
            """
            SELECT document_title, technique, document_date
            FROM document_metadata
            WHERE document_date BETWEEN %s AND %s
            """,
            (from_date, to_date),
        )

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results

# ---------------- SEMANTIC SEARCH ----------------

@app.post("/semantic-search")
def semantic_search(query: str = Form(...), top_k: int = 5):

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            record_id,
            document_title,
            product_api_name,
            technique,
            keywords,
            summary,
            ocr_text
        FROM document_metadata
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return []

    texts = []
    metadata = []

    for r in rows:
        combined_text = " ".join([
            r[1] or "",
            r[2] or "",
            r[3] or "",
            r[4] or "",
            r[5] or "",
            r[6] or "",
        ]).strip()

        if combined_text:
            texts.append(combined_text)
            metadata.append({
                "record_id": r[0],
                "document_title": r[1],
                "technique": r[3],
            })

    if not texts:
        return []

    doc_embeddings = model.encode(texts)
    query_embedding = model.encode([query])

    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    ranked = sorted(
        zip(metadata, similarities),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    return [
        {
            **item,
            "score": float(score)
        }
        for item, score in ranked
    ]

# ---------------- DOCUMENT DETAILS ----------------

@app.get("/document/{record_id}")
def get_document_details(record_id: str = Path(...)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            record_id,
            document_title,
            project_documents,
            project_id,
            product_api_name,
            technique,
            document_date,
            archived_date,
            version,
            ocr_text,
            keywords,
            summary
        FROM document_metadata
        WHERE record_id = %s
        """,
        (record_id,)
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "record_id": row[0],
        "document_title": row[1],
        "project_documents": row[2],
        "project_id": row[3],
        "product_api_name": row[4],
        "technique": row[5],
        "document_date": row[6],
        "archived_date": row[7],
        "version": row[8],
        "ocr_text": row[9],
        "keywords": row[10],
        "summary": row[11],
    }

# ---------------- UPLOAD & INSERT ----------------

@app.post("/upload")
def upload_and_insert_metadata(file: UploadFile = File(...)):

    filename = file.filename.lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File read error: {e}")

    df.columns = df.columns.str.strip().str.lower()

    required_columns = {
        "document_title",
        "project_documents",
        "project_id",
        "product_api_name",
        "technique",
        "document_date",
        "archived_date",
        "version",
        "ocr_text",
        "keywords",
        "summary",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing}",
        )

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    updated = 0

    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO document_metadata (
                document_title,
                project_documents,
                project_id,
                product_api_name,
                technique,
                document_date,
                archived_date,
                version,
                ocr_text,
                keywords,
                summary
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (project_id, document_title)
            DO UPDATE SET
                project_documents = EXCLUDED.project_documents,
                product_api_name = EXCLUDED.product_api_name,
                technique = EXCLUDED.technique,
                document_date = EXCLUDED.document_date,
                archived_date = EXCLUDED.archived_date,
                version = EXCLUDED.version,
                ocr_text = EXCLUDED.ocr_text,
                keywords = EXCLUDED.keywords,
                summary = EXCLUDED.summary
            WHERE document_metadata.version < EXCLUDED.version
            """,
            (
                row["document_title"],
                row["project_documents"],
                row["project_id"],
                row["product_api_name"],
                row["technique"],
                row["document_date"],
                row["archived_date"],
                int(row["version"]),
                row["ocr_text"],
                row["keywords"],
                row["summary"],
            ),
        )

        if cur.rowcount == 1:
            inserted += 1
        else:
            updated += 1

    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "Upload processed successfully",
        "inserted_rows": inserted,
        "updated_rows": updated,
    }
