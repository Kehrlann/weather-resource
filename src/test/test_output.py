import json
import sys
import unittest
from io import StringIO

from weather.output import output_version


class TestPrintVersion(unittest.TestCase):
    def setUp(self):
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_outputs_version(self):
        output_version()
        captured_output = self.stdout.getvalue().strip()
        json_output = json.loads(captured_output)
        self.assertEqual(json_output['version']['weather'],
                         "Really, you shouldn't be trying to change the weather, friend.")


if __name__ == '__main__':
    unittest.main()
