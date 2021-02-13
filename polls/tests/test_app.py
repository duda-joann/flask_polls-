import unittest
import requests
from flask import Flask
from polls.app.routes import app
url = 'http://127.0.0.1:5000/'


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = app
        print('Tests started')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tests finished')

    def test_app(self):
        self.assertIsInstance(self.app, Flask)
        self.assertEqual(app.debug, False)

    def test_main(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'What do you prefer?', response)
        self.assertIn(b'Please choose one band', response)


if __name__ == '__main__':
    unittest.main()
