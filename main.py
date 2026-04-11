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
    if user.email in fake_users:
        return {"error": "User exists"}

    fake_users[user.email] = user.password
    return {"message": "signup success"}
    @app.post("/login")
def login(user: User):
    if fake_users.get(user.email) == user.password:
        return {"message": "login success", "api_key": user.email}
    return {"error": "invalid credentials"}
    
