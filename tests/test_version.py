import unittest

import tradingdb


class VersionTestCase(unittest.TestCase):
    """Version tests"""

    def test_version(self):
        """check tradingdb exposes a version attribute"""
        self.assertTrue(hasattr(tradingdb, "__version__"))
        self.assertIsInstance(tradingdb.__version__, str)


if __name__ == "__main__":
    unittest.main()
