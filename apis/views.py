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
from django.db.models import Q
import os
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
        trend_data = json.loads(trend_json)
        trend_lst = []
        trend_count = 0

        for i in trend_data[0]['trends']:
            try:
                obj = Trend.objects.get(name=i['name'])
            except Exception:
                obj = Trend(name=i['name'],
                    tweet_volume=i['tweet_volume'],
                    url=i['url'],
                    query=i['query']
                    )
                obj.save()
            trend_lst.append(obj)

        for i in Trend.objects.all():
            contents = oauth_req(url='https://api.twitter.com/1.1/search/tweets.json?q='+ i.query +'&lang=th&result_type=popular&count=100')
            content_json = contents.decode('utf8')
            content_data = json.loads(content_json)
            content_count = 0
            trend_count+=1
            for j in content_data['statuses']:
                text = j['text']
                link_index = text.find('http')
                url = text[link_index:-1]
                obj = Content(text=text[:link_index-1],
                    url=url)
                obj.save()
                i.content.add(obj)
                content_count+=1
                print('success-'+str(trend_count)+': '+str(content_count))

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
    
    def writefile(self, tag_name, article, count, data_type):
        file_name = data_type +'/'+tag_name+'/'+str(count)+'.txt'
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        # with open( file_name,+'w') as w:
        #     w.write(article.text)
        f = open(file_name , "w")
        f.write(article.text)
        f.close()

    def catagorize(self, articles, data_type='dataset'):
        categories = []
        for i in articles:
            if i.tag not in categories and i.tag is not None:
                categories.append(i.tag)
        for i in categories:
            count = 0
            for j in articles:
                if j.tag == i:
                    count+=1
                    self.writefile(tag_name=i, article=j, count=count, data_type=data_type)

    def merge(self):
        count=0
        articles = Article.objects.order_by('created_on')
        for i in articles:
            if i.tag is not None:
                continue
            if 'โรค' in i.title:
                count+=1
                print('success: '+str(count))
                i.tag = 'สุขภาพ'
                i.save()
                continue
            for j in i.categories.all():
                if j.name == 'โรค' or j.name == 'โรค' or 'โรค' in j.name or 'โรค' in j.name:
                    count+=1
                    print('success: '+str(count))
                    i.tag = 'สุขภาพ'
                    i.save()
                    break

    def tag_by_category(self,i,category,tag, count):
        for j in i.categories.all():
            if i.tag is not None:
                continue
            if j.name == category or category in j.name or j.name in category:
                count+=1
                print('success: '+str(count))
                i.tag = tag
                i.save()
                break
        return count

    def tag_by_title(self,i,title,tag, count):
        if title in i.title and i.tag is not None:
            count+=1
            print('success: '+str(count))
            i.tag = tag
            i.save()
        return count

    def tag_by_text(self,i,text,tag, count):
        if text in i.text and i.tag is not None:
            count+=1
            print('success: '+str(count))
            i.tag = tag
            i.save()
        return count
    def merge_sample(self):
        count=0
        articles = Article.objects.order_by('created_on')
        for i in articles:
            if i.tag is not None:
                continue
            count = self.tag_by_title(i,title="บอล",tag='กีฬา', count=count)
            count = self.tag_by_title(i,title="ภาพยนตร์",tag='ภาพยนตร์', count=count)
            count = self.tag_by_title(i,title="สัตว์",tag='สัตว์', count=count)
            count = self.tag_by_title(i,title="รัฐ",tag='สถานที่', count=count)
            count = self.tag_by_title(i,title="กษัตริย์",tag='บุคคลสำคัญ', count=count)
            count = self.tag_by_title(i,title="สงคราม",tag='สงคราม', count=count)
            count = self.tag_by_title(i,title="มวย",tag='กีฬา', count=count)
            count = self.tag_by_title(i,title="จังหวัด",tag='สถานที่', count=count)
            count = self.tag_by_title(i,title="เหตุ",tag='เหตุการณ์สำคัญ', count=count)
            count = self.tag_by_title(i,title="พรรค",tag='การเมือง', count=count)
            count = self.tag_by_title(i,title="หญ้า",tag='พืช', count=count)
            count = self.tag_by_title(i,title="มหาวิทยาลัย",tag='การศึกษา', count=count)
            count = self.tag_by_title(i,title="ศาสนา",tag='ศาสนา', count=count)
            count = self.tag_by_title(i,title="โรงเรียน",tag='การศึกษา', count=count)
            count = self.tag_by_title(i,title="มหาลัย",tag='การศึกษา', count=count)
            count = self.tag_by_title(i,title="คอนเสิร์ต",tag='ดนตรี', count=count)

            count = self.tag_by_category(i,category='บอล',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='เกมส์',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='โรค',tag='สุขภาพ', count=count)
            count = self.tag_by_category(i,category='ภูมิคุ้มกัน',tag='สุขภาพ', count=count)
            count = self.tag_by_category(i,category='นักแสดง',tag='ภาพยนตร์', count=count)
            count = self.tag_by_category(i,category='ภาพยนตร์',tag='ภาพยนตร์', count=count)
            count = self.tag_by_category(i,category='สัตว์',tag='สัตว์', count=count)
            count = self.tag_by_category(i,category='สงคราม',tag='สงคราม', count=count)
            count = self.tag_by_category(i,category='เพลง',tag='ดนตรี', count=count)
            count = self.tag_by_category(i,category='อัลบั้ม',tag='ดนตรี', count=count)
            count = self.tag_by_category(i,category='ศิลปิน',tag='ดนตรี', count=count)
            count = self.tag_by_category(i,category='มวย',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='กีฬา',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='กอล์ฟ',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='ลิมปิก',tag='กีฬา', count=count)
            count = self.tag_by_category(i,category='จังหวัด',tag='สถานที่', count=count)
            count = self.tag_by_category(i,category='กองทัพ',tag='สงคราม', count=count)
            count = self.tag_by_category(i,category='ประเทศ',tag='สถานที่', count=count)
            count = self.tag_by_category(i,category='เกม',tag='เกม', count=count)
            count = self.tag_by_category(i,category='บุคคล',tag='บุคคลสำคัญ', count=count)
            count = self.tag_by_category(i,category='ชาว',tag='บุคคลสำคัญ', count=count)
            count = self.tag_by_category(i,category='เลือกตั้ง',tag='การเมือง', count=count)
            count = self.tag_by_category(i,category='พรรค',tag='การเมือง', count=count)
            count = self.tag_by_category(i,category='เหตุ',tag='เหตุการณ์สำคัญ', count=count)
            count = self.tag_by_category(i,category='พืช',tag='พืช', count=count)
            count = self.tag_by_category(i,category='ผลไม้',tag='พืช', count=count)
            count = self.tag_by_category(i,category='ผัก',tag='พืช', count=count)
            count = self.tag_by_category(i,category='ศาสนา',tag='ศาสนา', count=count)
            count = self.tag_by_category(i,category='อาหาร',tag='อาหาร', count=count)
            count = self.tag_by_category(i,category='ซุป',tag='อาหาร', count=count)
            count = self.tag_by_category(i,category='ขนม',tag='อาหาร', count=count)
            count = self.tag_by_category(i,category='มังสวิรัติ',tag='อาหาร', count=count)
            count = self.tag_by_category(i,category='ทวีป',tag='สถานที่', count=count)
            count = self.tag_by_category(i,category='เกาะ',tag='สถานที่', count=count)
            count = self.tag_by_text(i,text="ภาษา",tag='ภาษา', count=count)
            count = self.tag_by_text(i,text="คำศัพท์",tag='ภาษา', count=count)
            count = self.tag_by_text(i,text="แร่",tag='วิทยาศาสตร์', count=count)

            count = self.tag_by_text(i,text="คอมพิวเตอร์",tag='เทคโนโลยี', count=count)
            count = self.tag_by_text(i,text="ซิงเกิล",tag='ดนตรี', count=count)
            count = self.tag_by_text(i,text="เครื่องดื่ม",tag='อาหาร', count=count)
            count = self.tag_by_text(i,text="พืช",tag='พืช', count=count)
            count = self.tag_by_text(i,text="พระ",tag='ศาสนา', count=count)
            count = self.tag_by_text(i,text="โทรทัศน์",tag='รายการโทรทัศน์', count=count)
            count = self.tag_by_text(i,text="อักษร",tag='ภาษา', count=count)
            #count = self.tag_by_text(i,text="ภาษา",tag='ภาษา', count=count)
            count = self.tag_by_text(i,text="สิ่งมีชีวิต",tag='สัตว์', count=count)
            count = self.tag_by_text(i,text="แข่งขัน",tag='กีฬา', count=count)
            count = self.tag_by_text(i,text="อาหาร",tag='อาหาร', count=count)
            count = self.tag_by_text(i,text="คอนเสิร์ต",tag='ดนตรี', count=count)
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
    
    def getsample(self):
        random_articles = self.randomize(pages=500)
        base = SampleArticle.objects.all().values_list('title', flat=True)
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
            obj = SampleArticle(title=article.title,
                            url=article.url,
                            text=content,
                            )
            try:
                categories = article.categories
            except Exception:
                continue
            obj.save()
            

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
        
    def core(self, random_articles, count = 0):
        # random_articles = wikipedia.random(pages=1024)
        base = Article.objects.all().values_list('title', flat=True)
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
        return count
        

# trend = TrendList()
# trend.core()
# a = Article.objects.filter(~Q(tag=None))
# b = GetArticle()
# b.catagorize(a)

def command(data_type='newsample'):
    a = GetArticle()
    title = a.randomize(pages=1)
    try:
        article = wikipedia.page(title[0])
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            article = wikipedia.page(e.options[0])
        except Exception:
            return
    except Exception as e:
        return
    content = a.tokenize(article.content)
    obj = Article(title=article.title,
                    url=article.url,
                    text=content,
                    )
    obj.save()
    a.catagorize(obj, data_type=data_type)
    print('success')

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