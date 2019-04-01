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
from intersecter import intersecter
from words_filter import words_filter

MODEL_PATH='../model/'
DATASET_PATH = f'{MODEL_PATH}dataset5/'
TESTSET_PATH = f'{MODEL_PATH}testset5/'
CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาษา","สถานที่","สัตว์","อาหาร","ภาพยนตร์"]
#CATEGORIES = ["พืช"]
training_data = []

def create_training_data():
    count_fail = [0]*10
    cate=0
    intersecter()
    for category in CATEGORIES:
        ##for DATASET
        #path = os.path.join(DATASET_PATH,category)
        ##for TESTSET
        path = os.path.join(TESTSET_PATH,category)
        class_num = CATEGORIES.index(category)
    #directory_in_str = "D:/thesis/trend_rmd/model"
    #directory_in_str = "F:/Workspace/Thesis/trend_rmd/model"
    #directory = os.fsencode(DATASET_PATH)
        checkpoint = open(path+"/cp_filtered.text",mode="w+")
        all_counts = Counter()
        files = os.listdir(path)
        '''
        try:
            #files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))
            files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))
        except:
            files.remove("cp.text")
            files.remove("cp_filtered.text")
            files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))
        '''
        n_word = 30 #######################
        c_word = n_word
        for file in files:
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
                print(path+"/"+filename,end=" ")
                #print(result)
                
                count = Counter(result)
                counts = words_filter(count) #filtered

                all_counts = counts + all_counts
                print(len(counts) ,end=" ")
                if(len(counts)>=32):
                    
                    print("success")
                    most = counts.most_common(24)
                    m=[]
                    for i in most : m.append(i[0])
                    #words most
                    for i in m: del(counts[i])
                    #print(len(m))
                    #print(m)
                    #lowest = list(counts.most_common()[:-17:-1])
                    #lw = []
                    #for i in lowest: lw.append(i[0])
                    ##words lowerest
                    #for i in lw: del(counts[i]) 
                    ##print(len(lw))
                    ##print(lw)
                    randoming = random.choices(list(counts),k=8) 
                    #random words
                    rd =[]
                    for i in randoming: rd.append(i)
                    #print(len(rd16))
                    #print(rd16)
                    sentence=[]
                    sentence.extend(m)
                    #sentence.extend(lw)
                    sentence.extend(rd)
                    new_array = v2c.t2v(sentence)
                    training_data.append([new_array, class_num])

                    #print(training_data)
                    c_word = c_word-1
                else :
                    count_fail[cate] = count_fail[cate]+1
                    print("fail")
                text.close()

            n_word = n_word-1
            if(n_word==0):
                break

        

        checkpoint.write(str(len(all_counts.most_common()))+" "+str(len(all_counts.most_common()))+"\n")
        for i in all_counts.most_common():
            txt , count = i
            checkpoint.write(txt+" "+str(count)+"\n")
        
        while(c_word>0):
            sentence=[]
            words = all_counts.most_common()
            rand = random.sample(words,k=32)
            for i in rand:
                txt , count = i
                sentence.append(txt)
            new_array = v2c.t2v(sentence)
            training_data.append([new_array, class_num])
            c_word=c_word-1
            print(c_word)

        checkpoint.close()
        all_counts.clear()
        
        #here
        cate = cate + 1
    print(count_fail)
    
create_training_data()

X=[]
y=[]
for features,label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, 32, 400, 1)

pickle_out = open("x_test5_32.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y_test5_32.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()



