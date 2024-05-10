from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from .models import Product, Transaction

# Create your views here.
def index(request):
    return HttpResponse('')

class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'merchstore/product_create.html'
    fields = '__all__'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'merchstore/product_update.html'
    fields = '__all__'

class TransactionListView(ListView):
    model = Transaction
    template_name = 'merchstore/transaction_list.html'