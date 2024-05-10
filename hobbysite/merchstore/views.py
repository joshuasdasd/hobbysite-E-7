from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import is_valid_path
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from user_management.models import Profile
from .models import Product, ProductType, Transaction
from .forms import ProductForm, TransactionForm

# Create your views here.
def index(request):
    return HttpResponse('')

class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'

    form = TransactionForm()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                transaction = Transaction()
                transaction.buyer = request.user.profile
                transaction.product = self.get_object()
                transaction.amount = form.cleaned_data.get("amount")
                product = self.get_object()
                product.stock = product.stock - transaction.amount
                product.save()
                transaction.status = Transaction.TransactionStatus.ON_CART
                transaction.save()
                return HttpResponseRedirect("/merchstore/cart")
            else:
                return HttpResponseRedirect("/registration/login?next=/merchstore/item/{}".format(self.get_object().pk))
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = "/registration/login"
    model = Product
    template_name = 'merchstore/product_create.html'
    fields = ["name", "product_type", "description", "price", "stock", "status"]

    form = ProductForm()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product()
            product.name = form.cleaned_data.get("name")
            product.product_type = form.cleaned_data.get("product_type")
            product.description = form.cleaned_data.get("description")
            product.price = form.cleaned_data.get("price")
            product.stock = form.cleaned_data.get("stock")
            product.status = form.cleaned_data.get("status")
            product.owner = request.user.profile
            product.save()
            return HttpResponseRedirect("/merchstore/items")
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'merchstore/product_update.html'
    fields = ["name", "product_type", "description", "price", "stock", "status"]

class CartListView(ListView):
    model = Profile
    template_name = 'merchstore/cart_list.html'    

class TransactionListView(ListView):
    model = Profile
    template_name = 'merchstore/transaction_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile_transactions = [[Profile, i.transactions.all()]
                               for i in Profile.objects.all()]
        ctx["profile_transactions"] = profile_transactions
        return ctx