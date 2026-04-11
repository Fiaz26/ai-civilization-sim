from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS MUST BE FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------
# DATA STORE (TEMP)
# ------------------
users = {}

class User(BaseModel):
    email: str
    password: str

# ------------------
# TEST ROUTE
# ------------------
@app.get("/")
def home():
    return {"status": "working"}

# ------------------
# SIGNUP
# ------------------
@app.post("/signup")
def signup(user: User):
    email = user.email.lower()

    if email in users:
        return {"status": "error", "message": "User exists"}

    users[email] = user.password
    return {"status": "success", "api_key": email}

# ------------------
# LOGIN
# ------------------
@app.post("/login")
def login(user: User):
    email = user.email.lower()

    if users.get(email) == user.password:
        return {"status": "success", "api_key": email}

    return {"status": "error", "message": "Invalid credentials"}

# ------------------
# SIMULATION
# ------------------
tick = 0

@app.get("/step")
def step():
    global tick
    tick += 1

    return {
        "tick": tick,
        "gdp": 1000 + tick * 10,
        "agents": 10 + tick,
        "companies": 2 + tick // 2,
        "alive": True
    }
