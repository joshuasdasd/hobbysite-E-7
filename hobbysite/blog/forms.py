from django import forms
from .models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = Article.header_image
        fields = '__all__'

