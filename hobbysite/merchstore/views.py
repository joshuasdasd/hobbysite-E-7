from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product

# Create your views here.
def index(request):
    return HttpResponse('')

class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'

class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'