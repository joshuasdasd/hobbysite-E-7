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
class AuthorProfileMixin(object):
    def author_profile(self):
        if self.request.user.is_authenticated:
            author, _ = Profile.objects.get_or_create(user=self.request.user)
            return author
        return None

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'

    def ctx_data(self, **kwargs): #articles that are created by the log-in user are in a separate..
        ctx = super().ctx_data(**kwargs)
        author = self.author_profile()
        if author:
            if author:
                articles_by_author = Article.objects.filter(author=author)
                ctx['articles_by_author'] = articles_by_author
            return ctx

class ArticleDetailView(DetailView): #will do later
    model = Article
    template_name = 'wiki/article_detail.html'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_create.html'

    def get_success_url(self):
        return reverse_lazy('wiki:article_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        author = Profile.objects.get(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)

    def cxt_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Profile.objects.get(user=self.request.user)
        context['form'] = ArticleForm(initial={'author': author})
        return context

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_update.html'

    def get_success_url(self):
        return reverse_lazy('wiki:article_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)