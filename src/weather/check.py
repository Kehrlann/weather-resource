import json
import sys
from datetime import datetime
from typing import List, Union

import requests

from weather.models import EmptyVersion, Source, TVersion, Version, load_source_version


def run_check(source: Source, previous_version: TVersion = EmptyVersion()) -> List[Version]:
    url = 'https://query.yahooapis.com/v1/public/yql'
    query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % source.city
    response = requests.get(url, {'q': query, 'format': 'json'})
    data = response.json()['query']
    weather = data['results']['channel']['item']['condition']['text']

    if weather == previous_version.weather:
        return []

    return [Version(weather, data['created'])]


if __name__ == "__main__":
    source, version = load_source_version(sys.stdin.read())
    new_versions = run_check(source, version)
    print(json.dumps([v.to_dict() for v in new_versions]))
