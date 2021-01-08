import numpy as np
import time
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import FeatureHasher
from collections import defaultdict

# 'and', 'drawing', 'attention', 'to'
# 'and drawing', 'drawing attention', 'attention to'
# 'and drawing attention', 'drawing attention to'

categories = [
    'alt.atheism',
    'comp.graphics',
]

# Uncomment the following line to use a larger set (11k+ documents)
categories = None

print("Loading 20 newsgroups training data")
news = fetch_20newsgroups(subset='all', categories=categories)

raw_data = news.data
data_size_mb = sum(len(s.encode('utf-8')) for s in raw_data) / 1e6
print("%d documents - %0.3fMB" % (len(raw_data), data_size_mb))
print()
# news.data is raw text, news.target is target labels

X_train_text, X_test_text, y_train, y_test = train_test_split(news.data, news.target, random_state=0)


def tokens_ngram(doc, ngrams=2):
    """Extract tokens from doc.

    This uses a simple regex to break strings into tokens. For a more
    principled approach, see CountVectorizer or TfidfVectorizer.
    """
    doc = doc.replace('\n', ' ')
    words_list = [w.lower().strip() for w in doc.split(' ')]
    words_list = list(filter(lambda w: len(w) > 0, words_list))
    ngrams_list = []
 
    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + ngrams])
        ngrams_list.append(ngram)
 
    return ngrams_list


def tokens_ngram_upto(doc, ngrams=2):
    all_ngrams_list = []
    for ngram in range(1, ngrams+1):
        ngrams_list = tokens_ngram(doc, ngram)
        all_ngrams_list += ngrams_list
    return all_ngrams_list


def token_freqs(doc):
    """Extract a dict mapping tokens from each document doc to their frequencies."""
    NGRAMS = 3
    freq = defaultdict(int)
    toks = tokens_ngram_upto(doc, ngrams=NGRAMS)
    for tok in toks:
        freq[tok] += 1
    return freq




print("DictVectorizer on frequency dicts")
vec_dict = DictVectorizer()
t1 = time.time()
X_train = vec_dict.fit_transform(token_freqs(d) for d in X_train_text)

X_test = vec_dict.transform(token_freqs(d) for d in X_test_text)
print(f"DictVectorizer has shape {X_train.shape} with {X_train.data.nbytes:,} bytes and {X_train.nnz:,} non-zero items in {time.time()-t1:0.2f} seconds")
print(f"Vocabulary has {len(vec_dict.vocabulary_):,} tokens")

est = LogisticRegression(multi_class='auto', solver='liblinear')
t1 = time.time()
est.fit(X_train, y_train)
print(f"LogisticRegression score {est.score(X_test, y_test):0.2f} in {time.time()-t1:0.2f} seconds")



print("FeatureHasher on frequency dicts")
hasher = FeatureHasher()
t1 = time.time()

X_train = hasher.fit_transform(token_freqs(d) for d in X_train_text)
X_test = hasher.transform(token_freqs(d) for d in X_test_text)
print(f"FeatureHasher has shape {X_train.shape} with {X_train.data.nbytes:,} bytes and {X_train.nnz:,} non-zero items in {time.time()-t1:0.2f} seconds")

est = LogisticRegression(multi_class='auto', solver='liblinear')
t1 = time.time()
est.fit(X_train, y_train)
print(f"LogisticRegression score {est.score(X_test, y_test):0.2f} in {time.time()-t1:0.2f} seconds")


