from typing import Any, List
from datetime import datetime
import requests
import json

from weather.models import Version, EmptyVersion, Source


def check(source: Source = None, previous_version: Version = None) -> List[Version]:
    url = 'https://query.yahooapis.com/v1/public/yql?q='
    response = requests.get(url).json()
    weather = response['item']['condition']
    return [Version(weather, response['created'])]
