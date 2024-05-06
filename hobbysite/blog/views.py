from django.shortcuts import *
from django.views.generic.edit import *
from django.views.generic.list import *
from django.views.generic.detail import *

from .forms import *
from .models import *


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'


class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'blog/article_details.html'


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'recipe_create.html'


class ArticleUpdateView(UpdateView):
    model = Article
    fields = '__all__'
    template_name = ''
    form_class = ''





# class RecipeAddImageView(LoginRequiredMixin, UpdateView):
#     model = Article
#     form_class = RecipeImageForm
#     template_name = 'recipe_add_image.html'
#
#     def get_success_url(self):
#         return reverse_lazy('ledger:recipes', kwargs={'pk': self.kwargs['pk']})