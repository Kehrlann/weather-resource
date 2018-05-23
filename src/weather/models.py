import json
from typing import Dict, Tuple, Union


class EmptyVersion:
    weather: str = ""
    date: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {}


class Version:
    weather: str = ""
    date: str = ""

    def __init__(self, weather: str, date: str) -> None:
        self.weather = weather
        self.date = date

    @staticmethod
    def from_json(data: Dict[str, str]) -> 'TVersion':
        if not data:
            return EmptyVersion()
        weather = data.get('weather') or Version.weather
        date = data.get('date') or Version.date
        return Version(weather, date)

    def to_dict(self) -> Dict[str, str]:
        return {"weather": self.weather, "date": self.date}


TVersion = Union[Version, EmptyVersion]


class Source:
    city: str = ""
    weather_change_only: bool = False

    def __init__(self, city: str, weather_change_only: bool = False) -> None:
        self.city = city
        self.weather_change_only = weather_change_only

    @staticmethod
    def from_json(data: Dict[str, str]) -> 'Source':
        city = data.get('city') or Source.city
        weather_change_only = bool(data.get('weather_change_only')) or Source.weather_change_only
        return Source(city, weather_change_only)


def load_source_version(raw_data: str) -> Tuple[Source, TVersion]:
    parsed_input = json.loads(raw_data)
    source_json = parsed_input.get("source")
    version_json = parsed_input.get("version")
    return Source.from_json(source_json), Version.from_json(version_json)
