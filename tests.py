import unittest
import requests
import pytest


class FlaskTest(unittest.TestCase):

    def test_register(self):
        response = requests.get("http://127.0.0.1:5000/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1> Welcome to Posty!</h1>' in response.text, True)

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>Where students can connect and learn!</h2>' in response.text, True)

    def test_posts(self):
        response = requests.get("http://127.0.0.1:5000/posts")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(response.url == "http://127.0.0.1:5000/login", True)


if __name__ == " __main__":
    unittest.main()
