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

    def core(self):
        feed = parse("https://trends.google.com/trends/trendingsearches/daily/rss?geo=TH")
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
            gt.published_on = datetime(*entry.published_parsed[:6])
            gt.save()

        