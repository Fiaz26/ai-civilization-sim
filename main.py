from fastapi import FastAPI

app = FastAPI()

tick = 0

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/step")
def step():
    global tick
    tick += 1

    return {
        "tick": tick,
        "gdp": 1000 + tick * 10,
        "agents": 10 + tick,
        "companies": 2 + tick // 2,
        "alive": True
    }
