from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ✅ 1. CREATE APP FIRST (MOST IMPORTANT)
app = FastAPI()

# ✅ 2. MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 3. MODELS
class User(BaseModel):
    email: str
    password: str

# ✅ 4. STORAGE
users = {}

# ✅ 5. ROUTES
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
