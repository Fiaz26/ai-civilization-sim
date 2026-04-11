from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

# ===== IMPORT YOUR MODULES =====
from engine import run_simulation
from auth import create_user, login_user
from billing import get_user_plan
from payments import create_payment, get_payments, approve_payment

# ===== CREATE APP =====
app = FastAPI()

# ===== ENABLE CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROOT ROUTE =====
@app.get("/")
def home():
    return {"status": "AI Civilization API running"}

# ===== SIMULATION ROUTE =====
@app.get("/step")
def step():
    return run_simulation()

# ===== AUTH ROUTES =====
@app.post("/signup")
def signup(data: dict):
    api_key = create_user(data["email"], data["password"])
    return {"api_key": api_key}

@app.post("/login")
def login(data: dict):
    return login_user(data["email"], data["password"])

# ===== USER PLAN =====
@app.get("/me")
def me(api_key: str = Header(None)):
    plan = get_user_plan(api_key)
    return {"plan": plan}

# ===== PAYMENT ROUTE =====
@app.post("/pay")
def pay(data: dict):
    return create_payment(data)

# ===== ADMIN ROUTES =====
@app.get("/admin/payments")
def admin_payments():
    return get_payments()

@app.post("/admin/approve")
def approve(payment_id: int):
    return approve_payment(payment_id)
