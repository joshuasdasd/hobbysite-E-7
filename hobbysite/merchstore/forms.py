from django import forms
from .models import *

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner']
