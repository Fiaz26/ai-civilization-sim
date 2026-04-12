import sqlite3

def get_db():
    conn = sqlite3.connect("db.sqlite", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def init_db():
    conn, cursor = get_db()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        credits INTEGER DEFAULT 10
    )
    """)
    conn.commit()
    conn.close()
