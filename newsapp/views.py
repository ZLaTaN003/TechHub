from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from datetime import datetime,timedelta

# Create your views here.

def latest_news(request):
    latest_articles = Article.objects.filter(post_published__gte=datetime.now().date() - timedelta(days=1)).order_by("-post_published")
    ctx = {"artcls": latest_articles}

    return render(request,"newsapp/news.html",context=ctx)




