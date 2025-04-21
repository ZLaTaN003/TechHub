from django.contrib import admin
from .models import Article,Domain,NewsUser,Product
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Domain)
admin.site.register(NewsUser)
admin.site.register(Product)
