from django.db import models
from django.forms import ModelForm
from django.urls import *
from django import forms


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Article Categories"


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL(),
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        related_name='category',
        null=True,
    )
    entry = models.TextField(null=True)
    # header_image = models.ImageField(upload_to='images/', null=True)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}\non {}\n\n{}\nLast updated:{}'.format(self.title, self.created_on, self.entry, self.updated_on)

    def get_absolute_url(self):
        return reverse('article_details', args=[str(self.title)])

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL(),
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']