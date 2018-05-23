import os.path
import tempfile
import unittest
from unittest.mock import patch

from weather.input import run_in
from weather.models import Source, Version


class TestIn(unittest.TestCase):
    # TODO : metadata
    # TODO: copy file

    def setUp(self):
        self.created_time = '2018-05-21T16:26:37Z'
        self.source = Source("tokyo, japan")
        self.input_dir = tempfile.mkdtemp()

    def test_fetches_from_yahoo_weather(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)
            run_in(self.source, self.input_dir)

            mock_fetch.assert_called_once_with(self.source)

    def test_creates_txt_file(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version(
                "lovely weather", self.created_time)
            run_in(self.source, self.input_dir)

            weather_file = os.path.join(self.input_dir, "weather.txt")
            self.assertTrue(os.path.isfile(weather_file))

            file_content = None
            with open(weather_file, "r") as f:
                file_content = f.read()

            self.assertEqual(file_content, "lovely weather")


if __name__ == '__main__':
    unittest.main()
