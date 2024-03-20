from django.contrib import admin
from .models import Product, ProductType

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductType)
