from fastapi import APIRouter
from models import User
from auth import create_user, verify_user
from database import cursor, conn

router = APIRouter()

# -------- AUTH --------
@router.post("/signup")
def signup(user: User):
    if create_user(user.email, user.password):
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "User exists"}


@router.post("/login")
def login(user: User):
    if verify_user(user.email, user.password):
        return {"status": "success", "api_key": user.email}
    return {"status": "error", "message": "Invalid credentials"}


# -------- SIMULATION --------
tick_store = {}

@router.get("/step")
def step(api_key: str):
    cursor.execute("SELECT credits FROM users WHERE email=?", (api_key,))
    user = cursor.fetchone()

    if not user:
        return {"error": "Invalid API key"}

    credits = user[0]

    if credits <= 0:
        return {"error": "Upgrade required"}

    tick_store[api_key] = tick_store.get(api_key, 0) + 1

    cursor.execute(
        "UPDATE users SET credits = credits - 1 WHERE email=?",
        (api_key,)
    )
    conn.commit()

    tick = tick_store[api_key]

    return {
        "tick": tick,
        "gdp": 1000 + tick * 10,
        "credits_left": credits - 1
    }


# -------- ADMIN --------
@router.get("/admin")
def admin():
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    return {"total_users": users}
