import unittest
from helloworld import main

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(main(), "Hello World! From Chinenye Genevieve Onyema: This simple web app is deployed on Kubernetes Cluster using Jenkins CICD pipeline")

if __name__ == "__main__":
    unittest.main()
