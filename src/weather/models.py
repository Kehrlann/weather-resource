import json
from typing import Union


class EmptyVersion:
    weather: str = ""


class Version:
    weather: str = ""
    date: str = ""

    def __init__(self, weather: str, date: str) -> None:
        self.weather = weather
        self.date = date

    @staticmethod
    def from_json(raw_data: str) -> Union['Version', EmptyVersion]:
        if not raw_data:
            return EmptyVersion()

        data = json.loads(raw_data)
        weather = data.get('weather') or Version.weather
        date = data.get('date') or Version.date
        return Version(weather, date)


TVersion = Union[Version, EmptyVersion]


class Source:
    city: str = ""

    def __init__(self, city: str) -> None:
        self.city = city

    @staticmethod
    def from_json(raw_data: str) -> 'Source':
        data = json.loads(raw_data)
        return Source(data.get('city') or Source.city)
