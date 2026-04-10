from fastapi import FastAPI
import random

app = FastAPI()

# -----------------------
# WORLD (MULTI CIVS)
# -----------------------
world = {
    "tick": 0,
    "civilizations": [
        {
            "id": "Earth-Alpha",
            "gdp": 1000,
            "agents": 10,
            "companies": 3,
            "alive": True
        },
        {
            "id": "Earth-Beta",
            "gdp": 800,
            "agents": 8,
            "companies": 2,
            "alive": True
        }
    ]
}

# -----------------------
# UPDATE ONE CIV
# -----------------------
def update_civ(civ):
    if not civ["alive"]:
        return

    # agents impact economy
    agent_power = civ["agents"] * random.randint(1, 5)

    # companies impact economy
    company_power = civ["companies"] * random.randint(5, 15)

    # randomness (events)
    event = random.randint(-20, 30)

    civ["gdp"] += agent_power + company_power + event

    # population growth
    civ["agents"] += random.choice([0, 1])

    # company growth/failure
    change = random.choice([-1, 0, 1])
    civ["companies"] += change
    if civ["companies"] < 1:
        civ["companies"] = 1

    # collapse condition
    if civ["gdp"] < 300:
        civ["alive"] = False

# -----------------------
# SIMULATION STEP
# -----------------------
def step_world():
    world["tick"] += 1

    for civ in world["civilizations"]:
        update_civ(civ)

    return {
        "tick": world["tick"],
        "civilizations": world["civilizations"]
    }

# -----------------------
# API
# -----------------------
@app.get("/step")
def step():
    return step_world()

@app.get("/state")
def state():
    return world
