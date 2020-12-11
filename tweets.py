import re

import numpy as np
import pandas as pd
import gensim.downloader as api

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SoftCosineSimilarity
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.utils import simple_preprocess, simple_tokenize

def preprocess(doc):
    """
    Tokenize, clean up input document string
    Parameters:
        - doc : the string to be preprocessed
    """
    doc = re.sub(r'pic.twitter.com\/+\w{0,}', 'picture_token', doc)
    #doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    #doc = sub(r'<[^<>]+(>|$)', " ", doc)
    #doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

df = pd.read_csv('tweets.csv', index_col=False)
tweets = df['text']

#del df

print("Tweets loaded")

print("Start preprocessing")

documents = tweets
stopwords = ['the', 'and', 'are', 'a']

# Preprocess the documents, including the query string
corpus = [preprocess(document) for document in documents]

print("Preprocessing finished")

print("Loading model")
# Load the model: this is a big file, can take a while to download and open
glove = api.load("glove-wiki-gigaword-50")    
similarity_index = WordEmbeddingSimilarityIndex(glove)
