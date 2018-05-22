import requests
from weather.models import Source, Version

def fetch(source: Source) -> Version:
    url = 'https://query.yahooapis.com/v1/public/yql'
    query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % source.city
    response = requests.get(url, {'q': query, 'format': 'json'})
    data = response.json()['query']
    weather = data['results']['channel']['item']['condition']['text']

    return Version(weather, data['created'])