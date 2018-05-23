import os.path
import tempfile
import unittest
from unittest.mock import patch

from weather.input import run_in
from weather.models import Version


class TestIn(unittest.TestCase):
    # TODO : metadata
    # TODO: copy file

    def setUp(self):
        self.version = Version("lovely weather", "2018-05-21T16:26:37Z")
        self.input_dir = tempfile.mkdtemp()

    def test_creates_txt_file(self):
        run_in(self.version, self.input_dir)

        weather_file = os.path.join(self.input_dir, "weather.txt")
        self.assertTrue(os.path.isfile(weather_file))

        file_content = None
        with open(weather_file, "r") as f:
            file_content = f.read()

        self.assertEqual(file_content, "lovely weather")

    def test_creates_json_file(self):
        run_in(self.version, self.input_dir)

        json_file = os.path.join(self.input_dir, "weather.json")
        self.assertTrue(os.path.isfile(json_file))

        file_content = None
        with open(json_file, "r") as f:
            file_content = f.read()

        self.assertEqual(
            file_content,
            '{"weather": "lovely weather", "date": "2018-05-21T16:26:37Z"}'
        )


if __name__ == '__main__':
    unittest.main()
