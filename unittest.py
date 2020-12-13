import unittest
import requests
import os
from bs4 import BeautifulSoup

class FlaskTest(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        self.sentence = {
        'input_tweet': "Climate change has been created by the chinese terrorists to export their 5G mobile phones into our american households."
        }
        
        def tearDown(self):
            pass
        
if __name__ == "__main__":
    unittest.main()