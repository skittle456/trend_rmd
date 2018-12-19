# -*- coding: utf-8 -*-
import docx2txt
import docx
import codecs
import os
import io
import re
from pythainlp.tokenize import word_tokenize
from pythainlp.summarize import summarize_text
from collections import Counter
import random


#directory_in_str = "D:/thesis/trend_rmd/model"
directory_in_str = "F:/Workspace/Thesis/trend_rmd/model"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".docx"):
        #text = docx2txt.process(directory_in_str+ filename)
        doc = docx.Document( filename)
        fullText = ""
        for para in doc.paragraphs:
            fullText=fullText+para.text
        #file = open(filename+".txt","w")
        
        with io.open(directory_in_str + filename+".txt",'w',encoding='utf8') as f:
            f.write(fullText)
        text=re.sub('[^A-Za-z0-9\u0E00-\u0E7F.\-]+','',fullText)
        result=word_tokenize(text,engine='newmm')
        if("1.docx"==filename):
            #print(result)
            counts = Counter(result)
            most32 = counts.most_common(32)
            m32=[]
            for i in most32 : m32.append(i[0])
            print("Most :",m32) #32 words most
            for i in m32: del(counts[i])
            print()

            lowest16 = list(counts.most_common()[:-17:-1])
            lw16 = []
            for i in lowest16: lw16.append(i[0])
            print("lowest :",lw16) #16 words lowerest
            for i in lw16: del(counts[i]) 

            print() 
            random16 = random.choices(list(counts),k=16) #16 random words
            rd16 =[]
            for i in random16: rd16.append(i)
            print("Random :",rd16)



