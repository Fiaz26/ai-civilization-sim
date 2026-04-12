from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS (required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Model (THIS FIXES CRASH)
class User(BaseModel):
    email: str
    password: str

# In-memory storage
users = {}
ticks = {}

@app.get("/")
def home():
    return {"status": "running"}


@app.post("/signup")
def signup(user: User):
    email = user.email
    password = user.password

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
def login(user: User):
    email = user.email
    password = user.password

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


# IMPORTANT FOR RAILWAY
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
