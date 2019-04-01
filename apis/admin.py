from django.contrib import admin
from apis.models import *
# Register your models here.

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Trend)
admin.site.register(Content)