# -*- coding: utf-8 -*-
from collections import Counter
import os
'''
MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset_thai_8/'
TESTSET_PATH = f'{MODEL_PATH}testset_thai_8/'
#CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาษา","สถานที่","สัตว์","อาหาร","ศาสนา"]
CATEGORIES = ["กีฬา","บุคคลสำคัญ"]
'''
MODEL_PATH='model/'
DATASET_PATH = f'{MODEL_PATH}dataset_eng9/'
TESTSET_PATH = f'{MODEL_PATH}testset_eng9/'
CATEGORIES = ["business","entertainment","food","health","music","plant","politics","sport","tech"]


intsect=[]
def words_filter(counter,len_min=None):
    int_words = open(DATASET_PATH+"intersected.txt")
    for word in int_words:
        del counter[word.rstrip()]
    int_words.close()

    if(len_min!=None):
        counted = Counter()
        for i in counter:
            if(len(i)>len_min):
                a = {i:counter[i]}
                counted = counted + Counter(a)
        counter = counted
    return counter