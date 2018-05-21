import unittest
from unittest.mock import patch
from datetime import datetime
import json
from weather.check import check


class TestCheck(unittest.TestCase):
    def test_gets_data_from_request(self):
        with patch('requests.get') as mock_request:
            created_time = '2018-05-21T16:26:37Z'

            mock_request.return_value = FakeResponse.fromWeatherAndDate(
                "sunny",
                created_time
            )

            version = check()
            self.assertEqual(version.weather, "sunny")
            self.assertEqual(version.date, created_time)

    def test_contacts_yahoo(self):
        with patch('requests.get') as mock_request:
            check()
            mock_request.assert_called_once()
            url = mock_request.call_args[0]
            self.assertIn("https://query.yahooapis.com/v1/public/yql?q=", url)


class FakeResponse:
    status_code = 200
    content = "{}"

    def __init__(self, content="{}"):
        self.content = content

    @staticmethod
    def fromWeatherAndDate(weather: str, date: str = "") -> 'FakeResponse':
        return FakeResponse(
            '{ "item": { "condition" : "%s" }, "created": "%s" }'
            % (weather,
               date or datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        )

    def json(self):
        return json.loads(self.content)


if __name__ == '__main__':
    unittest.main()
