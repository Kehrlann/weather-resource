import weather.yahoo_weather as yahoo_weather
from weather.models import Source, Version

def run_in(source: Source) -> Version:
    return yahoo_weather.fetch(source)

if __name__ == "__main__":
    pass

