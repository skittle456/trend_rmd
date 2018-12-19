from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.decorators import login_required
import twitter
import oauth2
import json
import wikipedia
import re
from apis.models import *
# Create your views here.

#twitter
# api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
#                 consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
#                 access_token_key=settings.TWITTER_ACCESS_TOKEN,
#                 access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
# print(api.VerifyCredentials())
#key=settings.TWITTER_ACCESS_TOKEN, secret=settings.TWITTER_ACCESS_TOKEN_SECRET
def oauth_req(url, key='895689175223095296-lS956TCRC7FpadMili3tkb5tJbC1wJm', secret='0EiMeh2Xcqbl6NBzitD1LKAHHdYehevaSbECJ1Tr4fBWd', http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=settings.SOCIAL_AUTH_TWITTER_KEY, secret=settings.SOCIAL_AUTH_TWITTER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content
class TrendList(object):
    def __init__(self):
        pass
    def core(self):
        trends = oauth_req(url='https://api.twitter.com/1.1/trends/place.json?id=23424960')
        trend_json = trends.decode('utf8').replace("'", '"')
        print(trends)
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(trend_json)
        trend_json = json.dumps(data, indent=4, sort_keys=True)
        for i in trend_json:
            print(i)
            print(i['trends'])
        contents = oauth_req(url='https://api.twitter.com/1.1/search/tweets.json?q=SabrinaNetflix&lang=th&result_type=popular&count=10')
        print(contents)
        with open('contents','ab') as w:
            w.write(contents)
            w.write(', ')

class GetArticle(object):

    def __init__(self):
        wikipedia.set_lang('th')
        pass
    
    def tokenize(self, content):
        index = 1
        content = content.split('\n')
        for item in content:
            if '== อ้างอิง ==' == item:
                index = content.index(item)
                if index != -1:
                    content[index:] = ''
            elif '==' in item:
                content.remove(item)
        # index = 1
        # while index != -1:
        #     index = content.index('[', index+1)
        #     close_index = content.index(']', index+1)
        #     for i in range(index, close_index):
        #         content[i] = ''
        #     if index != -1:
        #         index = close_index + 1
        content = ''.join(content)
        content = re.sub("[\=\(\[].*?[\)\=\]]", "", content)
        return content
    def merge(self):
        count=0
        articles = Article.objects.order_by('created_on')
        for i in articles:
            if i.tag is not None:
                continue

            for j in i.categories.all():
                if j.name == 'ดาว' or j.name == 'ดาว' or 'ดาว' in j.name or 'ดาว' in j.name:
                    count+=1
                    print('success: '+str(count))
                    i.tag = 'วิทยาศาสตร์'
                    i.save()
                    break
    def randomize(self, pages=20000):
        articles = wikipedia.random(pages=pages)
        
        for i in articles:
            if 'จังหวัด' in i or 'อำเภอ' in i or 'เขต' in i or 'ทางหลวง' in i:
                articles.remove(i)
        return articles
    
    def search_title(self, query, results=13000):
        articles = wikipedia.search(query, results=results)
        articles = articles[::-1]
        for i in articles:
            if 'จังหวัด' in i or 'อำเภอ' in i or 'เขต' in i or 'ทางหลวง' in i:
                articles.remove(i)
        return articles

    def core(self, random_articles):
        # random_articles = wikipedia.random(pages=1024)
        base = Article.objects.all().values_list('title', flat=True)
        count = 0
        skip_count = 0
        for item in random_articles:
            if item in base:
                skip_count+=1
                continue
            try:
                article = wikipedia.page(item)
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    article = wikipedia.page(e.options[0])
                except Exception:
                    continue
            except Exception as e:
                continue

            if article.title in base:
                skip_count+=1
                continue

            content = self.tokenize(article.content)
            obj = Article(title=article.title,
                            url=article.url,
                            text=content,
                            )
            try:
                categories = article.categories
            except Exception:
                continue
            obj.save()
            
            main_category = Category.objects.get(name="อาหาร")
            obj.categories.add(main_category)

            base_categories = Category.objects.all().values_list('name', flat=True)
            for category in categories:
                category = category.replace('หมวดหมู่:', '')
                if re.search('[a-zA-Z]', category) is None and 'บทความ' not in category and 'หน้าที่' not in category and category is not None:
                    if category not in base_categories:
                        obj_cat = Category(name=category)
                        obj_cat.save()
                    else:
                        obj_cat = Category.objects.get(name=category)
                    obj.categories.add(obj_cat)
            obj.save()
            count+=1
            print('success: '+str(count))
        print('total: '+str(len(random_articles)))
        print('skip: '+str(skip_count))
        return obj
        

# trend = TrendList()
# trend.core()
a = GetArticle()
a.merge()
# articles = a.search_title(query='สัตว์')
# a.core(random_articles=articles)
# from django.db import connections

# def srd_db():
#     c = connections['srd-view'].cursor()
#     print('after cusor')
#     c.execute("select * from apps.xxcon_lease;")
#     print('after exe')
#     row = c.fetchall()
#     print('after fetch')
#     print(row)
#     return row
# srd_db()
@login_required
def home(request):
    return render(request, 'home.html')

class TrendingList(APIView):
    def get(self, request):
        return redirect("https://api.twitter.com/1.1/trends/place.json?id=1")
        
# import requests
# import html2text
# import time
# import re
# class GetArticle(object):

#     def __init__(self):
#         pass

#     def core(self):
#         translator = html2text.HTML2Text()
#         translator.ignore_links = True
#         translator.ignore_images = True
#         articles = []
#         for i in range(6):
#             random_page = requests.get('https://th.wikipedia.org/api/rest_v1/page/random/title')
#             random_page = random_page.json()
#             title = random_page['items'][0]['title']
#             page = requests.get('https://th.wikipedia.org/api/rest_v1/page/html/'+title)
#             page = page.text

#             not_categories = ['บทความ', 'หน้าที่']
#             index = 1
#             i = 1
#             categories = []
#             while index != -1:
#                 index = page.find('<link rel="mw:PageProp/Category" href="./หมวดหมู่:', index+1)
#                 if index != -1:
#                     index+=50
#                 category = ''
#                 for j in page[index:]:
#                     if j == '"':
#                         if category not in not_categories and re.search('[a-zA-Z]', category) is None:
#                             for i in not_categories:
#                                 if i in category:
#                                     break
#                             categories.append(category)
#                         category = ''
#                         break
#                     category+=j
#                 i+=1
        
#             text = translator.handle(page)
#             #articles.append(text)
#             with open('articles','a') as w:
#                 w.write("'category' :")
#                 for i in categories:
#                     w.write(i)
#                     w.write(', ')
#                 w.write(', ')
#                 w.write("'text' :")
#                 w.write(text)
#                 w.write(', ')

#             #print("title: "+title, 'category: ', *categories, sep=' ,')
#         return articles