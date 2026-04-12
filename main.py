from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()
from auth import create_user, verify_user

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB
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

# ROUTES
@app.get("/")
def home():
    return {"status": "running"}

@app.post("/signup")
def signup(user: User):
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, 10)", (user.email, user.password))
        conn.commit()
        return {"status": "success", "api_key": user.email}
    except:
        return {"status": "error", "message": "User exists"}

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (user.email, user.password))
    if cursor.fetchone():
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "Invalid"}

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

    cursor.execute("UPDATE users SET credits = credits - 1 WHERE email=?", (api_key,))
    conn.commit()

    return {
        "tick": tick_store[api_key],
        "credits_left": credits - 1
    }
from auth import create_user, verify_user
      
@app.post("/signup")
def signup(user: User):
    if create_user(cursor, conn, user.email, user.password):
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "User exists"}
    
@app.post("/login")
def login(user: User):
    if verify_user(cursor, user.email, user.password):
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "Invalid"}

  const data = await res.json();
  console.log(data);
}
<script>
const API = "https://ai-civilization-sim-production.up.railway.app";

/* ===== SIGNUP ===== */
async function signup() {
  try {
    const res = await fetch(`${API}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      })
    });

    const data = await res.json();

    if (data.status === "success") {
      localStorage.setItem("api_key", data.api_key);
    }

    document.getElementById("output").innerText =
      JSON.stringify(data, null, 2);

  } catch (err) {
    document.getElementById("output").innerText =
      "Signup error: " + err.message;
  }
}

/* ===== LOGIN ===== */
async function login() {
  try {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      })
    });

    const data = await res.json();

    if (data.status === "success") {
      localStorage.setItem("api_key", data.api_key);
    }

    document.getElementById("output").innerText =
      JSON.stringify(data, null, 2);

  } catch (err) {
    document.getElementById("output").innerText =
      "Login error: " + err.message;
  }
}

/* ===== SIMULATION ===== */
async function runSim() {
  try {
    const apiKey = localStorage.getItem("api_key");

    if (!apiKey) {
      document.getElementById("output").innerText =
        "Please login first!";
      return;
    }

    const res = await fetch(`${API}/step?api_key=${apiKey}`);
    const data = await res.json();

    document.getElementById("output").innerText =
      JSON.stringify(data, null, 2);

  } catch (err) {
    document.getElementById("output").innerText =
      "Simulation error: " + err.message;
  }
}
</script>

