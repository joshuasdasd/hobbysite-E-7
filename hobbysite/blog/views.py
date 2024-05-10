import datetime

from django.shortcuts import *
from django.views.generic.edit import *
from django.views.generic.list import *
from django.views.generic.detail import *
from django.contrib.auth.mixins import *

from .forms import *
from .models import *
from user_management.models import Profile


class AuthorProfileMixin(object):
    def author_profile(self):
        if self.request.user.is_authenticated:
            author, _ = Profile.objects.get_or_create(user=self.request.user)
            return author
        return None


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_objects = ArticleCategory.objects.all()
        article_objects = Article.objects.all()

        context['categories'] = category_objects
        context['articles'] = article_objects

        return context


class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'blog/article_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        article = self.get_object()
        context['article'] = article

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['comments'] = article.comment_set.all()

        return context

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.author = form.cleaned_data.get('author')
            comment.article = form.cleaned_data.get('article')
            comment.entry = form.cleaned_data.get('entry')
            comment.created_on = form.cleaned_data.get('created_on')
            comment.updated_on = form.cleaned_data.get('updated_on')
            comment.save()
            return redirect('blog:article_details', kwargs={'pk': self.object.pk})

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy('blog:articles_list')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.created_on = datetime.datetime.now()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'blog/article_update.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_details', kwargs={'pk': self.object.pk})
