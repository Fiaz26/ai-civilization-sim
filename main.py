from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

users = {}

@app.post("/signup")
def signup(user: User):
    if user.email in users:
        return {"status": "error"}

    users[user.email] = {
        "password": user.password,
        "credits": 10
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
            "credits": users[user.email]["credits"]
        }

    return {"status": "error"}
