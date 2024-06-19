from fastapi import FastAPI
import numpy as np
from keras.models import load_model

from service.pollution import PollutantService
from service.model import PollutantModel

app = FastAPI()

@app.get('/', status_code=418 )
async def root():
    return {"message": "I'm a teapot"}

@app.get("/pollutants/{target_datetime}")
async def get(target_datetime: str, lat: float = 51.4231, lon: float = 5.4623):
    pollutant_service = PollutantService()
    current_pollutants = pollutant_service.get(target_datetime, lat, lon)
    return current_pollutants

@app.get("/model")
async def get_model_summary():
    model = PollutantModel(load_model("model/pollutant_model.keras"))
    return {"summary": model.summary()}

@app.get("/test_prediction")
async def test_prediction():
    model = PollutantModel(load_model("model/pollutant_model.keras"))
    data = np.load("model/sequence.npy")
    forecasted_weather = np.load("model/future_sequence.npy")
    return {"result": model.predict(data, forecasted_weather)}