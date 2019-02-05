'''
#coding: UTF-8
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import numpy as np
from pythainlp import word_tokenize
from pythainlp.word_vector import thai2vec
model = thai2vec.get_model()

def article2vec(article,dim=999):
    tok = word_tokenize(article) # tokenize word from article
    for word in tok:
        if word in labels: # for case that tok wasn't in dic
            # vec = [[x,y], ..]
            vec += values(word)
    return vec
'''
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from pythainlp.tokenize import word_tokenize
from gensim.models import KeyedVectors
import numpy as np

from pythainlp.corpus import ttc
from pythainlp.spell import spell

DATA_PATH='../model/'
MODEL_PATH = f'{DATA_PATH}word2vec/'

def t2v(words):
        #load into gensim
        model = KeyedVectors.load_word2vec_format(f'{MODEL_PATH}thai2vec.bin',binary=True)
        #create dataframe
        arr = np.empty((0,400), int)
        for word in words:
                if word not in model.wv.index2word:
                        word = "รายงาน"
                arr = np.append( arr, [model.wv.word_vec(word)],axis=0 )  
        return arr