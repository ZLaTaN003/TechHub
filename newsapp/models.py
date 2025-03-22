from django.db import models

# Create your models here.


class Domain(models.Model):
    category = models.CharField(max_length=200, default="", unique=True)

    def __str__(self):
        return self.category


class Article(models.Model):
    title = models.CharField(max_length=2000)
    short_description = models.CharField(max_length=4000)
    content = models.TextField()
    image_url = models.CharField(max_length=400)
    published_at = models.DateTimeField(auto_now_add=True)
    source_link = models.CharField(max_length=400)
    author = models.CharField(max_length=100, null=True)
    post_published = models.DateField()
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="articles",default=""
    )

    def __str__(self):
        return self.title[:10]
