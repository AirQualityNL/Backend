import os

import pandas as pd
from datetime import datetime, timedelta

import requests

import config
from repository.database.base import Entry, Location


class TNORepository:
    def __init__(self):
        self.root_url: str = "https://ilm2.site.dustmonitoring.nl/download"
        self.location: str = (
            "p=531&p=521&p=542&p=543&p=553&p=544&p=545&p=532&p=533&p=554&p=534&p=535&p=546&p=536&p=556&p=522&p=557&p=547&p=549&p=524&p=537&p=525&p=526&p=539&p=551&p=540&p=558&p=527&p=528&p=529&p=530&p=560&p=561&p=562&p=563&p=564&p=565&p=566&p=567&p=568&p=569&p=570&p=571&p=574&p=575&p=576&p=577&p=578&s=10&s=11&s=128&s=129&s=130&s=145&s=146"
        )
        self.data_file: str = "temp"
        os.makedirs(self.data_file, exist_ok=True)
        self.pollutants = ["PM1", "PM2.5", "PM10", "NO2"]

    def get_range(
        self, start_date: datetime, end_date: datetime, segment: int = 10
    ) -> list[Entry]:
        segments = self.segment_date(start_date, end_date)

        entries = []
        for start, end in segments:
            new_entries = self.get_entries(start, end, segment)
            entries += new_entries
        entries = entries[::-1]
        return entries

    def get_entries(
        self, start_date: datetime, end_date: datetime, segment: int
    ) -> list[Entry]:
        data = requests.get(
            f"{self.root_url}?from={start_date.strftime('%Y-%m-%d')}&to={end_date.strftime('%Y-%m-%d')}&interval={segment}&align=1&type=csv-semicolon&{self.location}"
        )
        filepath = f"{self.data_file}/data.csv"
        with open(filepath, "+w") as file:
            file.write(data.text)
        df = pd.read_csv(filepath, index_col=False, sep=";")
        df = self.update_headers(df)
        df = self.values_to_numeric(df)
        df = self.ensure_10_entries(df)
        df = df.round(3)

        locations = []
        for col in df.columns:
            if col != "":
                locations.append(col.split("-")[0])

        locations = list(set(locations))

        dates = []
        for i, row in df.iterrows():
            new_locations = []
            for location in locations:
                lat = row.get(f"{location}-Lat")
                lon = row.get(f"{location}-Lon")
                pm1 = row.get(f"{location}-PM1")
                pm25 = row.get(f"{location}-PM2.5")
                pm10 = row.get(f"{location}-PM10")
                no2 = row.get(f"{location}-NO2")

                # Check if any value is None, if yes, skip adding to the list
                if None in (lat, lon, pm1, pm25, pm10, no2):
                    continue
                new_location = Location(lat, lon, pm1, pm25, pm10, no2)
                new_locations.append(new_location)

            date = i.to_pydatetime().strftime(config.DATETIME_FORMAT)
            entry = Entry(date, new_locations)
            dates.append(entry)

        return dates

    @staticmethod
    def segment_date(
        start_date: datetime, end_date: datetime
    ) -> list[(datetime, datetime)]:
        entries = []
        current_date = start_date
        while current_date < end_date:
            next_date = current_date + timedelta(days=30)
            if next_date > end_date:
                next_date = end_date
            entries.append((current_date, next_date))
            current_date = next_date
        return entries

    @staticmethod
    def update_headers(df: pd.DataFrame) -> pd.DataFrame:
        header_string = df.iloc[:2].values
        row_1 = [row.split(".")[0] for row in df.columns.tolist()]
        row_2 = header_string[0]
        new_columns = []
        for row1, row2 in zip(row_1, row_2):
            row1 = row1.replace("Unnamed: ", "")
            new_columns.append(f"{row1}-{row2}")
        # Remove the used rows
        df = df.iloc[2:]
        # Set new column names
        df.columns = new_columns
        df = df.rename(columns={"0-Tijd": "Tijd-UTC"})
        df = df.drop("1-Tijd", axis=1)
        return df

    @staticmethod
    def values_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace(",", ".", regex=True)
        df = df.apply(pd.to_numeric, errors="ignore")
        return df

    def ensure_10_entries(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Tijd-UTC"] = pd.to_datetime(df["Tijd-UTC"])
        df.set_index("Tijd-UTC", inplace=True)
        new_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq="10T")
        df = df.reindex(new_index)
        df = df.interpolate()
        df = df.ffill().bfill()
        return df
