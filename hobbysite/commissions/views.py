# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Commission, Job
from .forms import CommissionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission
from .forms import CommissionForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Commission
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Commission, Job, JobApplication

class CommissionListView(ListView):
    template_name = 'commissions/commission_list.html'

    def get_queryset(self):
        queryset1 = Commission.objects.all()
        queryset2 = JobApplication.objects.all()
        combined_queryset = list(queryset1) + list(queryset2)
        return combined_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch instances of Model1 and Model2
        model1_objects = Commission.objects.all()
        model2_objects = JobApplication.objects.all()
        
        # Add the models to the context
        context['commissions'] = model1_objects
        context['applications'] = model2_objects
        
        return context


class CommissionDetailView(DetailView):
    template_name = 'commissions/commission_detail.html'

    model = Commission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch instances of Model1 and Model2
        model1_objects = Commission.objects.all()
        model2_objects = Job.objects.all()
        
        # Add the models to the context
        context['commissions'] = model1_objects
        context['jobs'] = model2_objects
        
        return context



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
