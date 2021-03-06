import sys
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch

from weather.check import output_versions, run_check
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
            source = Source("tokyo, japan", True)

            versions = run_check(source, Version("sunny", ""))
            self.assertEqual(len(versions), 0)

    def test_new_version_on_same_weather(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)

            versions = run_check(self.source, Version(
                "sunny", "1970-01-01T00:00:00Z"))
            self.assertEqual(len(versions), 1)

    def test_new_version_when_previous_empty(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)

            versions = run_check(self.source, EmptyVersion())
            self.assertEqual(len(versions), 1)


class TestPrintVersions(unittest.TestCase):
    def setUp(self):
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_outputs_versions(self):
        output_versions([Version("a", "one"), Version("b", "two")])
        captured_output = self.stdout.getvalue().strip()
        self.assertEqual(
            captured_output, '[{"weather": "a", "date": "one"}, {"weather": "b", "date": "two"}]')


if __name__ == '__main__':
    unittest.main()
