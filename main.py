from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI

app = FastAPI()

tick = 0

@app.get("/")
def home():
    return {"status": "running"}

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
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

fake_users = {}

@app.post("/signup")
def signup(user: User):
    email = user.email.strip().lower()

    if email in fake_users:
        return {"status": "error", "message": "User already exists"}

    fake_users[email] = user.password
    return {"status": "success", "api_key": email}


@app.post("/login")
def login(user: User):
    email = user.email.strip().lower()

    if fake_users.get(email) == user.password:
        return {"status": "success", "api_key": email}

    return {"status": "error", "message": "Invalid credentials"}
    
