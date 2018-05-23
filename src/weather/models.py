import json
from typing import Dict, Tuple, Union


class EmptyVersion:
    weather: str = ""

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

    def __init__(self, city: str) -> None:
        self.city = city

    @staticmethod
    def from_json(data: Dict[str, str]) -> 'Source':
        return Source(data.get('city') or Source.city)


def load_source_version(raw_data: str) -> Tuple[Source, TVersion]:
    parsed_input = json.loads(raw_data)
    source_json = parsed_input.get("source")
    version_json = parsed_input.get("version")
    return Source.from_json(source_json), Version.from_json(version_json)
