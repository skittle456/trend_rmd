# -*- coding: utf-8 -*-
from pythainlp.tokenize import word_tokenize
f = open("simple-data.txt")

a = "ความท้าทายของโอกาสธุรกิจส Organic Tourism อยู่ที่ความไม่ชัดเจนว่าใครจะมาเป็นลูกค้า"
print(a)
b = word_tokenize(a)
print(b) 