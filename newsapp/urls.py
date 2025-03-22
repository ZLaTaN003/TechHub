from django.urls import path
from . import views

urlpatterns = [
    path("news/latest-news",name="allnews",view=views.latest_news),
]