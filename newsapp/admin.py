from django.contrib import admin
from .models import Article,Domain
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Domain)
