import unittest
from weather.models import Version, EmptyVersion, Source


class TestVersion(unittest.TestCase):

    def test_loads_from_json(self):
        version = Version.from_json(
            '{ "weather": "sunny", "date": "2018-05-21T16:26:37Z" }'
        )
        self.assertEqual(version.weather, "sunny")
        self.assertEqual(version.date, "2018-05-21T16:26:37Z")

    def test_loads_from_json_empty_version(self):
        version = Version.from_json("")
        self.assertIsInstance(version, EmptyVersion)


class TestSource(unittest.TestCase):
    def test_loads_city(self):
        source = Source.from_json('{ "city": "Paris, France" }')
        self.assertEqual(source.city, "Paris, France")


if __name__ == '__main__':
    unittest.main()
