from django.urls import path

from .views import index
from .views import item_list, item_1

urlpatterns = [
    path('items/', item_list, name='item_list'),
    path('', index, name='index'),
]

app_name = "merchstore"