from django.contrib import admin

from .models import *


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline, ]
    fields = ['name', 'description']


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    fields = ['title', 'category', 'created_on', 'entry']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)