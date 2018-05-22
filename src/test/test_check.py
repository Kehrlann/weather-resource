import json
import unittest
from datetime import datetime
from unittest.mock import patch

from weather.check import check
from weather.models import EmptyVersion, Source, Version


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

            version = check(self.tokyo)[0]
            self.assertEqual(version.weather, "sunny")
            self.assertEqual(version.date, self.created_time)

    def test_contacts_yahoo(self):
        with patch('requests.get') as mock_request:
            check(self.tokyo)
            url = mock_request.call_args[0]
            self.assertIn("https://query.yahooapis.com/v1/public/yql", url)

    def test_checks_weather_for_city(self):
        with patch('requests.get') as mock_request:
            check(Source("paris, france"))
            yql = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="paris, france")'
            url = mock_request.call_args[0]
            self.assertIn({'q': yql, 'format': 'json'}, url)

    def test_new_version_on_weather_change(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            versions = check(self.tokyo, Version("cloudy", ""))
            self.assertGreaterEqual(len(versions), 1)

    def test_no_version_on_same_weather(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            versions = check(self.tokyo, Version("sunny", ""))
            self.assertEqual(len(versions), 0)

    def test_new_version_when_previous_empty(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            versions = check(self.tokyo, EmptyVersion())
            self.assertEqual(len(versions), 1)


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
