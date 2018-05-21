import json
from typing import Type


class Version:
    weather: str = ""
    date: str = ""

    def __init__(self, weather: str, date: str) -> None:
        self.weather = weather
        self.date = date

    @staticmethod
    def fromJson(raw_data: str) -> 'Version':
        if not raw_data:
            return Version()

        data = json.loads(raw_data)
        weather = data.get('weather') or Version.weather
        date = data.get('date') or Version.date
        return Version(weather, date)
