from fastapi import FastAPI
import random

app = FastAPI()

state = {
    "tick": 0,
    "gdp": 1000,
    "agents": 10,
    "companies": 3
}

def simulate():
    state["tick"] += 1
    state["gdp"] += random.randint(-50, 100)
    state["companies"] += random.choice([-1, 0, 1])
    if state["companies"] < 1:
        state["companies"] = 1
    return state

@app.get("/step")
def step():
    return simulate()

@app.get("/state")
def get_state():
    return state
