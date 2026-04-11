from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

fake_users = {}

@app.post("/signup")
def signup(user: User):
    email = user.email.lower()

    if email in fake_users:
        return {"status": "error", "message": "User exists"}

    fake_users[email] = user.password
    return {"status": "success", "api_key": email}
    
fetch(API + "/signup", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    email,
    password
  })
})fetch("https://ai-civilization-sim-production.up.railway.app/signup", {
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: JSON.stringify({email:"test@test.com", password:"1234"})
})
.then(r=>r.json())
.then(console.log)
.catch(console.error)
