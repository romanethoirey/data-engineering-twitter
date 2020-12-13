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

start_time = time.time()

df = pd.read_csv('data/tweets.csv', index_col=False)
tweets = df['text']

#del df

print("Tweets loaded")

print("Start preprocessing")

documents = tweets
file_doc_w = open("data/doc.pickle", 'wb')
pickle.dump(documents, file_doc_w)
file_doc_w.close()

stopwords = ['the', 'and', 'are', 'a']

# Preprocess the documents, including the query string
corpus = [preprocess(document) for document in documents]

file_corpus_w = open("data/corpus.pickle", 'wb')
pickle.dump(corpus, file_corpus_w)
file_corpus_w.close()
print("Preprocessing finished")

print(time.time() - start_time)
print("Loading model")
# Load the model: this is a big file, can take a while to download and open
glove = api.load("glove-wiki-gigaword-50")    
similarity_index = WordEmbeddingSimilarityIndex(glove)
file_sim_idx_w = open("data/sim_idx.pickle", 'wb')
pickle.dump(similarity_index, file_sim_idx_w)
file_sim_idx_w.close()

print("Model loaded")
print(time.time() - start_time)
#####################

print("Building term dictionary and similarity matrix")
# Build the term dictionary, TF-idf model
dictionary = Dictionary(corpus)
tfidf = TfidfModel(dictionary=dictionary)
file_tfidf_w = open("data/tfidf.pickle", 'wb')
pickle.dump(tfidf, file_tfidf_w)
file_tfidf_w.close()
file_dico_w = open("data/dico.pickle", 'wb')
pickle.dump(dictionary, file_dico_w)
file_dico_w.close()

# Create the term similarity matrix.  
similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)
file_sim_matrix_w = open("data/sim_matrix.pickle", 'wb')
pickle.dump(similarity_matrix, file_sim_matrix_w)
file_sim_matrix_w.close()

print("Term dictionary and similarity matrix created")
print(time.time() - start_time)
print("Finished")
######################################################