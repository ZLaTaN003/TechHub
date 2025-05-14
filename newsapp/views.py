from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404
from .forms import SignUp, Login,ProductCommentForm
from .models import NewsUser, Product
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
import json


# Create your views here.


def latest_news(request):

    latest_articles = Article.objects.all().order_by("-post_published", "-published_at")

    try:
        paginator = Paginator(latest_articles, 5)
        current_p = paginator.page(request.GET.get("cpage", 1))
    except InvalidPage:
        current_p = paginator.get_page(1)

    ctx = {"articles": latest_articles, "page": current_p}
    return render(request, "newsapp/latestnews.html", context=ctx)


def detailed_page(request, news_slug):
    article = get_object_or_404(Article, slug=news_slug)
    user_liked = (
        "1" if article.likes.filter(username=request.user.username).exists() else "0"
    )
    ctx = {"article": article, "user_liked": user_liked}
    return render(request, "newsapp/newsdetail.html", context=ctx)


def signup(request):
    form = SignUp()
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            if password1 == password2:
                try:
                    user = NewsUser.objects.create_user(
                        username=username, password=password1
                    )

                    user.save()
                except IntegrityError:  # duplicate values
                    form.add_error("username", "The username already Exists")
                    return render(
                        request, "newsapp/register.html", context={"form": form}
                    )

                login(request, user)
                return redirect("allnews")

            else:
                print("Not same")
                form.add_error("password1", "The passwords given does not match")
                return render(request, "newsapp/register.html", context={"form": form})

    ctx = {"form": form}
    return render(request, "newsapp/register.html", context=ctx)


def login_view(request):
    if request.user.is_authenticated:
        redirect("allnews")
    login_form = Login()

    if request.method == "POST":
        form = Login(request.POST)
        print("yo yo yo")
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            print("i am", user)
            if user is not None:
                login(request, user)

                return redirect("allnews")
            else:
                form.add_error("username", "The User does not exist")
                ctx = {"login_form": form}
                return render(request, "newsapp/login.html", context=ctx)

        else:
            ctx = {"login_form": form}
            return render(request, "newsapp/login.html", context=ctx)

    ctx = {"login_form": login_form}
    return render(request, "newsapp/login.html", context=ctx)


def like_news(request, news_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = json.loads(request.body)
        article = get_object_or_404(Article, slug=news_slug)
        status = data["status"]

        exist = article.likes.filter(username=request.user.username).exists()

        if status == "1":
            if not exist:
                print("Liking it")
                article.likes.add(request.user)
                return JsonResponse({"liked": True, "likecount": article.no_of_likes()})

        else:
            if exist:
                print("Unliking")
                article.likes.remove(request.user)
                return JsonResponse(
                    {"liked": False, "likecount": article.no_of_likes()}
                )
    else:
        return JsonResponse({"error": "Invalid Method"})


def logout_view(request):
    logout(request)
    return redirect("allnews")


class TrendingProducts(ListView):
    model = Product
    paginate_by = 5
    template_name = "newsapp/trendingproducts.html"
    context_object_name = "object"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.order_by("-featuredat")
        return queryset


def trending_detail(request, product_name):
    product = get_object_or_404(Product, slug=product_name)
    user_liked = (
        "1" if product.likes.filter(username=request.user.username).exists() else "0"
    )
    form = ProductCommentForm()
    ctx = {"product": product, "user_liked": user_liked,"comment_form":form}
    return render(request, "newsapp/trendingdetails.html", context=ctx)


def home(request):
    return render(request, "newsapp/home.html")


def like_product(request, product_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = json.loads(request.body)
        article = get_object_or_404(Product, slug=product_slug)
        status = data["status"]

        exist = article.likes.filter(username=request.user.username).exists()

        if status == "1":
            if not exist:
                print("Liking it")
                article.likes.add(request.user)
                return JsonResponse({"liked": True, "likecount": article.no_of_likes()})

        else:
            if exist:
                print("Unliking")
                article.likes.remove(request.user)
                return JsonResponse(
                    {"liked": False, "likecount": article.no_of_likes()}
                )
    else:
        return JsonResponse({"error": "Invalid Method"})

def product_comment(request,product_slug):
    print("HEY")