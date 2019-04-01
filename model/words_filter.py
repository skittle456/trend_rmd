# -*- coding: utf-8 -*-
from collections import Counter
import os
MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset5/'
TESTSET_PATH = f'{MODEL_PATH}testset5/'
CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาพยนตร์","ภาษา","สถานที่","สัตว์","อาหาร","ภาพยนตร์"]
intsect=[]
def words_filter(counter):
    int_words = open(DATASET_PATH+"intersected.txt")
    for word in int_words:
        del counter[word.rstrip()]
    int_words.close()
    return counter