from fastapi import FastAPI

from service.pollution import PollutantService

app = FastAPI()

@app.get('/', status_code=418 )
async def root():
    return {"message": "I'm a teapot"}

@app.get("/pollutants/{target_datetime}")
async def get(target_datetime: str, lat: float = 51.4231, lon: float = 5.4623):
    pollutant_service = PollutantService()
    current_pollutants = pollutant_service.get(target_datetime, lat, lon)
    return current_pollutants

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)