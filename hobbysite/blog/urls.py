from django.urls import path

from .views import *

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('article/<int:pk>/', ArticleDetailsView.as_view(), name='article_details'),
    path('article/add', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit', ArticleUpdateView.as_view(), name='article_update')
]

app_name = "blog"
