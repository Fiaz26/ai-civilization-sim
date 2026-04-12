
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================
# APP
# =====================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# DATABASE (SQLite)
# =====================
engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =====================
# TABLE
# =====================
class UserDB(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    password = Column(String)
    credits = Column(Integer, default=10)

Base.metadata.create_all(bind=engine)

# =====================
# MODELS
# =====================
class User(BaseModel):
    email: str
    password: str

class Payment(BaseModel):
    api_key: str
    method: str
    amount: float
    note: str

# =====================
# ROUTES
# =====================

@app.get("/")
def home():
    return {"status": "running"}

# ---------------------
# SIGNUP
# ---------------------
@app.post("/signup")
def signup(user: User):
    db = SessionLocal()

    existing = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing:
        db.close()
        return {"status": "error", "message": "User exists"}

    new_user = UserDB(
        email=user.email,
        password=user.password,
        credits=10
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"status": "success", "api_key": user.email, "credits": 10}

# ---------------------
# LOGIN
# ---------------------
@app.post("/login")
def login(user: User):
    db = SessionLocal()

    existing = db.query(UserDB).filter(
        UserDB.email == user.email,
        UserDB.password == user.password
    ).first()

    db.close()

    if not existing:
        return {"status": "error"}

    return {
        "status": "success",
        "api_key": existing.email,
        "credits": existing.credits
    }

# ---------------------
# STEP (SIMULATION)
# ---------------------
@app.get("/step")
def step(api_key: str):
    db = SessionLocal()

    user = db.query(UserDB).filter(UserDB.email == api_key).first()
    if not user:
        db.close()
        return {"error": "invalid"}

    if user.credits <= 0:
        db.close()
        return {"error": "no credits"}

    user.credits -= 1
    db.commit()

    db.close()

    return {
        "tick": "running",
        "credits": user.credits
    }

# ---------------------
# PAYMENTS (STORED)
# ---------------------
payments = []

@app.post("/request-payment")
def request_payment(payment: Payment):
    payments.append(payment.dict())
    return {"status": "submitted"}

@app.get("/payments")
def get_payments():
    return payments
