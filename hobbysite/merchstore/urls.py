from django.urls import path
from .views import index
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView
from .views import TransactionListView

urlpatterns = [
    path('items/', ProductListView.as_view(), name='item_list'),
    path('item/<int:pk>/', ProductDetailView.as_view(), name='item_detail'),
    path('item/add/', ProductCreateView.as_view(), name='item_add'),
    path('item/<int:pk>/edit/', ProductUpdateView.as_view(), name='item_edit'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list')
    # path('', index, name='index'),
]

app_name = "merchstore"