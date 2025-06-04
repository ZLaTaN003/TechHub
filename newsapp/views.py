from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404
from .forms import (
    SignUp,
    Login,
    ProductCommentForm,
    ArticleCommentForm,
    ArticleComment,
    ProductComment,
)
from .models import NewsUser, Product
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count, Max
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
import json
from django.utils import timezone
from datetime import timedelta


def home(request):
    past_week_date = timezone.now() - timedelta(days=7)
    past_month_date = timezone.now() - timedelta(days=30)
    hyped_articles = (
        Article.objects.filter(post_published__gte=past_week_date)
        .annotate(num_likes=Count("likes"))
        .order_by("-num_likes").order_by("-post_published", "-published_at")[:10]
    )
    latest_news_articles = Article.objects.all().order_by(
        "-post_published", "-published_at"
    )[:10]
    hyped_products = Product.objects.filter(featuredat__gt=past_month_date).order_by(
        "-upvotes"
    )[:10]

    categories_product = Product.objects.values_list(
        "domain", flat=True
    ).distinct()  # category to base

    return render(
        request,
        "newsapp/home.html",
        context={
            "hyped_articles": hyped_articles,
            "latest_news": latest_news_articles,
            "hyped_products": hyped_products,
            "categories": categories_product,
        },
    )


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
    form = ArticleCommentForm()
    article_comments = ArticleComment.objects.filter(article=article).order_by(
        "-created_at"
    )
    user_liked = (
        "1" if article.likes.filter(username=request.user.username).exists() else "0"
    )
    no_of_likes = article.no_of_likes()

    ctx = {
        "article": article,
        "user_liked": user_liked,
        "comment_form": form,
        "comments": article_comments,
        "no_of_likes": no_of_likes,
    }
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


def logout_view(request):
    logout(request)
    return redirect("allnews")


class CategoryProduct(ListView):
    paginate_by = 5
    template_name = "newsapp/trendingproducts.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.objects.values_list(
            "domain", flat=True
        ).distinct()  # category to base
        context["type"] = "category"
        context["category"] = self.category
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        queryset = Product.objects.filter(domain_slug=category_slug)
        self.category = queryset[0].domain
        return queryset


class TrendingProducts(ListView):
    model = Product
    paginate_by = 5
    template_name = "newsapp/trendingproducts.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.objects.values_list(
            "domain", flat=True
        ).distinct()  # category to base
        context["type"] = "productlist"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-featuredat")
        return queryset


def search_product(request):
    query = request.GET.get("searchTerm")
    products = Product.objects.filter(name__contains=query).order_by("featuredat")
    categories = Product.objects.values_list(
        "domain", flat=True
    ).distinct()  # category to base
    paginator = Paginator(products, 5)

    try:
        current_p = paginator.page(request.GET.get("page", 1))
    except InvalidPage:
        current_p = paginator.get_page(1)
    return render(
        request,
        "newsapp/trendingproducts.html",
        context={
            "page_obj": current_p,
            "categories": categories,
            "type": "search",
            "query": query,
            "object": current_p,
        },
    )


def trending_detail(request, product_name):
    product = get_object_or_404(Product, slug=product_name)
    user_liked = (
        "1" if product.likes.filter(username=request.user.username).exists() else "0"
    )
    form = ProductCommentForm()
    product_comments = ProductComment.objects.filter(product=product).order_by(
        "-created_at"
    )
    no_of_likes = product.no_of_likes()

    categories_product = Product.objects.values_list("domain", flat=True).distinct()
    ctx = {
        "product": product,
        "user_liked": user_liked,
        "comment_form": form,
        "comments": product_comments,
        "no_of_likes": no_of_likes,
        "categories": categories_product,
    }
    return render(request, "newsapp/trendingdetails.html", context=ctx)


def like_news(request, news_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = json.loads(request.body)
        article = get_object_or_404(Article, slug=news_slug)
        status = data["status"]

        exist = article.likes.filter(username=request.user.username).exists()

        if status == "like":
            if not exist:
                article.likes.add(request.user)
                return JsonResponse({"liked": True, "likecount": article.no_of_likes()})
            else:
                return JsonResponse(
                    {
                        "liked": True,
                        "likecount": article.no_of_likes(),
                        "message": "already_liked",
                    }
                )
        if status == "unlike":
            if exist:
                article.likes.remove(request.user)
                return JsonResponse(
                    {"liked": False, "likecount": article.no_of_likes()}
                )
            else:
                return JsonResponse(
                    {
                        "liked": True,
                        "likecount": article.no_of_likes(),
                        "message": "already_unliked",
                    }
                )
    else:
        return JsonResponse({"error": "Invalid Method"})


def like_product(request, product_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = json.loads(request.body)
        article = get_object_or_404(Product, slug=product_slug)
        status = data["status"]

        exist = article.likes.filter(username=request.user.username).exists()

        if status == "like":
            if not exist:
                article.likes.add(request.user)
                return JsonResponse({"liked": True, "likecount": article.no_of_likes()})
            else:
                return JsonResponse(
                    {
                        "liked": True,
                        "likecount": article.no_of_likes(),
                        "message": "already_liked",
                    }
                )
        if status == "unlike":
            if exist:
                article.likes.remove(request.user)
                return JsonResponse(
                    {"liked": False, "likecount": article.no_of_likes()}
                )
            else:
                return JsonResponse(
                    {
                        "liked": True,
                        "likecount": article.no_of_likes(),
                        "message": "already_unliked",
                    }
                )
    else:
        return JsonResponse({"error": "Invalid Method"})


def product_comment(request, product_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = json.loads(request.body)
        form = ProductCommentForm({"comment": data["comment"]})
        product_comment = form.save(commit=False)
        product_comment.user = request.user
        product_comment.product = Product.objects.get(slug=product_slug)
        product_comment.save()

        return JsonResponse(
            {
                "author": request.user.username,
                "commentmessage": product_comment.comment,
                "date": product_comment.created_at,
            }
        )


def news_comment(request, news_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden
    if request.method == "POST":
        data = json.loads(request.body)
        form = ArticleCommentForm({"comment": data["comment"]})
        article_comment = form.save(commit=False)
        article_comment = form.save(commit=False)
        article_comment.user = request.user
        article_comment.article = Article.objects.get(slug=news_slug)
        article_comment.save()

        return JsonResponse(
            {
                "author": request.user.username,
                "commentmessage": article_comment.comment,
                "date": article_comment.created_at,
            }
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


def bookmarked(request):
    if not request.user.is_authenticated:
        redirect("login")
    username = request.user.username
    products_liked_by_user = NewsUser.objects.get(username=username).product_set.all()
    categories = Product.objects.values_list(
        "domain", flat=True
    ).distinct()  # category to base
    print(products_liked_by_user)
    paginator = Paginator(products_liked_by_user, 5)

    try:
        current_p = paginator.page(request.GET.get("page", 1))
    except InvalidPage:
        current_p = paginator.get_page(1)

    return render(
    request,
    "newsapp/trendingproducts.html",
    context={
        "page_obj": current_p,
        "categories": categories,
        "type": "bookmark",
        "object": current_p,
    },
)


