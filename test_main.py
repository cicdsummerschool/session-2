"""
This is a simple test suite for the hello_world function
"""

import unittest
from unittest.mock import patch
import io
from main import hello_world


class TestHelloWorld(unittest.TestCase):
    """
    Test the hello_world function
    """

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hello_world(self, mock_stdout):
        """
        Test the hello_world function
        """
        hello_world()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
