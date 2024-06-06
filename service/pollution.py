import math
from datetime import datetime, timedelta

import config
from dto.pollutants_response import PollutantResponse
from exception.failed_to_predict import FailedToPredictException
from repository.data_objects.prediction import Prediction
from repository.database.base import Entry, Location
from repository.db import Database
from repository.tno import TNORepository


class PollutantService:
    def __init__(self):
        self.tno = TNORepository()
        self.db = Database()

    def get(self, target_datetime: str, lat: float, lon: float) -> PollutantResponse:
        target_datetime = datetime.strptime(target_datetime, config.DATETIME_FORMAT)
        target_datetime = self._round_to_nearest_10_minutes(target_datetime)

        # Get entry from database
        entry = self.get_entry(target_datetime, lat, lon)
        if entry:
            return entry

        # Get new data from TNO and add it to the database
        self.update_tno_database(target_datetime)
        self.update_weather_database(target_datetime)

        # Retry getting entry from database
        entry = self.get_entry(target_datetime, lat, lon)
        if entry:
            return entry

        # If data not in database and not in TNO predict it
        passed_data, future_data = self._can_make_prediction()
        if len(passed_data) == 60 and future_data == 18:
            prediction = self._get_prediction(passed_data, future_data)
            return PollutantResponse.from_prediction(prediction)

        raise FailedToPredictException(
            "Model is not able to predict this far in to the future."
        )

    def update_tno_database(self, target_datetime: datetime):
        last_entry = self.db.get_last_entry()
        date = target_datetime
        if last_entry is not None:
            date = last_entry.date
        new_entries = self.tno.get_range(date, datetime.utcnow())
        self.db.add_all_entries(new_entries)

    def get_entry(
        self, target_datetime: datetime, lat: float, lon: float
    ) -> PollutantResponse | None:
        entry = self.db.get_entry(target_datetime)
        if entry:
            location = self._get_location_from_db_entry(entry, lat, lon)
            return PollutantResponse.from_location(location)
        return None

    def _get_prediction(
        self, passed_data: list[dict], future_data: list[dict]
    ) -> Prediction:
        # TODO: Use the model to make a prediction
        pass

    def _can_make_prediction(self) -> (list[dict], list[dict]):
        # TODO: get the needed data from tno and the weather service check if there is enough data
        return [], []

    def _get_location_from_db_entry(
        self, entry: Entry, lat: float, lon: float
    ) -> Location:
        best_location = None
        best_mag = 1000000

        for location in entry.locations:
            mag = self._get_magnitude((location.lat, location.lon), (lat, lon))
            if mag < best_mag:
                best_location = location
                best_mag = mag
        return best_location

    @staticmethod
    def _get_magnitude(start, to):
        x = pow(start[0] - to[0], 2)
        y = pow(start[1] - to[1], 2)
        return math.sqrt(x + y)

    @staticmethod
    def _round_to_nearest_10_minutes(target_datetime: datetime) -> datetime:
        minutes_past_last_10_minutes = target_datetime.minute % 10
        if minutes_past_last_10_minutes < 5:
            rounded_datetime = target_datetime - timedelta(
                minutes=minutes_past_last_10_minutes
            )
        else:
            rounded_datetime = target_datetime + timedelta(
                minutes=10 - minutes_past_last_10_minutes
            )
        rounded_datetime = rounded_datetime.replace(second=0)
        return rounded_datetime

    def update_weather_database(self, target_datetime: datetime):
        last_entry = self.db.get_last_weather()
        date = target_datetime
        if last_entry is not None:
            date = last_entry.date
        new_entries = self.weather.get_range(date, datetime.utcnow())
        self.db.add_all_weather(new_entries)
