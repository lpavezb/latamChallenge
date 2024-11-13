import os
import pandas as pd

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH", "data/data.csv")
MODEL_PATH = os.environ.get("MODEL_PATH", "0001.model")
THRESHOLD_IN_MINUTES = int(os.environ.get("THRESHOLD_IN_MINUTES", 15))


app = FastAPI()

from challenge.models import Flights
from challenge.model import DelayModel

model = DelayModel()
model.load_model()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.body},
    )

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: Flights) -> dict:
    try:
        data = [flight.model_dump() for flight in request.flights]
        features = model.preprocess(pd.DataFrame(data))
        preds = model.predict(features)
        return JSONResponse(
            status_code=200, 
            content={
                "predict": preds
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content=f"server error: {str(e)}")