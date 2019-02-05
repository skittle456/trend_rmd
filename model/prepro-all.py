# -*- coding: utf-8 -*-
import docx2txt
import docx
import codecs
import os
import io
import re
import v2c
from pythainlp.tokenize import word_tokenize
from pythainlp.summarize import summarize_text
from collections import Counter
import random
import numpy as np
import pickle
import string

MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset2/'
CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาพยนตร์","ภาษา","ศาสนา","สัตว์","อาหาร","สถานที่"]
#CATEGORIES = ["พืช"]
training_data = []

def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATASET_PATH,category)
        class_num = CATEGORIES.index(category)
    #directory_in_str = "D:/thesis/trend_rmd/model"
    #directory_in_str = "F:/Workspace/Thesis/trend_rmd/model"
    #directory = os.fsencode(DATASET_PATH)
        checkpoint = open(path+"/cp.text",mode="w+")
        all_counts = Counter()
        for file in os.listdir(path):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                #text = docx2txt.process(directory_in_str+ filename)
                #doc = docx.Document( filename)
                #fullText = ""
                #for para in doc.paragraphs:
                #    fullText=fullText+para.text
                #file = open(filename+".txt","w")
                
                #with io.open(DATASET_PATH + filename+".txt",'w',encoding='utf8') as f:
                #    f.write(fullText)
                #text=re.sub('[^A-Za-z0-9\u0E00-\u0E7F.\-]+','',fullText)
                #result=word_tokenize(text,engine='newmm')
                fullText=""
                text = open(path+"/"+filename,mode="rb")
                for line in text:
                    fullText = str(fullText)+ str(line.decode("utf-8"))
                #print(fullText)
                #clean_text=re.sub("[A-Za-z0123456789!\#\$%\&'\*\+\-\.\^_`\|\~:\(\)\,\\\ ]+",'',fullText)
                clean_text=re.sub("[^ก-๙]+",'',fullText)
                result=word_tokenize(clean_text,engine='newmm')
                print(path+"/"+filename)
                #print(result)
                
                counts = Counter(result)
                all_counts = counts + all_counts
                '''
                if(len(counts)>=64):
                    most32 = counts.most_common(32)
                    m32=[]
                    for i in most32 : m32.append(i[0])
                    #32 words most
                    for i in m32: del(counts[i])
                    print(len(m32))
                    print(m32)
                    lowest16 = list(counts.most_common()[:-17:-1])
                    lw16 = []
                    for i in lowest16: lw16.append(i[0])
                    #16 words lowerest
                    for i in lw16: del(counts[i]) 
                    print(len(lw16))
                    print(lw16)
                    random16 = random.choices(list(counts),k=16) 
                    #16 random words
                    rd16 =[]
                    for i in random16: rd16.append(i)
                    print(len(rd16))
                    print(rd16)
                    sentence=[]
                    sentence.extend(m32)
                    sentence.extend(lw16)
                    sentence.extend(rd16)
                    new_array = v2c.t2v(sentence)
                    training_data.append([new_array, class_num])

                    print(training_data)
                '''
                text.close()
        checkpoint.write(str(len(all_counts.most_common()))+"\n")
        for i in all_counts.most_common():
            txt , count = i
            checkpoint.write(txt+" "+str(count)+"\n")
        checkpoint.close()
        all_counts.clear()
        #here

create_training_data()
'''
X=[]
y=[]
for features,label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, 64, 400, 1)

pickle_out = open("X_article.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y_article.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()
'''


