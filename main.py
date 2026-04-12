from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {}  # in-memory (temporary but stable)
ticks = {}

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/signup")
def signup(data: dict):
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return {"status": "error", "msg": "exists"}

    users[email] = password
    return {"status": "success", "api_key": email}


@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if users.get(email) == password:
        return {"status": "success", "api_key": email}

    return {"status": "error", "msg": "invalid"}


@app.get("/step")
def step(api_key: str):
    ticks[api_key] = ticks.get(api_key, 0) + 1
    return {
        "tick": ticks[api_key],
        "user": api_key
    }
    
