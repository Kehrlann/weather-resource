import os.path

import weather.yahoo_weather as yahoo_weather
from weather.models import Source, Version


def run_in(source: Source, input_dir: str) -> None:
    version = yahoo_weather.fetch(source)
    weather_file = os.path.join(input_dir, "weather.txt")
    with open(weather_file, "w") as f:
        f.write(version.weather)


if __name__ == "__main__":
    pass
