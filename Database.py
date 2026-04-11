import sqlite3

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        plan TEXT DEFAULT 'free',
        credits INTEGER DEFAULT 10
    )
    """)
    conn.commit()
