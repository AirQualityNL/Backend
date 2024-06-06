from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Location:
    lat: float
    lon: float
    pm1: float
    pm25: float
    pm10: float
    no2: float


@dataclass
class Entry:
    date: datetime
    locations: List[Location]


@dataclass
class Weather:
    dateTime: datetime
    global_radiation_avg: float
    global_radiation_min: float
    global_radiation_max: float
    sunshine_duration: float
    wind_speed_avg: float
    wind_speed_avg_10m: float
    wind_direction_avg: float
    Wind_direction_std: float
    wind_speed_std: float
    wind_speed_max_10m: float
    wind_speed_max_10m_aviation: float
    wind_speed_max: float
    wind_speed_max_aviation: float
    squall_indicator: float
    temp: float
    temp_min_10cm: float
    dew_point: float
    temp_min: float
    wet_bulb_temp: float
    temp_max: float
    humidity: float
    precipitation_weather: float
    precipitation_electric: float
    weather_code: float
    intensity_precipitation_weather: float
    intensity_precipitation_electric: float
    lat: float
    lon: float
