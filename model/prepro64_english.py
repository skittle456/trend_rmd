# -*- coding: utf-8 -*-
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
#CATEGORIES = ["กีฬา","ศาสนา"]
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
MODE = "TEST"

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

        num_word = 100 #
        n_word = num_word #######################
        c_word = 100
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
                clean_text=re.sub("[^A-z ]+",'',fullText)
                result=word_tokenize(clean_text)
                result= [x.lower() for x in result]
                print(path+"/"+filename,end=" ")
                #print(result)
                
                counts = Counter(result)
                counts = words_filter(counts) #Filtering start here !!!!!!!!!!!!!!!!!!!!!!!!!!!
                all_counts = counts + all_counts
                
                ##HERE Pure augment
                words=counts.most_common()
                lst=[]
                for i in words : lst.append(i[0])
                words = list(filter(lambda x: x in model.vocab, lst))
                print(len(words) ,end=" ")
                
                if(len(words)>=64):
                    print("success")
                    most64 = words[:64]
                    m64=[]
                    for word in most64:
                        m64.append( model[word])
                    training_data.append([m64, class_num])
                    #array = np.append(np.ndarray(shape=(0,0)) ,new_array)
                    
                    newpath = f'{path}_english_prepro/' # Need to set up !!!!!!!!!!!!!!!!!
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    new_file = open(newpath+str(num_word - c_word +1)+".txt",mode="w+")
                    for i in most64:
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
            
            if(n_word==0 or fail_count==None):
                break
           
        checkpoint.write(str(len(all_counts.most_common()))+" "+str(len(all_counts.most_common()))+"\n")
        for i in all_counts.most_common():
            txt , count = i
            checkpoint.write(txt+" "+str(count)+"\n")
        
        #Augmentation start here !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        while(c_word>0 ):
            
            sentence=[]
            words = all_counts.most_common()
            #rand = random.sample(words,k=64)
            while True:
                rand = WeightedSelectionWithoutReplacement(len(all_counts.most_common()),words,n=100)
                lst=[]
                for i in rand : lst.append(i[1])
                lst = list(filter(lambda x: x in model.vocab, lst))
                if(len(lst)>=64):
                    break
            most64=[]
            for i in lst:
                most64.append(model[i])
                if(len(most64)==64): break
            training_data.append([most64, class_num])

            #pure augment
            
            #new_file = open(newpath+str(num_word - c_word +1)+".txt",mode="w+")
            #for i in sentence:
            #    new_file.write(str(i)+"\n")
            
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

        X = np.array(X).reshape(-1, 300, 64, 1)

        pickle_out = open("x_test9eng_fil_mix."+str(cate)+".pickle","wb") #pickle x
        pickle.dump(X, pickle_out)
        pickle_out.close()

        pickle_out = open("y_test9eng_fil_mix."+str(cate)+".pickle","wb") #pickle y
        pickle.dump(y, pickle_out)
        pickle_out.close()

    print(count_fail)

def WeightedSelectionWithoutReplacement(len_allcounts,l, n):
    """Selects without replacement n random elements from a list of (weight, item) tuples."""
    l = sorted((random.random() * (x[1]/len_allcounts), x[0]) for x in l)
    return l[-n:] 

create_training_data()
