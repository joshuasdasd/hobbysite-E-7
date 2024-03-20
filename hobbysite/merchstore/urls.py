from django.urls import path
from .views import index
from .views import ItemListView, ItemDetailView

urlpatterns = [
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('', index, name='index'),
]

app_name = "merchstore"