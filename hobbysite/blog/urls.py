from django.urls import path

from .views import *

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('article/<int:pk>/', ArticleDetailsView.as_view(), name='article_details'),
    path('article/add', ArticleCreateView.as_view(),name='create'),
    path('recipe/<int:pk>/edit', ArticleUpdateView.as_view(), name='edit')
]


app_name = "blog"

# path('recipes/list/', RecipesListView.as_view(), name='recipes_list'),
#     path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe_detail'),
#     path('recipe/add', RecipeCreateView.as_view(), name='create'),
#     path('recipe/<int:pk>/add_image', RecipeAddImageView.as_view(), name='add_image'),
#     path('accounts/', include('django.contrib.auth.urls'))