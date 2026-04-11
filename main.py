tick = 0

def run_simulation():
    global tick
    tick += 1

    return {
        "tick": tick,
        "civilizations": [
            {
                "id": "Earth-Alpha",
                "gdp": 1000 + tick * 50,
                "agents": 10 + tick,
                "companies": 2 + tick // 2,
                "alive": True
            },
            {
                "id": "Earth-Beta",
                "gdp": 900 + tick * 40,
                "agents": 8 + tick,
                "companies": 1 + tick // 3,
                "alive": True
            }
        ],
        "global_trade": tick * 20
    }
