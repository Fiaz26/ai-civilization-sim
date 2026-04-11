from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ===== IMPORT MODULES =====
from engine import run_simulation
from auth import create_user, login_user
from billing import get_user_plan
from payments import create_payment, get_payments, approve_payment

# ===== CREATE APP =====
app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELS =====
class User(BaseModel):
    email: str
    password: str

class Payment(BaseModel):
    txn_id: str

# ===== ROOT =====
@app.get("/")
def home():
    return {"status": "API running"}

# ===== SIMULATION =====
@app.get("/step")
def step():
    return run_simulation()

# ===== AUTH =====
@app.post("/signup")
def signup(user: User):
    api_key = create_user(user.email, user.password)
    return {"api_key": api_key}

@app.post("/login")
def login(user: User):
    return login_user(user.email, user.password)

# ===== USER PLAN =====
@app.get("/me")
def me(api_key: str = Header(None)):
    return {"plan": get_user_plan(api_key)}

# ===== PAYMENT =====
@app.post("/pay")
def pay(p: Payment, api_key: str = Header(None)):
    return create_payment(p.txn_id, api_key)

# ===== ADMIN =====
@app.get("/admin/payments")
def admin_payments():
    return get_payments()

@app.post("/admin/approve")
def approve(payment_id: int):
    return approve_payment(payment_id)
