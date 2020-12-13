import re
import time
import pickle

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

app = Flask(__name__)
start_time = time.time()

stopwords = ['the', 'and', 'are', 'a']

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
    print(query_tf)
    
    index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in corpus]],similarity_matrix)

    doc_similarity_scores = index[query_tf]

    # Output the sorted similarity scores and documents
    sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
    print("Tweets sorted")
    
    similar_tweets = []
    for i, idx in enumerate(sorted_indexes):
        if i > int(n):
            break
        similar_tweets.append(f'{doc_similarity_scores[idx]:0.3f} \t {documents[idx]}')
    return similar_tweets

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        details = request.form
        if (details['form_type'] == 'analysis_sentence'):
            content = details['sentence']
            tweets = get_N_Most_Similar_Tweets(details['sentence'], details['topN'])
            return render_template('index.html', content=content, tweets=tweets)
    return render_template('index.html', content='', tweets=-1)

if __name__ == '__main__':
    app.run(host='0.0.0.0')