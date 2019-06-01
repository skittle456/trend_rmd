from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Category(models.Model):
    category_id = models.AutoField(max_length=10,primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" %  (self.name)

class Content(models.Model):
    content_id = models.AutoField(max_length=10,primary_key=True)
    text =  models.TextField()
    url = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    created_on = models.DateTimeField(auto_now_add=True) 

class Trend(models.Model):
    trend_id = models.AutoField(max_length=10,primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255,null=True,blank=True)
    query = models.CharField(max_length=255,null=True,blank=True)
    tweet_volume = models.IntegerField(null=True,blank=True,default=0)
    content = models.ManyToManyField(Content)
    def __str__(self):
        return "%s" %  (self.name)
    
class GoogleTrend(models.Model):
    trend_id = models.AutoField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255)
    title_detail = models.CharField(max_length=255,null=True,blank=True)
    summary = models.CharField(max_length=255,null=True,blank=True)
    lang = models.CharField(max_length=100, default='TH')
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=255,null=True,blank=True)
    query = models.CharField(max_length=255,null=True,blank=True)
    approx_traffic = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True, blank=True)
    published_on = models.DateTimeField(null=True)
     
class Article(models.Model):
    article_id = models.AutoField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255)
    text =  models.TextField()
    url = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    tag = models.CharField(max_length=255, default=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return "%s" %  (self.title)

class SampleArticle(models.Model):
    article_id = models.AutoField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255)
    text =  models.TextField()
    url = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    tag = models.CharField(max_length=255, default=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return "%s" %  (self.title)