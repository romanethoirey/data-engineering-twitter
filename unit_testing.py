import unittest
import requests
import os
from bs4 import BeautifulSoup

class FlaskTest(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        self.sentence = {
            'input_tweet': "This is a test tweet."
        }
        
    def tearDown(self):
        pass
    
    def test_flask_page(self):
        sentence = {
            "sentence": self.sentence['input_tweet'],
            'form_type': 'analysis_sentence',
            "topN":"3"
        }
        response = requests.post('http://localhost:5000/', data=sentence)
        self.assertEqual(response.status_code, 200)        

    def test_input(self):
        sentence = {
            "sentence": self.sentence['input_tweet'],
            'form_type': 'analysis_sentence',
            "topN":"3"
        }
        response = requests.post('http://localhost:5000/', data=sentence)
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        input_tweet = soup.find(id='content').get_text()
        input_tweet = input_tweet.split('"')[1]
        self.assertEqual(str(input_tweet), sentence['sentence'])
        
    def test_tweets(self):
        sentence = {
            "sentence": self.sentence['input_tweet'],
            'form_type': 'analysis_sentence',
            "topN":"3"
        }
        response = requests.post('http://localhost:5000/', data=sentence)
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        answer_tweets = soup.find(id='tweets')
        answer_tweets = str(answer_tweets).split("<p")
        self.assertEqual(len(answer_tweets)-2, int(sentence['topN']))
        
if __name__ == "__main__":
    unittest.main()