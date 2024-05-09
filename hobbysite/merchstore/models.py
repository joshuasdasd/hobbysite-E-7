from django.db import models
from django.urls import reverse

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True
    )
    owner = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        null=True
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(null=True)
    status_choices = [
        ('Out of stock', 'Out of stock'),
        ('Available', 'Available'),
        ('On sale', 'On sale')
    ]
    status = models.CharField(
        max_length=12, 
        choices=status_choices, 
        default='Available'
    )

    def __str__(self):
        return self.name

class Transaction(models.Model):
    buyer = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.PositiveIntegerField()
    status_choices = [
        ('On cart', 'On cart'),
        ('To pay', 'To pay'),
        ('To ship', 'To ship'),
        ('To receive', 'To receive'),
        ('Delivered', 'Delivered')
    ]
    status = models.CharField(
        max_length=10, 
        choices=status_choices, 
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['buyer']
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'

    def get_absolute_url(self):
        return reverse('merchstore:item_detail', args=[self.pk])