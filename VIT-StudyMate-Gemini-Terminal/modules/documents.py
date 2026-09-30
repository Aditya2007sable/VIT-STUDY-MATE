from database.database import get_connection
from pypdf import PdfReader


def add_document(title, file_path, content):
    try:
        pages = len(PdfReader(file_path).pages)
    except Exception:
        pages = 0
    conn = get_connection()
    cursor = conn.execute("INSERT INTO documents(title,file_path,content,pages) VALUES(?,?,?,?)", (title, file_path, content, pages))
    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()
    return doc_id


def list_documents():
    conn = get_connection()
    rows = conn.execute("SELECT id,title,file_path,pages,created_at FROM documents ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_document(doc_id):
    conn = get_connection()
    row = conn.execute("SELECT id,title,file_path,content,pages,created_at FROM documents WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
