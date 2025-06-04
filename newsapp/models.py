from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


# Create your models here.
class NewsUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = "username"


class Domain(models.Model):
    category = models.CharField(max_length=200, default="", unique=True)

    def __str__(self):
        return self.category


class Article(models.Model):
    title = models.CharField(max_length=2000, unique=True)
    short_description = models.CharField(max_length=4000)
    image_url = models.CharField(max_length=400,default="https://images.unsplash.com/photo-1624269305543-efbc8d89f1d3?q=80&w=3125&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    published_at = models.DateTimeField(auto_now_add=True)
    source_link = models.CharField(max_length=400)
    author = models.CharField(max_length=100, null=True)
    post_published = models.DateField()
    summary = models.TextField(default="No Summary Yet")
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="articles"
    )
    slug = models.SlugField(max_length=500)
    likes = models.ManyToManyField(NewsUser, blank=True)

    def __str__(self):
        return self.title[:10]

    def save(self, *args, **kwargs):
        title_items = self.title.split()[:4]
        title_string = " ".join(title_items)
        self.slug = slugify(title_string)
        return super().save(*args, **kwargs)

    def no_of_likes(self):
        return self.likes.count()


class Product(models.Model):
    name = models.CharField(max_length=400, unique=True)
    short = models.CharField(max_length=400)
    description = models.CharField(max_length=3000)
    thumbnail = models.CharField(max_length=400,default="https://images.unsplash.com/photo-1597484661973-ee6cd0b6482c?q=80&w=3174&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    media = models.CharField(max_length=400,default="https://images.unsplash.com/photo-1556888335-23631cd2801a?q=80&w=2906&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    summary = models.TextField()
    featuredat = models.DateField()
    upvotes = models.IntegerField()
    link = models.CharField(max_length=400)
    domain = models.CharField(max_length=400)
    slug = models.SlugField(max_length=500)
    likes = models.ManyToManyField(NewsUser, blank=True)
    domain_slug = models.SlugField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        title_items = self.name.split()[:4]
        title_string = " ".join(title_items)
        self.domain_slug = slugify(self.domain)
        self.slug = slugify(title_string)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name[:10]

    def no_of_likes(self):
        return self.likes.count()
    
class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"[:10]
    
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"[:10]