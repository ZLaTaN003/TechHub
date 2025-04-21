from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.
class NewsUser(AbstractUser):
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = "username"


class Domain(models.Model):
    category = models.CharField(max_length=200, default="", unique=True)

    def __str__(self):
        return self.category


class Article(models.Model):
    title = models.CharField(max_length=2000,unique=True)
    short_description = models.CharField(max_length=4000)
    image_url = models.CharField(max_length=400)
    published_at = models.DateTimeField(auto_now_add=True)
    source_link = models.CharField(max_length=400)
    author = models.CharField(max_length=100, null=True)
    post_published = models.DateField()
    summary = models.TextField(default="Default summary")
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="articles"
    )
    slug = models.SlugField(max_length=500)
    likes = models.ManyToManyField(NewsUser,blank=True)

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
    name = models.CharField(max_length=400,unique=True)
    short = models.CharField(max_length=400)
    description = models.CharField(max_length=3000)
    thumbnail = models.CharField(max_length=400)
    media = models.CharField(max_length=400)
    summary = models.TextField(default="Default Summary")
    featuredat = models.DateField()
    upvotes = models.IntegerField(default=0)
    link = models.CharField(max_length=400,default="")
    domain = models.CharField(max_length=400,default="")



    def __str__(self):
        return self.name[:10]