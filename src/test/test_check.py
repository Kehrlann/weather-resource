import unittest
from datetime import datetime
from unittest.mock import patch

from weather.check import run_check
from weather.models import EmptyVersion, Source, Version


class TestCheck(unittest.TestCase):

    def setUp(self):
        self.created_time = '2018-05-21T16:26:37Z'
        self.source = Source("tokyo, japan")

    def test_fetches_from_yahoo_weather(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)
            run_check(self.source, EmptyVersion())

            mock_fetch.assert_called_once_with(self.source)

    def test_new_version_on_weather_change(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)

            versions = run_check(self.source, Version("cloudy", ""))
            self.assertGreaterEqual(len(versions), 1)

    def test_no_version_on_same_weather(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)

            versions = run_check(self.source, Version("sunny", ""))
            self.assertEqual(len(versions), 0)

    def test_new_version_when_previous_empty(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)

            versions = run_check(self.source, EmptyVersion())
            self.assertEqual(len(versions), 1)


if __name__ == '__main__':
    unittest.main()
