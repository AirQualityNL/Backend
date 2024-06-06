from repository.data_objects.prediction import Prediction
from repository.database.base import Location


class PollutantResponse:
    def __init__(self):
        self.type: str = ""
        self.lat: float = 0
        self.lon: float = 0
        self.pm1: float = 0
        self.pm25: float = 0
        self.pm10: float = 0
        self.no2: float = 0

    @classmethod
    def from_location(cls, location: Location):
        instance = cls()
        instance.type = "db"
        instance.lat = location.lat
        instance.lon = location.lon
        instance.pm1 = location.pm1
        instance.pm25 = location.pm25
        instance.pm10 = location.pm10
        instance.no2 = location.no2
        return instance

    @classmethod
    def from_prediction(cls, prediction: Prediction):
        instance = cls()
        instance.type = "prediction"
        instance.lat = prediction.lat
        instance.lon = prediction.lon
        instance.pm1 = prediction.pm1
        instance.pm25 = prediction.pm25
        instance.pm10 = prediction.pm10
        instance.no2 = prediction.no2
        return instance

    def to_dict(self):
        return {
            "type": self.type,
            "lat": self.lat,
            "lon": self.lon,
            "pm1": self.pm1,
            "pm25": self.pm25,
            "pm10": self.pm10,
            "no2": self.no2,
        }
