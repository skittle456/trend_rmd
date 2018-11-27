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
directory_in_str = "D:/thesis/trend_rmd/model"
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
            print(result)
            counts = Counter(result)
            print(counts)
            print(len(counts))



