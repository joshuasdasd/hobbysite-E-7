from django.db import models
from django.utils import timezone
from django.urls import reverse
from user_management.models import Profile

# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'  
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True, blank = True)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
    )
    entry = models.TextField()
    header_images = models.ImageField(upload_to='images/', null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('wiki:article_detail', args=[self.pk])
    
class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.author}'