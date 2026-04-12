# database.py

import sqlite3

# SINGLE GLOBAL CONNECTION (IMPORTANT)
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        credits INTEGER DEFAULT 10
    )
    """)
    conn.commit()
