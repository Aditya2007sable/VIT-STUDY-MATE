from database.database import get_connection

def add_assignment(title, subject, due_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO assignments(title,subject,due_date) VALUES(?,?,?)",
        (title, subject, due_date)
    )
    conn.commit()
    conn.close()

def list_assignments():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id,title,subject,due_date,status FROM assignments ORDER BY due_date"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
