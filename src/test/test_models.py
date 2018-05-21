import unittest
from weather.models import Version, EmptyVersion


class TestVersion(unittest.TestCase):

    def test_loads_from_json(self):
        version = Version.fromJson(
            '{ "weather": "sunny", "date": "2018-05-21T16:26:37Z" }'
        )
        self.assertEqual(version.weather, "sunny")
        self.assertEqual(version.date, "2018-05-21T16:26:37Z")

    def test_loads_from_json_empty_version(self):
        version = Version.fromJson("")
        self.assertIsInstance(version, EmptyVersion)

if __name__ == '__main__':
    unittest.main()
