import fastapi

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/insight")
def get_insight(data: dict):
    return {"Insight": "Insight"}
