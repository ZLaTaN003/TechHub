from django.urls import path
from . import views

urlpatterns = [
    path("news/latest-news/",name="allnews",view=views.latest_news),
    path("news/register/",name="register",view=views.signup),
    path("news/login/",name="login",view=views.login_view),
    path("news/logout/",name="logout",view=views.logout_view),
    path("news/trending",name="trending",view=views.TrendingProducts.as_view()),


    path("news/like/<slug:title_slug>/",name="like",view=views.like),
    path("news/<slug:title_slug>/",name="detailed",view=views.detailed_page),
    path("trending/<str:name>/",name="trending",view=views.trending_detail),


]