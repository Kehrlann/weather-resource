import unittest
from weather.models import Version, EmptyVersion, Source, load_source_version


class TestVersion(unittest.TestCase):

    def test_loads_from_json(self):
        version = Version.from_json(
            {"weather": "sunny", "date": "2018-05-21T16:26:37Z"}
        )
        self.assertEqual(version.weather, "sunny")
        self.assertEqual(version.date, "2018-05-21T16:26:37Z")

    def test_loads_from_json_empty_version(self):
        version = Version.from_json({})
        self.assertIsInstance(version, EmptyVersion)


class TestSource(unittest.TestCase):
    def test_loads_city(self):
        source = Source.from_json({"city": "Paris, France"})
        self.assertEqual(source.city, "Paris, France")


class TestLoadingFromJson(unittest.TestCase):
    def test_loads(self):
        source, version = load_source_version(
            """
            {
                "source" : {
                    "city" : "Cormeilles en Parisis, France"
                },
                "version" : {
                    "weather": "sunny",
                    "date": "2018-05-21T16:26:37Z"
                }
            }
            """
        )
        self.assertEqual(source.city, "Cormeilles en Parisis, France")
        self.assertEqual(version.weather, "sunny")

    def test_load_empty_version(self):
        _, version = load_source_version(
            """
             {
                "source" : {
                    "city" : "Cormeilles en Parisis, France"
                }
            }
            """
        )
        self.assertIsInstance(version, EmptyVersion)


if __name__ == '__main__':
    unittest.main()
