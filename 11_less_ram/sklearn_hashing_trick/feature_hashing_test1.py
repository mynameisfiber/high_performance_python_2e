# explore some timings and characteristics of the feature hashing, dict vectoriser and count vectoriser
# note that these are not used in the book

# how much storage required by each?
# what sort of loss by each stage of having a smaller n_features?
# exact same config of words for all?
# what is nbytes for each?

import re
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

NGRAM_MAX = 3
FIT = True
print(f"{NGRAM_MAX} NGRAM_MAX")

categories = [
    'alt.atheism',
    'comp.graphics',
]

categories2 = [
    'alt.atheism',
    'comp.graphics',
    'comp.sys.ibm.pc.hardware',
    'misc.forsale',
    'rec.autos',
    'sci.space',
    'talk.religion.misc',
]

# Uncomment the following line to use a larger set (11k+ documents)
#categories = None

print("Loading 20 newsgroups training data")
#raw_data = fetch_20newsgroups(subset='train', categories=categories).data
#data_size_mb = sum(len(s.encode('utf-8')) for s in raw_data) / 1e6
#print("%d documents - %0.3fMB" % (len(raw_data), data_size_mb))
#print()
news = fetch_20newsgroups(subset='train', categories=categories)
# news.data is raw text, news.target is target labels

print(pd.Series(news.target).value_counts())

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
    #return (tok.lower() for tok in re.findall(r"\w+", doc))



def tokens_ngram_upto(doc, ngrams=2):
    all_ngrams_list = []
    for ngram in range(1, ngrams+1):
        ngrams_list = tokens_ngram(doc, ngram)
        all_ngrams_list += ngrams_list
    return all_ngrams_list
print(tokens_ngram_upto(X_train_text[0], 2))









if False:
    print("\nCountVectorizer")
    vec = CountVectorizer(ngram_range=(1, NGRAM_MAX))
    t1 = time.time()
    X_train = vec.fit_transform(X_train_text)
    X_test = vec.transform(X_test_text)
    print(f"CountVectorizer shape {X_train.shape} with {X_train.data.nbytes:,} bytes and nnz {X_train.nnz:,} in {time.time()-t1}")
    #(Pdb) p X_train.todense()
    #matrix([[0, 0, 0, ..., 0, 0, 0],
    #        [2, 0, 0, ..., 0, 0, 0],
    #        [0, 0, 0, ..., 0, 0, 0],

    print(f"Vocab length {len(vec.vocabulary_)}")

    if True and FIT:
        est = LogisticRegression(multi_class='auto', solver='liblinear')
        t1 = time.time()
        est.fit(X_train, y_train)

        print(f"Score CountVectorizer {est.score(X_test, y_test)} in {time.time()-t1}")


def tokens(doc):
    """Extract tokens from doc.

    This uses a simple regex to break strings into tokens. For a more
    principled approach, see CountVectorizer or TfidfVectorizer.
    """
    return (tok.lower() for tok in re.findall(r"\w+", doc))


def token_freqs(doc):
    """Extract a dict mapping tokens from doc to their frequencies."""
    freq = defaultdict(int)
    #toks = tokens(doc)
    toks = tokens_ngram_upto(doc, NGRAM_MAX)
    for tok in toks:
        freq[tok] += 1
    return freq


print("\nDictVectoriser")
print("DictVectorizer on frequency dicts")
vec_dict = DictVectorizer()
#vec_dict.fit_transform(token_freqs(d) for d in X_train_text)
#hasher = FeatureHasher(n_features=n_features)
t1 = time.time()
X_train = vec_dict.fit_transform(token_freqs(d) for d in X_train_text)
X_test = vec_dict.transform(token_freqs(d) for d in X_test_text)
print(f"DictVectorizer shape {X_train.shape} with {X_train.data.nbytes:,} bytes and nnz {X_train.nnz:,} in {time.time()-t1}")
print(f"Vocab length {len(vec_dict.vocabulary_)}")
#(Pdb) p X_train.todense()
#matrix([[1., 0., 0., ..., 0., 0., 0.],
#        [0., 2., 0., ..., 0., 0., 0.],
#        [0., 0., 0., ..., 0., 0., 0.],

if True and FIT:
    est = LogisticRegression(multi_class='auto', solver='liblinear')
    t1 = time.time()
    est.fit(X_train, y_train)

    print(f"Score {est.score(X_test, y_test)} in {time.time()-t1}")

print("\nFeatureHasher")
print("FeatureHasher on frequency dicts")
n_features=1048576
#n_features=int(1048576 / 2)
hasher = FeatureHasher(n_features=n_features)
t1 = time.time()
X_train = hasher.fit_transform(token_freqs(d) for d in X_train_text)
X_test = hasher.transform(token_freqs(d) for d in X_test_text)
print(f"FeatureHasher XX shape {X_train.shape} with {X_train.data.nbytes:,} bytes and nnz {X_train.nnz:,} in {time.time()-t1}")

if FIT:
    est = LogisticRegression(multi_class='auto', solver='liblinear')
    t1 = time.time()
    est.fit(X_train, y_train)
    print(f"Score {est.score(X_test, y_test)} in {time.time()-t1}")


#NGRAM_MAX 1

#CountVectorizer
#CountVectorizer shape (8485, 112359) with 10,723,592 bytes and nnz 1,340,449
#Vocab length 112359
#Score CountVectorizer 0.8882997525627431

#DictVectoriser
#DictVectorizer on frequency dicts
#DictVectorizer shape (8485, 213378) with 11,570,296 bytes and nnz 1,446,287
#Vocab length 213378
#Score 0.8709791445740545

#FeatureHasher
#FeatureHasher on frequency dicts
#FeatureHasher XX shape (8485, 1048576) with 11,568,160 bytes and nnz 1,446,020
#Score 0.8709791445740545


#In [24]: n_features=int(1048576 / 2) 
#FeatureHasher XX shape (8485, 524288) with 11,564,952 bytes and nnz 1,445,619
#Score 0.8695652173913043

# div 128 to 8192 cols saves no RAM, scores starts to decrease
#In [28]: n_features=int(1048576 / 128) 
#FeatureHasher XX shape (8485, 8192) with 11,325,136 bytes and nnz 1,415,642
#Score 0.8373983739837398

# div 1024 saves RAM but gets obviously worse
#In [31]: n_features=int(1048576 / 1024) 
#FeatureHasher XX shape (8485, 1024) with 9,972,088 bytes and nnz 1,246,511
#Score 0.6493460586779781 # also failed to converge

#NGRAM_MAX 2

#CountVectorizer
#CountVectorizer shape (8485, 976933) with 28,135,904 bytes and nnz 3,516,988
#Vocab length 976933

#DictVectoriser
#DictVectorizer on frequency dicts
#DictVectorizer shape (8485, 1209358) with 29,098,656 bytes and nnz 3,637,332
#Vocab length 1209358

#FeatureHasher
#FeatureHasher on frequency dicts
#FeatureHasher XX shape (8485, 1048576) with 29,081,744 bytes and nnz 3,635,218



#NGRAM_MAX 3

#CountVectorizer
#CountVectorizer shape (8485, 2,562,221) with 46,976,712 bytes and nnz 5,872,089
#Vocab length 2562221
#Score CountVectorizer 0.8992576882290562

#DictVectoriser
#DictVectorizer on frequency dicts
#DictVectorizer shape (8485, 2874808) with 47,750,336 bytes and nnz 5,968,792 in 21.821120500564575
#Vocab length 2874808
#Score 0.8819370802403677 in 476.8893744945526

#FeatureHasher
#FeatureHasher on frequency dicts
#FeatureHasher XX shape (8485, 1048576) with 47,698,064 bytes and nnz 5,962,258 in 12.273415803909302
#Score 0.8829975256274302 in 346.5603098869324
# Note 1/2 time to build and 35% faster at build time

#NGRAM_MAX 4

#CountVectorizer
#CountVectorizer shape (8485, 4440538) with 66,176,936 bytes and nnz 8,272,117
#Vocab length 4440538

#DictVectoriser
#DictVectorizer on frequency dicts
#DictVectorizer shape (8485, 4819861) with 66,615,984 bytes and nnz 8,326,998
#Vocab length 4819861

#FeatureHasher
#FeatureHasher on frequency dicts
#FeatureHasher XX shape (8485, 1048576) with 66,505,560 bytes and nnz 8,313,195

# NGRAM_MAX 5

#CountVectorizer
#CountVectorizer shape (8485, 6412596) with 85,489,304 bytes and nnz 10,686,163
#Vocab length 6412596

#DictVectoriser
#DictVectorizer on frequency dicts
#DictVectorizer shape (8485, 6860942) with 85,513,760 bytes and nnz 10,689,220
#Vocab length 6860942

#FeatureHasher
#FeatureHasher on frequency dicts
#FeatureHasher XX shape (8485, 1048576) with 85,323,080 bytes and nnz 10,665,385

# feature hasher is _faster_ than DictVectorizer for same RAM usage - other benefits?
# maybe time to fit is faster due to smaller feature space?
