from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

class TrendingList(APIView):
    def get(request):
        if request.user.is_authenticated:
            redirect('https://api.twitter.com/1.1/trends/place.json?id=1')
        