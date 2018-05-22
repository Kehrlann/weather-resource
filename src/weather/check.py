import json
from datetime import datetime
from typing import List, Union

import requests

from weather.models import EmptyVersion, Source, TVersion, Version


def check(source: Source, previous_version: TVersion = EmptyVersion()) -> List[Version]:
    url = 'https://query.yahooapis.com/v1/public/yql'
    query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % source.city
    response = requests.get(url, {'q': query, 'format': 'json'})
    data = response.json()['query']
    weather = data['results']['channel']['item']['condition']['text']

    if weather == previous_version.weather:
        return []

    return [Version(weather, data['created'])]
