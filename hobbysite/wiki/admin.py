from django.contrib import admin
from .models import Article, ArticleCategory, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(Comment)