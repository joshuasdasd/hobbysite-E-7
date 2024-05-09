from django.urls import path
from .views import UserUpdateView, UserCreateView
from django.views.generic import TemplateView


app_name = 'user_management'

urlpatterns = [
    path('profile/', UserUpdateView.as_view(), name='user_detail'),
    path('register/', UserCreateView.as_view(), name='user_registration'),
    path('login_success/', TemplateView.as_view(template_name='homepage.html'))
]