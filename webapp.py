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

from flask import Flask, request, render_template

app = Flask(__name__)

def preprocess(doc):
    """
    Tokenize, clean up input document string
    Parameters:
        - doc : the string to be preprocessed
    """
    doc = re.sub(r'pic.twitter.com\/+\w{0,}', 'picture_token', doc)
    doc = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

df = pd.read_csv('tweets.csv', index_col=False)
tweets = df['text']
#del df

print("Tweets loaded")

######################

print("Start preprocessing")

documents = tweets
stopwords = ['the', 'and', 'are', 'a']

# Preprocess the documents, including the query string
corpus = [preprocess(document) for document in documents]

print("Preprocessing finished")

###############################

print("Loading model")
# Load the model: this is a big file, can take a while to download and open
glove = api.load("glove-wiki-gigaword-50")    
similarity_index = WordEmbeddingSimilarityIndex(glove)

print("Model loaded")

#####################

print("Building term dictionary and similarity matrix")
# Build the term dictionary, TF-idf model
dictionary = Dictionary(corpus)
tfidf = TfidfModel(dictionary=dictionary)

# Create the term similarity matrix.  
similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

print("Term dictionary and similarity matrix created")

######################################################

def get_N_Most_Similar_Tweets(sentence, n=20):
    print(n, type(n))
    
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