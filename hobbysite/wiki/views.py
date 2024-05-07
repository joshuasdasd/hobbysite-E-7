from django.shortcuts import redirect
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
    model = ArticleCategory
    template_name = 'wiki/article_list.html'

    def context_data(self, **kwargs): #articles that are created by the log-in user are in a separate..
        context = super().context_data(**kwargs)
        author = self.author_profile()
        if author:
            if author:
                articles_created = Article.objects.filter(author=author)
                context['articles_created'] = articles_created
            return context

class ArticleDetailView(DetailView): #will do later
    model = Article
    template_name = 'wiki/article_detail.html'

    def context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object
        context['article'] = article

        articles_created = Article.objects.filter(author=article.author).exclude(pk=article.pk)
        context['articles_created'] = articles_created

        if self.request.user.is_authenticated:
            author_profile = Profile.objecs.filter(user=self.request.user).first()
            context['author_profile'] = author_profile
            context['comment_form'] = CommentForm()
            return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        author = Profile.objects.get(user=self.request.user)
        article = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.article = article
            comment.save()
            return redirect('wiki:article_detail', pk=article.pk)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

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

    def context_data(self, **kwargs):
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
    
    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.object.pk)
        return context
    
    #https://stackoverflow.com/questions/22646771/user-authentication-in-django
    #https://stackoverflow.com/questions/58067267/django-filtering-articles-by-categories
    #https://stackoverflow.com/questions/60497516/django-add-comment-section-on-posts-feed