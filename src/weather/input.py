import json
from pathlib import Path

import weather.yahoo_weather as yahoo_weather
from weather.models import Version


def run_in(version: Version, input_dir: str) -> None:
    base_path = Path(input_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    weather_file = base_path / "weather.txt"
    with open(weather_file, "w") as f:
        f.write(version.weather)

    json_file = base_path / "weather.json"
    with open(json_file, "w") as f:
        json_data = json.dumps(version.to_dict())
        f.write(json_data)


if __name__ == "__main__":
    pass
