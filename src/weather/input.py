import json
import sys
from pathlib import Path

import weather.yahoo_weather as yahoo_weather
from weather.models import TVersion, load_source_version


def run_in(version: TVersion, input_dir: str) -> None:
    base_path = Path(input_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    weather_file = base_path / "weather.txt"
    with open(weather_file, "w") as f:
        f.write(version.weather)

    json_file = base_path / "weather.json"
    with open(json_file, "w") as f:
        json_data = json.dumps(version.to_dict())
        f.write(json_data)


def output_version(version: TVersion) -> None:
    json_version = json.dumps({"version": version.to_dict()})
    print(json_version)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    source, version = load_source_version(sys.stdin.read())
    run_in(version, input_dir)

    output_version(version)
