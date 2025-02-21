import unittest
from helloworld import main

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(main(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()