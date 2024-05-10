from django.urls import path
from .views import index
from .views import *

urlpatterns = [
    path('items/', ProductListView.as_view(), name='item_list'),
    path('item/<int:pk>/', ProductDetailView.as_view(), name='item_detail'),
    path('item/add/', ProductCreateView.as_view(), name='item_add'),
    path('item/<int:pk>/edit/', ProductUpdateView.as_view(), name='item_edit'),
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list')
    # path('', index, name='index'),
]

app_name = "merchstore"