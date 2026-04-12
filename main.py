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
ticks = {}
payments = []

@app.get("/")
def home():
    return {"status": "running"}


@app.post("/signup")
def signup(user: User):
    if user.email in users:
        return {"status": "error"}

    users[user.email] = {
        "password": user.password,
        "credits": 10,
        "plan": "free"
    }

    return {
        "status": "success",
        "api_key": user.email,
        "credits": 10
    }


@app.post("/login")
def login(user: User):
    if user.email in users and users[user.email]["password"] == user.password:
        return {
            "status": "success",
            "api_key": user.email,
            "credits": users[user.email]["credits"],
            "plan": users[user.email]["plan"]
        }

    return {"status": "error"}


@app.get("/step")
def step(api_key: str):
    if api_key not in users:
        return {"error": "invalid"}

    if users[api_key]["credits"] <= 0:
        return {"error": "no credits"}

    users[api_key]["credits"] -= 1
    ticks[api_key] = ticks.get(api_key, 0) + 1

    return {
        "tick": ticks[api_key],
        "credits_left": users[api_key]["credits"],
        "plan": users[api_key]["plan"]
    }


# 💰 SUBMIT PAYMENT REQUEST
import json
import os

PAYMENT_FILE = "payments.json"

def load_payments():
    if os.path.exists(PAYMENT_FILE):
        with open(PAYMENT_FILE, "r") as f:
            return json.load(f)
    return []

def save_payments(data):
    with open(PAYMENT_FILE, "w") as f:
        json.dump(data, f)

payments = load_payments()
@app.post("/request-payment")
def request_payment(payment: Payment):
    payments.append(payment.dict())
    save_payments(payments)

    return {"status": "submitted"}
    @app.get("/payments")
def get_payments():
    return payments

# 🧑‍💼 ADMIN APPROVAL
@app.post("/approve")
def approve(index: int):
    if index >= len(payments):
        return {"error": "invalid"}

    payment = payments[index]
    user = payment["user"]

    users[user]["credits"] += 100
    users[user]["plan"] = "pro"
    payment["status"] = "approved"

    return {"status": "approved"}


# 📋 VIEW PAYMENTS
@app.get("/payments")
def get_payments():
    return payments
