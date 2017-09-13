import unittest
from unittest.mock import Mock, patch
import asyncio

import xmlrunner

import {{ cookiecutter.project_slug }}
from test import common


# @unittest.skip("skipped")
class SimpleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    async def async_setUp(self):
        pass

    async def async_tearDown(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_this(self):
        self.assertEqual(1,2)



if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)