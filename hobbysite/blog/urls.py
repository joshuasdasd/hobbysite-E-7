from django.urls import path

from .views import *

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('article/<int:pk>/', ArticleDetailsView.as_view(), name='article_details'), ]

app_name = "blog"
