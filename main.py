from fastapi import FastAPI

from service.pollution import PollutantService

app = FastAPI()


@app.get("/pollutants/{target_datetime}")
async def get(target_datetime: str, lat: float = 51.4231, lon: float = 5.4623):
    pollutant_service = PollutantService()
    current_pollutants = pollutant_service.get(target_datetime, lat, lon)
    return current_pollutants
