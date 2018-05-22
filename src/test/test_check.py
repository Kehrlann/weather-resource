import unittest
from unittest.mock import patch
from datetime import datetime
import json
from weather.check import check
from weather.models import Version

class TestCheck(unittest.TestCase):

    def setUp(self):
        self.created_time = '2018-05-21T16:26:37Z'
        self.response_sunny = FakeResponse.from_weather_and_date(
            "sunny",
            self.created_time
        )

    def test_gets_data_from_request(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            version = check()[0]
            self.assertEqual(version.weather, "sunny")
            self.assertEqual(version.date, self.created_time)

    def test_contacts_yahoo(self):
        with patch('requests.get') as mock_request:
            check()
            url = mock_request.call_args[0]
            self.assertIn("https://query.yahooapis.com/v1/public/yql?q=", url)

    def test_produces_new_version_on_weather_change(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            versions = check(previous_version=Version("cloudy", ""))
            self.assertGreaterEqual(len(versions), 1)

    def test_no_new_version_on_same_weather(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = self.response_sunny

            versions = check(previous_version=Version("sunny", ""))
            self.assertTrue( len(versions) == 0)


class FakeResponse:
    status_code = 200
    content = "{}"

    def __init__(self, content="{}"):
        self.content = content

    @staticmethod
    def from_weather_and_date(weather: str, date: str = "") -> 'FakeResponse':
        return FakeResponse(
            '{ "item": { "condition" : "%s" }, "created": "%s" }'
            % (weather,
               date or datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        )

    def json(self):
        return json.loads(self.content)


if __name__ == '__main__':
    unittest.main()
