# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, RegistrationForm

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user_management/user_detail.html'
    success_url = reverse_lazy('commissions:commission_list')

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "user_management/register.html"
    success_url = reverse_lazy('commissions:commission_list')

    def form_valid(self, form):
        user = form.save()
        
        Profile.objects.create(
            user=user,
            display_name=user.username, 
            email_address=user.email  
        )

        return redirect(self.success_url)
