import json
import unittest
from datetime import datetime
from unittest.mock import patch

import weather.yahoo_weather as yahoo_weather
from weather.models import  Source, Version


class TestCheck(unittest.TestCase):

    def setUp(self):
        self.created_time = '2018-05-21T16:26:37Z'
        self.response_sunny = FakeResponse.from_weather_and_date(
            "sunny",
            self.created_time
        )
        self.tokyo = Source("tokyo, japan")

    def test_gets_data_from_request(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            version = yahoo_weather.fetch(self.tokyo)
            self.assertEqual(version.weather, "sunny")
            self.assertEqual(version.date, self.created_time)

    def test_contacts_yahoo(self):
        with patch('requests.get') as mock_request:
            yahoo_weather.fetch(self.tokyo)
            url = mock_request.call_args[0]
            self.assertIn("https://query.yahooapis.com/v1/public/yql", url)

    def test_checks_weather_for_city(self):
        with patch('requests.get') as mock_request:
            yahoo_weather.fetch(Source("paris, france"))
            yql = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="paris, france")'
            url = mock_request.call_args[0]
            self.assertIn({'q': yql, 'format': 'json'}, url)

class FakeResponse:
    status_code = 200
    content = "{}"

    def __init__(self, content="{}"):
        self.content = content

    @staticmethod
    def from_weather_and_date(weather: str, date: str = "") -> 'FakeResponse':
        return FakeResponse(
            """{
                "query":
                {
                    "created": "%s",
                    "results": {
                        "channel" : {
                            "item": {
                                "condition" : { "text": "%s" }
                            }
                        }
                    }
                }
            }"""
            % (date or datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
               weather)
        )

    def json(self):
        return json.loads(self.content)


if __name__ == '__main__':
    unittest.main()
