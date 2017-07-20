import unittest

import {{ cookiecutter.project_slug }}

# @unittest.skip("skipped")
class CommonTestCase(unittest.TestCase):
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

    def GIVEN_this(self):
        pass

    def WHEN_that(self):
        pass

    def THEN_verify(self):
        pass