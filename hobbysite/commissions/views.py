from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Commission
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Commission, Job
from .forms import CommissionForm

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'
    context_object_name = 'commission'

# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Commission, Job
from .forms import CommissionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Commission
from .forms import CommissionForm

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_create.html'
    success_url = reverse_lazy('commissions:commission_list')

    def form_valid(self, form):
        # Automatically set the author as the logged-in user's profile
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_update.html'
    success_url = reverse_lazy('commissions:commission_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        commission = self.object
        # Check if all related jobs have status 'FULL'
        if commission.job_set.exclude(status='FULL').exists():
            commission.status = 'OPEN'
        else:
            commission.status = 'FULL'
        commission.save()
        return response
