from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import numpy as np
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

print(model.similarity("plant","gun"))
'''
mst=model.most_similar('soil',topn=10)
for i in mst:
    print(i[0],i[1])
'''
'''
for i in range(1,3):
    pickle_in = open("x_testeng_4000_fil_mix."+str(i)+".pickle","rb")
    train_data = pickle.load(pickle_in)
    train_data = np.float32(train_data)

    pickle_in = open("y_testeng_4000_fil_mix."+str(i)+".pickle","rb")
    train_labels = pickle.load(pickle_in)
    train_labels = np.asarray(train_labels)     
    
    if(i==1):
        l = train_labels
        d = train_data
    else:
        d = np.concatenate((d,train_data))
        l = np.append([l],[train_labels])
    print(i)

print(len(d),len(l))
'''