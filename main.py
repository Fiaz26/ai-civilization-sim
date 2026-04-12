from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: str
    password: str

class Payment(BaseModel):
    api_key: str
    method: str
    amount: float
    note: str

users = {}
payments = []
ticks = {}

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/signup")
def signup(user: User):
    if user.email in users:
        return {"status": "error"}

    users[user.email] = {"password": user.password, "credits": 10}
    return {"status": "success", "api_key": user.email, "credits": 10}

@app.post("/login")
def login(user: User):
    if user.email in users and users[user.email]["password"] == user.password:
        return {"status": "success", "api_key": user.email, "credits": users[user.email]["credits"]}
    return {"status": "error"}

@app.post("/request-payment")
def request_payment(payment: Payment):
    payments.append(payment.dict())
    return {"status": "submitted"}

@app.get("/payments")
def get_payments():
    return payments
    @app.get("/step")
def step(api_key: str):
    if api_key not in users:
        return {"error": "invalid"}

    # prevent negative credits
    if users[api_key]["credits"] <= 0:
        return {"error": "no credits"}

    users[api_key]["credits"] -= 1

    # FIX: persist tick value
    ticks[api_key] = ticks.get(api_key, 0) + 1

    return {
        "tick": ticks[api_key],
        "credits": users[api_key]["credits"]
        }
