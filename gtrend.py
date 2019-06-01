from feedparser import parse
from apis.models import GoogleTrend
from datetime import datetime
from os import makedirs, path

class GTrend:
    def __init__(self):
        pass

    def write_all(self):
        gt = GoogleTrend.objects.order_by('-published_on')
        for i in gt:
            file_name = 'trends/' + i.title + '.txt'
            makedirs(path.dirname(file_name), exist_ok=True)
            f = open(file_name, "w")
            f.write(i.content)
            f.close()
            
    def core(self, geo='TH'):
        feed = parse("https://trends.google.com/trends/trendingsearches/daily/rss?geo="+geo)
        trends = GoogleTrend.objects.order_by('-published_on')
        for entry in feed.entries:
            duplicated = False
            for trend in trends:
                if trend.title == entry.title:
                    duplicated = True
                    break
            if duplicated:
                continue
            gt = GoogleTrend(title=entry.title, content=entry.ht_news_item_snippet, query = entry.summary, url = entry.ht_news_item_url)
            gt.approx_traffic = entry.ht_approx_traffic
            gt.description = entry.description
            gt.summary = entry.summary_detail.value
            gt.title_detail = entry.title_detail.value
            gt.published_on = datetime(*entry.published_parsed[:6])
            gt.lang = geo
            gt.save()
    def writefile(self, tag_name, gtrend, count, data_type):
        file_name = str(data_type) +'/'+str(tag_name)+'/'+str(count)+'.txt'
        makedirs(path.dirname(file_name), exist_ok=True)
        # with open( file_name,+'w') as w:
        #     w.write(article.text)
        f = open(str(file_name) , "w")
        f.write(str(gtrend.title) + str(gtrend.title_detail) + str(gtrend.content) + str(gtrend.query) + str(gtrend.description) +str(gtrend.summary))
        f.close()

    def catagorize(self, gtrends, data_type='trends'):
        dates = []
        for i in gtrends:
            if str(i.published_on)[:10] not in dates and i.published_on is not None:
                dates.append(str(i.published_on)[:10])
        for i in dates:
            count = 0
            for j in gtrends:
                if str(j.published_on)[:10] == i:
                    count+=1
                    self.writefile(tag_name=i, gtrend=j, count=count, data_type=data_type)

        