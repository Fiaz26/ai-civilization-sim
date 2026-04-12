
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

# In-memory storage (stable for now)
users = {}
ticks = {}

@app.get("/")
def home():
    return {"status": "running"}


@app.post("/signup")
def signup(data: dict):
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return {"status": "error", "msg": "User exists"}

    users[email] = {
        "password": password,
        "credits": 10
    }

    return {
        "status": "success",
        "api_key": email,
        "credits": 10
    }


@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if email in users and users[email]["password"] == password:
        return {
            "status": "success",
            "api_key": email,
            "credits": users[email]["credits"]
        }

    return {"status": "error", "msg": "Invalid login"}


@app.get("/step")
def step(api_key: str):
    if api_key not in users:
        return {"error": "Invalid user"}

    if users[api_key]["credits"] <= 0:
        return {
            "error": "No credits",
            "message": "Upgrade required"
        }

    users[api_key]["credits"] -= 1
    ticks[api_key] = ticks.get(api_key, 0) + 1

    return {
        "tick": ticks[api_key],
        "credits_left": users[api_key]["credits"]
    }
