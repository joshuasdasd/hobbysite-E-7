from django.shortcuts import *
from django.views.generic.list import *
from django.views.generic.detail import *

from .models import *


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'


class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'blog/article_details.html'
