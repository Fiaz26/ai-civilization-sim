from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    plan TEXT DEFAULT 'free',
    credits INTEGER DEFAULT 10
)
""")
conn.commit()

# MODELS
class User(BaseModel):
    email: str
    password: str

# AUTH
@app.post("/signup")
def signup(user: User):
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                       (user.email, user.password))
        conn.commit()
        return {"status": "success", "api_key": user.email}
    except:
        return {"status": "error", "message": "User exists"}

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (user.email, user.password))
    data = cursor.fetchone()

    if data:
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "Invalid credentials"}
    localStorage.setItem("api_key", data.api_key);

# SIMULATION (USER BASED)
tick_store = {}

@app.get("/step")
def step(api_key: str):
    cursor.execute("SELECT credits FROM users WHERE email=?", (api_key,))
    user = cursor.fetchone()

    if not user:
        return {"error": "Invalid API key"}

    credits = user[0]

    if credits <= 0:
        return {"error": "Upgrade plan required"}

    tick_store[api_key] = tick_store.get(api_key, 0) + 1

    # reduce credit
    cursor.execute("UPDATE users SET credits = credits - 1 WHERE email=?", (api_key,))
    conn.commit()

    tick = tick_store[api_key]

    return {
        "tick": tick,
        "gdp": 1000 + tick * 10,
        "agents": 10 + tick,
        "companies": 2 + tick // 2,
        "credits_left": credits - 1
    }

# ADMIN
@app.get("/admin")
def admin():
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(credits) FROM users")
    total_credits = cursor.fetchone()[0]

    return {
        "total_users": total_users,
        "total_credits": total_credits
    }
fetch(`${API}/step?api_key=` + localStorage.getItem("api_key"))

      
