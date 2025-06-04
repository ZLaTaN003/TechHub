from django.contrib import admin
from .models import Article,Domain,NewsUser,Product,ArticleComment,ProductComment
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Domain)
admin.site.register(NewsUser)
admin.site.register(Product)
admin.site.register(ProductComment)
admin.site.register(ArticleComment)


