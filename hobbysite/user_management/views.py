from django.db.models.base import Model 
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from .models import Profile
from .forms import ProfileForm, RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user_management/user_detail.html'
    success_url = reverse_lazy('homepage')
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "user_management/register.html"
    success_url = reverse_lazy('login')

    # When creating a new user, create an equivalent Profile object
    def form_valid(self, form):
        user = form.save()
        
        Profile.objects.create(
            user=user,
            display_name=user.username, 
            email_address=user.email  
        )

        return redirect(self.success_url)
