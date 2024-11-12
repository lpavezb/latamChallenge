import os
import fastapi

from dotenv import load_dotenv

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH", "../data/data.csv")
MODEL_PATH = os.environ.get("MODEL_PATH", "../0001.model")
THRESHOLD_IN_MINUTES = int(os.environ.get("THRESHOLD_IN_MINUTES", 15))


app = fastapi.FastAPI()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict() -> dict:
    return