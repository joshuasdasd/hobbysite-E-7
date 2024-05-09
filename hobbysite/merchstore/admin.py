from django.contrib import admin
from .models import Product, ProductType, Transaction

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Transaction)
