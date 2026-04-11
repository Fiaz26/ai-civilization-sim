from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROOT =====
@app.get("/")
def home():
    return {"status": "AI Civilization API running"}

# ===== SIMULATION =====
try:
    from engine import run_simulation

    @app.get("/step")
    def step():
        return run_simulation()

except Exception as e:
    @app.get("/step")
    def step_error():
        return {"error": "engine failed", "detail": str(e)}

# ===== AUTH =====
try:
    from auth import create_user, login_user

    @app.post("/signup")
    def signup(data: dict):
        return {"api_key": create_user(data["email"], data["password"])}

    @app.post("/login")
    def login(data: dict):
        return login_user(data["email"], data["password"])

except Exception as e:
    @app.post("/signup")
    def signup_error():
        return {"error": "auth failed", "detail": str(e)}

# ===== USER PLAN =====
try:
    from billing import get_user_plan

    @app.get("/me")
    def me(api_key: str = Header(None)):
        return {"plan": get_user_plan(api_key)}

except Exception as e:
    @app.get("/me")
    def me_error():
        return {"error": "billing failed", "detail": str(e)}

# ===== PAYMENTS =====
try:
    from payments import create_payment, get_payments, approve_payment

    @app.post("/pay")
    def pay(data: dict):
        return create_payment(data)

    @app.get("/admin/payments")
    def admin_payments():
        return get_payments()

    @app.post("/admin/approve")
    def approve(payment_id: int):
        return approve_payment(payment_id)

except Exception as e:
    @app.post("/pay")
    def pay_error():
        return {"error": "payment failed", "detail": str(e)}
