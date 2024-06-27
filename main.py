from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.pollution import PollutantService
from service.mockmodel import MockModelService
import numpy as np

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', status_code=418)
async def root():
    return {"message": "I'm a teapot"}

@app.get("/pollutants/{target_datetime}")
async def get(target_datetime: str, lat: float = 51.4231, lon: float = 5.4623):
    pollutant_service = PollutantService()
    current_pollutants = pollutant_service.get(target_datetime, lat, lon)
    return current_pollutants

@app.get("/mock-predict")
async def predict():
    # load the data from the mock-prediction.npy file
    data = np.load("dataset/mockprediction.npy")
    mock_model_service = MockModelService(data)
    pm25, pm10, no2, o3 = mock_model_service.predict()
    return {"PM2.5": pm25, "PM10": pm10, "NO2": no2, "O3": o3}