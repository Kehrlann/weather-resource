import json
from typing import Union

class EmptyVersion:
    pass

class Version:
    weather: str = ""
    date: str = ""

    def __init__(self, weather: str, date: str) -> None:
        self.weather = weather
        self.date = date

    @staticmethod
    def fromJson(raw_data: str) -> Union['Version', EmptyVersion]:
        if not raw_data:
            return EmptyVersion()

        data = json.loads(raw_data)
        weather = data.get('weather') or Version.weather
        date = data.get('date') or Version.date
        return Version(weather, date)
