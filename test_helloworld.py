import unittest
from helloworld import main

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(main(), "Jenkins CICD deployed on Kubernetes by Chinenye Genevieve Onyema")

if __name__ == "__main__":
    unittest.main()
