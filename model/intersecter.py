# -*- coding: utf-8 -*-
from collections import Counter
import os
MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset5/'
TESTSET_PATH = f'{MODEL_PATH}testset5/'
CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาษา","สถานที่","สัตว์","อาหาร","ภาพยนตร์"]
intsect=[]

def intersecter():
    for category in CATEGORIES:
        path = os.path.join(DATASET_PATH,category)
        cp_file = open(path+"/cp.text",mode="r")
        words=[]
        for i in cp_file:
            if(int(i.split()[1]) >=100):
                words.append((i.split()[0])) 

        if(category == "การเมือง"):
            intsect = words
        else:
            intsect = list(set(intsect).intersection(words))
        
        cp_file.close()

    #for DATASET
    intersected = open(DATASET_PATH+"intersected.txt",mode="w+")

    for w in intsect:
        intersected.write(w+"\n")
    intsect.clear()
    intersected.close()
        
intersecter()