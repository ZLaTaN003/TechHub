from django.urls import path
from . import views

urlpatterns = [
    path("",name="home",view=views.home),
    path("news/register/",name="register",view=views.signup),
    path("news/login/",name="login",view=views.login_view),
    path("news/logout/",name="logout",view=views.logout_view),
    path("trending/search/",name="product_search",view=views.search_product),
    path("trending/bookmarked/",name="bookmark",view=views.bookmarked),


    path("news/latest-news/",name="allnews",view=views.latest_news),   #news list
    path("news/trending",name="trending_list",view=views.TrendingProducts.as_view()), #product list

    path("news/like/<slug:news_slug>/",name="like_news",view=views.like_news),
    path("trending/like/<slug:product_slug>/",name="like_product",view=views.like_product),

    path("trending/comment/<slug:product_slug>/",name="product_comment",view=views.product_comment),

    path("news/comment/<slug:news_slug>/",name="news_comment",view=views.news_comment),

    path("news/<slug:news_slug>/",name="detailed",view=views.detailed_page), #news detail
    path("trending/<slug:product_name>/",name="trending_products",view=views.trending_detail), #trending detail

    path("trending/category/<slug:category_slug>/",name="category",view=views.CategoryProduct.as_view()),





]