import numpy as np
from pythainlp import word_tokenize
from pythainlp.word_vector import thai2vec
model = thai2vec.get_model()
labels = model.index2word
values = model.word_vector
def article2vec(article,dim=999):
    tok = word_tokenize(article) # tokenize word from article
    for word in tok:
        if word in labels: # for case that tok wasn't in dic
            # vec = [[x,y], ..]
            vec += values(word)
    return vec

