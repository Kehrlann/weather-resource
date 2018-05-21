from typing import Any, Sequence
from datetime import datetime
import requests
import json

from weather.models import Version

def check() -> Version:
    url = 'https://query.yahooapis.com/v1/public/yql?q='
    response = requests.get(url).json()
    weather = response['item']['condition']
    return Version(weather, response['created'])