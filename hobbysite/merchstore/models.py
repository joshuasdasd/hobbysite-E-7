from django.db import models
from django.urls import reverse

from user_management.models import Profile

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    owner = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        default=None
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=None)

    class ProductStatus(models.TextChoices):
        AVAILABLE = "Available"
        ON_SALE = "On Sale"
        OUT_OF_STOCK = "Out of Stock"
    status = models.CharField(
        max_length=12, 
        choices=ProductStatus.choices, 
        default=ProductStatus.AVAILABLE
    )
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:item_detail", args=[self.pk])

class Transaction(models.Model):
    buyer = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.PositiveIntegerField()

    class TransactionStatus(models.TextChoices):
        ON_CART = "On Cart"
        TO_PAY = "To Pay"
        TO_SHIP = "To Ship"
        TO_RECEIVE = "To Receive"
        DELIVERED = "Delivered"
    status = models.CharField(
        max_length=10, 
        choices=TransactionStatus.choices, 
    )

    created_on = models.DateTimeField(auto_now_add=True)