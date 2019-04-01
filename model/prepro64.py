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
CATEGORIES = ["การเมือง","การศึกษา","กีฬา","ดนตรี","พืช","ภาษา","สถานที่","สัตว์","อาหาร","ศาสนา"]
#CATEGORIES = ["กีฬา","ศาสนา"]

MODE = "DATA"

def create_training_data():
    
    count_fail = [0]*10
    cate=0
    intersecter()
    for category in CATEGORIES:
        training_data = []
        if(MODE == "DATA"):
            ##for DATASET
            path = os.path.join(DATASET_PATH,category)
        else:
            ##for TESTSET
            path = os.path.join(TESTSET_PATH,category)
        class_num = CATEGORIES.index(category)
        #directory_in_str = "D:/thesis/trend_rmd/model"
        #directory_in_str = "F:/Workspace/Thesis/trend_rmd/model"
        #directory = os.fsencode(DATASET_PATH)
        checkpoint = open(path+"/cp_filtered.text",mode="w+")
        all_counts = Counter()
        files = os.listdir(path)
        if(MODE =="DATA"):
            try:
                #files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))
                files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))
            except:
                files.remove("cp.text")
                files.remove("cp_filtered.text")
                files.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))

        num_word = 100
        n_word = num_word #######################
        c_word = n_word
        fail_count=0
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
                
                counts = Counter(result)
                counts = words_filter(counts) #filtered
                
                all_counts = counts + all_counts
                print(len(counts) ,end=" ")
                if(len(counts)>=64):
                    print("success")
                    most32 = counts.most_common(64)
                    m32=[]
                    for i in most32 : m32.append(i[0])
                    #32 words most
                    for i in m32: del(counts[i])
                    #print(len(m32))
                    #print(m32)
                    #lowest16 = list(counts.most_common()[:-17:-1])
                    #lw16 = []
                    #for i in lowest16: lw16.append(i[0])
                    ##16 words lowerest
                    #for i in lw16: del(counts[i]) 
                    ##print(len(lw16))
                    ##print(lw16)
                    #random16 = random.choices(list(counts),k=16) 
                    #16 random words
                    #rd16 =[]
                    #for i in random16: rd16.append(i)
                    #print(len(rd16))
                    #print(rd16)
                    sentence=[]
                    sentence.extend(m32)
                    #sentence.extend(lw16)
                    #sentence.extend(rd16)
                    new_array = v2c.t2v(sentence)
                    #array = np.append(np.ndarray(shape=(0,0)) ,new_array)
                    training_data.append([new_array, class_num])
                    newpath = f'{path}_preprocessed_unfil/' 
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    new_file = open(newpath+str(num_word - c_word +1)+".txt",mode="w+")
                    for i in sentence:
                        new_file.write(str(i)+"\n")
                    #print(training_data)
                    c_word = c_word-1
                    fail_count=0
                else :
                    count_fail[cate] = count_fail[cate]+1
                    fail_count=fail_count+1
                    print("fail")
                text.close()
            n_word = n_word-1
            
            if(n_word==0 or fail_count==10):
                break
            
        checkpoint.write(str(len(all_counts.most_common()))+" "+str(len(all_counts.most_common()))+"\n")
        for i in all_counts.most_common():
            txt , count = i
            checkpoint.write(txt+" "+str(count)+"\n")
        
        while(c_word>0):
            sentence=[]
            words = all_counts.most_common()
            #rand = random.sample(words,k=64)
            rand = WeightedSelectionWithoutReplacement(len(all_counts.most_common()),words,n=64)
            for i in rand:
                count , txt = i
                sentence.append(txt)
            new_array = v2c.t2v(sentence)
            #array = np.append(np.ndarray(shape=(0,0)) ,new_array)
            training_data.append([new_array, class_num])
            new_file = open(newpath+str(num_word - c_word +1)+".txt",mode="w+")
            for i in sentence:
                new_file.write(str(i)+"\n")
            c_word=c_word-1
            print(category,c_word)
        
        checkpoint.close()
        all_counts.clear()
        #here
        cate = cate + 1

        X=[]
        y=[]
        for features,label in training_data:
            X.append(features)
            y.append(label)

        X = np.array(X).reshape(-1, 400, 64, 1)

        pickle_out = open("x_data5_100."+str(cate)+".pickle","wb")
        pickle.dump(X, pickle_out)
        pickle_out.close()

        pickle_out = open("y_data5_100."+str(cate)+".pickle","wb")
        pickle.dump(y, pickle_out)
        pickle_out.close()

    print(count_fail)

def WeightedSelectionWithoutReplacement(len_allcounts,l, n):
    """Selects without replacement n random elements from a list of (weight, item) tuples."""
    l = sorted((random.random() * (x[1]/len_allcounts), x[0]) for x in l)
    return l[-n:] 

create_training_data()





