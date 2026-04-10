from fastapi import FastAPI
import random

app = FastAPI()

state = {
    "tick": 0,
    "gdp": 1000,
    "agents": 10,
    "companies": 3
}

def step_world():
    state["tick"] += 1
    state["gdp"] += random.randint(-30, 80)
    return state

@app.get("/step")
def step():
    return step_world()

@app.get("/state")
def get_state():
    return state
