# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import docx2txt
import docx
import codecs
import os
import io
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
from collections import Counter
import random
import numpy as np
import pickle
import string
from intersecter_english import intersecter
from words_filter import words_filter

MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset_eng9/'
TESTSET_PATH = f'{MODEL_PATH}testset_eng9/'
CATEGORIES = ["business","entertainment","food","health","music","plant","politics","sport","tech"]
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

import numpy as np
import tensorflow as tf

from model64_english import cnn_model_fn

tf.logging.set_verbosity(tf.logging.INFO)


def predict(input_string):
    fullText=input_string
    text = input_string
    #for line in text:
    #    fullText = str(fullText)+ str(line.decode("utf-8"))
    print("Fulltext",fullText)
    #clean_text=re.sub("[A-Za-z0123456789!\#\$%\&'\*\+\-\.\^_`\|\~:\(\)\,\\\ ]+",'',fullText)
    clean_text=re.sub("[^A-z ]+",'',fullText)
    result=word_tokenize(clean_text)
    result= [x.lower() for x in result]
    print("Result",result)
    
    counts = Counter(result)
    counts = words_filter(counts) #Filtering start here !!!!!!!!!!!!!!!!!!!!!!!!!!!
    print("Counts Filtered",counts)
    ##HERE Pure augment
    words=counts.most_common()
    lst=[]
    for i in words : lst.append(i[0])
    words = list(filter(lambda x: x in model.vocab, lst))
    print(len(words) ,end=" ")
    predict_data=[]
    while(len(words)<64):
        words.extend(words)
    if(len(words)>=64):
        print("success")
        most64 = words[:64]
        m64=[]
        for word in most64:
            m64.append( model[word])
        predict_data.append(m64)
        x = np.array(predict_data).reshape(-1, 300, 64, 1)

        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": x},
            num_epochs=1,
            shuffle=False,
            batch_size=10
            )
        # Create the Estimator
        tag_classifier = tf.estimator.Estimator(
            model_fn=cnn_model_fn, model_dir="saved")

        predictions = list(tag_classifier.predict(input_fn=eval_input_fn,predict_keys="probabilities"))
        for i in predictions:
            predicted=(i["probabilities"])*100
        return predicted
    else :
        print("fail")

    
text="After hours of teasing via a cryptic Twitch stream, today, Hideo Kojima revealed his next game, <b>Death Stranding</b>, will be launching on the PS4 on November 8th. The lengthy stream featured a series of handprints covering what appeared to be gameplay&nbsp;... \n After hours of teasing via a cryptic Twitch stream, today, Hideo Kojima revealed his next game, <b>Death Stranding</b>, will be launching on the PS4 on November 8th. The lengthy stream featured a series of handprints covering what appeared to be gameplay&nbsp;... \n After hours of teasing via a cryptic Twitch stream, today, Hideo Kojima revealed his next game, <b>Death Stranding</b>, will be launching on the PS4 on November 8th. The lengthy stream featured a series of handprints covering what appeared to be gameplay&nbsp;..."
predict(text)