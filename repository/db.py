from dataclasses import asdict
from datetime import datetime

from pymongo import DESCENDING
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import config
from repository.database.base import Entry, Location, Weather


class Database:
    def __init__(self):
        self.client = MongoClient(config.DB_URI, server_api=ServerApi("1"))
        self.db = self.client[config.DB_NAME]
        self.tno_collection = self.db["tno"]
        self.weather_collection = self.db["weather"]

    # TNO pollution
    def add_entry(self, entry: Entry):
        entry_dict = asdict(entry)
        entry_dict["locations"] = [asdict(loc) for loc in entry.locations]
        self.tno_collection.insert_one(entry_dict)

    def add_all_entries(self, entries: list[Entry]):
        for entry in entries:
            self.add_entry(entry)

    def get_entry(self, date: datetime) -> Entry | None:
        str_date = date.strftime("%Y-%m-%dT%H:%M:%S")
        date_document = self.tno_collection.find_one({"date": str_date})
        if date_document:
            return self._data_doc_to_entry(date_document)
        return None

    def get_last_entry(self) -> Entry | None:
        date_document = self.tno_collection.find_one(sort=[("date", DESCENDING)])
        if date_document:
            return self._data_doc_to_entry(date_document)
        return None

    def _data_doc_to_entry(self, data_doc) -> Entry:
        locations = [Location(**loc) for loc in data_doc["locations"]]
        date = datetime.strptime(data_doc["date"], config.DATETIME_FORMAT)
        return Entry(date=date, locations=locations)

    # Weather data
    def add_weather(self, weather: Weather):
        self.weather_collection.insert_one(asdict(weather))

    def add_all_weather(self, weather_entries: list[Weather]):
        for weather in weather_entries:
            self.add_weather(weather)
