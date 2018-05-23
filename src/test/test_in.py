import unittest
from unittest.mock import patch

from weather.models import Version, Source
from weather.in_cmd import run_in


class TestIn(unittest.TestCase):
    # TODO : metadata
    # TODO: copy file

    def setUp(self):
        self.created_time = '2018-05-21T16:26:37Z'
        self.source = Source("tokyo, japan")

    def test_fetches_from_yahoo_weather(self):
        with patch('weather.yahoo_weather.fetch') as mock_fetch:
            mock_fetch.return_value = Version("sunny", self.created_time)
            run_in(self.source)

            mock_fetch.assert_called_once_with(self.source)


if __name__ == '__main__':
    unittest.main()
