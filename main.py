from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    credits INTEGER DEFAULT 10
)
""")
conn.commit()

class User(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/signup")
def signup(user: User):
    try:
        cursor.execute(
            "INSERT INTO users (email, password, credits) VALUES (?, ?, 10)",
            (user.email, user.password)
        )
        conn.commit()
        return {"status": "success", "api_key": user.email}
    except:
        return {"status": "error"}

@app.post("/login")
def login(user: User):
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (user.email, user.password)
    )
    if cursor.fetchone():
        return {"status": "success", "api_key": user.email}
    return {"status": "error"}

tick_store = {}

@app.get("/step")
def step(api_key: str):
    cursor.execute("SELECT credits FROM users WHERE email=?", (api_key,))
    user = cursor.fetchone()

    if not user:
        return {"error": "Invalid key"}

    credits = user[0]

    if credits <= 0:
        return {"error": "No credits"}

    tick_store[api_key] = tick_store.get(api_key, 0) + 1

    cursor.execute(
        "UPDATE users SET credits = credits - 1 WHERE email=?",
        (api_key,)
    )
    conn.commit()

    return {
        "tick": tick_store[api_key],
        "credits_left": credits - 1
    }
    
