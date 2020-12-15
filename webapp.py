import re
import time
import pickle
import random

import numpy as np
import pandas as pd
import gensim.downloader as api

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SoftCosineSimilarity
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.utils import simple_preprocess, simple_tokenize

from flask import Flask, request, render_template

from prometheus_client import start_http_server, Counter, Gauge, Summary, Histogram
from multiprocessing.pool import ThreadPool

app = Flask(__name__)
start_time = time.time()

stopwords = ['the', 'and', 'are', 'a']

REQUESTS = Counter('twitter_app_calls_total', 'How many times the app was called')
EXCEPTIONS = Counter('twitter_app_exception_total', 'How many times the app caused an exception')
INPROGRESS = Gauge('twitter_app_inprogress', 'number of request in progress')
LAST = Gauge('twitter_app_last_time_seconds', 'the last time our app was called')
LATENCY_SUMMARY = Summary('twitter_app_latency_sum', 'the time needed for a request')
LATENCY_HISTOGRAM = Histogram('twitter_app_latency_hist', 'the time needed for a request',
                                buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9.0, 9.5, 10, 10.5, 11])


def preprocess(doc):
    """
    Tokenize, clean up input document string
    Parameters:
        - doc : the string to be preprocessed
    """
    doc = re.sub(r'pic.twitter.com\/+\w{0,}', 'picture_token', doc)
    doc = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

print("Loading data and corpus")

file_corpus_r = open("data/corpus.pickle",'rb')
corpus = pickle.load(file_corpus_r)
file_corpus_r.close()

file_doc_r = open("data/doc.pickle",'rb')
documents = pickle.load(file_doc_r)
file_doc_r.close()

file_dico_r = open("data/dico.pickle",'rb')
dictionary = pickle.load(file_dico_r)
file_dico_r.close()

file_corpus_r = open("data/corpus.pickle",'rb')
corpus = pickle.load(file_corpus_r)
file_corpus_r.close()

file_tfidf_r = open("data/tfidf.pickle",'rb')
tfidf = pickle.load(file_tfidf_r)
file_tfidf_r.close()

file_sim_idx_r = open("data/sim_idx.pickle",'rb')
similarity_index = pickle.load(file_sim_idx_r)
file_sim_idx_r.close()

file_sim_matrix_r = open("data/sim_matrix.pickle",'rb')
similarity_matrix = pickle.load(file_sim_matrix_r)
file_sim_matrix_r.close()

print("Data and corpus finished loading")
print(time.time() - start_time)

def get_N_Most_Similar_Tweets(sentence, n=20):
    """
    Return the n most similar tweets from a sentence
    Parameters:
        - sentence : the sentence you want similar tweets from
        - n : the number of tweets you want
    """
    # preprocess the input sentence
    query = preprocess(sentence)

    query_tf = tfidf[dictionary.doc2bow(query)]
    
    index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in corpus]],similarity_matrix)

    doc_similarity_scores = index[query_tf]

    # Output the sorted similarity scores and documents
    sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
    print("Tweets sorted")
    
    similar_tweets = []
    for i, idx in enumerate(sorted_indexes):
        if i >= int(n):
            break
        similar_tweets.append(f'{doc_similarity_scores[idx]:0.3f} \t {documents[idx]}')
    return similar_tweets

@app.route('/', methods=['GET', 'POST'])
def index():
    LAST.set(time.time())
    REQUESTS.inc()
    start = time.time()

    INPROGRESS.inc()

    if request.method == 'POST':
        details = request.form
        print(details)
        if (details['form_type'] == 'analysis_sentence'):
            content = details['sentence']
            tweets = get_N_Most_Similar_Tweets(details['sentence'], details['topN'])
            
            INPROGRESS.dec()
            LATENCY_SUMMARY.observe(time.time() - start)
            LATENCY_HISTOGRAM.observe(time.time() - start)
            return render_template('index.html', content=content, tweets=tweets)
    return render_template('index.html', content='', tweets=-1)

if __name__ == '__main__':
    # pool = ThreadPool(1)
    # pool.apply_async(start_http_server, (3630, ))
    start_http_server(8000)
    app.run(host='0.0.0.0')