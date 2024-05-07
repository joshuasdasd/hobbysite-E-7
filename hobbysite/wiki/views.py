from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ArticleCategory
from .forms import ArticleForm, CommentForm
from user_management.models import Profile
from django.urls import reverse_lazy

# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'