from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN use it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ THEN routes
@app.get("/")
def home():
    return {"status": "API running"}
# -----------------------
# WORLD STATE
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
            "gdp": 900,
            "agents": 9,
            "companies": 2,
            "alive": True
        }
    ],
    "trade_volume": 0
}

# -----------------------
# UPDATE CIV ECONOMY
# -----------------------
def update_civ(civ):
    if not civ["alive"]:
        return

    production = civ["agents"] * random.randint(1, 5)
    business = civ["companies"] * random.randint(5, 15)
    event = random.randint(-15, 25)

    civ["gdp"] += production + business + event

    civ["agents"] += random.choice([0, 1])

    civ["companies"] += random.choice([-1, 0, 1])
    if civ["companies"] < 1:
        civ["companies"] = 1

    if civ["gdp"] < 300:
        civ["alive"] = False

# -----------------------
# TRADE SYSTEM
# -----------------------
def trade_between(civ_a, civ_b):
    if not civ_a["alive"] or not civ_b["alive"]:
        return 0

    # trade strength based on economy size
    trade_value = int((civ_a["gdp"] + civ_b["gdp"]) * random.uniform(0.01, 0.03))

    # transfer effect
    if civ_a["gdp"] > civ_b["gdp"]:
        civ_a["gdp"] += trade_value
        civ_b["gdp"] += int(trade_value * 0.6)
    else:
        civ_b["gdp"] += trade_value
        civ_a["gdp"] += int(trade_value * 0.6)

    return trade_value

# -----------------------
# SIMULATION STEP
# -----------------------
def step_world():
    world["tick"] += 1
    world["trade_volume"] = 0

    # update civilizations
    for civ in world["civilizations"]:
        update_civ(civ)

    # trade phase (pairwise)
    civs = world["civilizations"]

    for i in range(len(civs)):
        for j in range(i + 1, len(civs)):
            trade_value = trade_between(civs[i], civs[j])
            world["trade_volume"] += trade_value

    return {
        "tick": world["tick"],
        "civilizations": world["civilizations"],
        "global_trade": world["trade_volume"]
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
