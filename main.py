from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "base working"}

# ADD ONLY THIS
from engine import run_simulation

@app.get("/step")
def step():
    return run_simulation()
    
