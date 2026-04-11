# database.py
import sqlite3

conn = sqlite3.connect("saas.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        plan TEXT DEFAULT 'free',
        api_key TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT,
        endpoint TEXT,
        count INTEGER DEFAULT 0,
        date TEXT
    )
    """)
    conn.commit()
  cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key TEXT,
    method TEXT,
    amount REAL,
    txn_id TEXT,
    status TEXT
)
""")
