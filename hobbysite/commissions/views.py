from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CommissionForm
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from .models import Commission, Job, JobApplication
from django.forms import BaseModelForm, inlineformset_factory
from django.db.models.signals import post_save
from django.dispatch import receiver


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

        if self.request.user.is_authenticated:
            # If user is logged in, filter commissions by their profile
            model3_objects = Commission.objects.all().filter(author=self.request.user.profile)
            model2_objects = JobApplication.objects.all().filter(applicant=self.request.user.profile)
        else:
            # If user is not logged in, provide an empty queryset
            model3_objects = Commission.objects.none()
            model2_objects = JobApplication.objects.none()


        # Add the models to the context
        context['commissions'] = model1_objects
        context['applications'] = model2_objects
        context['user_commissions'] = model3_objects
        
        return context



class CommissionDetailView(DetailView):
    template_name = 'commissions/commission_detail.html'
    model = Commission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        comm = Commission.objects.filter(pk=pk).first()

        model1_objects = Commission.objects.all()
        model2_objects = Job.objects.filter(commission=comm)

        # Calculate total initial required manpower (mpr)
        mpr = model2_objects.aggregate(total_manpower=Sum('manpower_required'))['total_manpower'] or 0

        # Calculate total accepted manpower for this commission
        accepted_manpower = JobApplication.objects.filter(job__commission=comm, status='Accepted').count()

        # Subtract accepted manpower from the total initial required manpower to get the remaining manpower
        remaining_manpower = mpr - accepted_manpower

        # Add the models to the context
        context['commissions'] = model1_objects
        context['jobs'] = model2_objects
        context['mpr'] = mpr
        context['remaining_manpower'] = remaining_manpower
        
        return context


class CommissionCreateView(LoginRequiredMixin, CreateView):

    JobInlineFormSet = inlineformset_factory(
    Commission, Job, form=JobForm, extra=5, can_delete=False
)
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = self.JobInlineFormSet(self.request.POST)
        else:
            context['job_formset'] = self.JobInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        return {'author': self.request.user.profile}

    def get_success_url(self):
        return reverse_lazy('commissions:commission_detail', kwargs={'pk': self.object.pk})


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = self.JobInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['job_formset'] = self.JobInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        return {'author': self.request.user.profile}

    def get_success_url(self):
        return reverse_lazy('commissions:commission_detail', kwargs={'pk': self.object.pk})

    JobInlineFormSet = inlineformset_factory(Commission, Job, form=JobForm, extra=5, can_delete=False)

from django.shortcuts import get_object_or_404

class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    form_class = JobApplicationForm
    template_name = 'commissions/applied_to.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=pk)
        context['job_name'] = job  # Add the job role to context
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=pk)
        initial['job'] = job
        initial['applicant'] = self.request.user.profile
        return initial
    
    def get_success_url(self):
        return reverse_lazy('commissions:commission_list')


@receiver(post_save, sender=JobApplication)
def update_commission_status(sender, instance, created, **kwargs):
    if created:
        # Check if the manpower required for the job is now full
        job = instance.job
        total_applications = job.job_applications.count()
        if total_applications >= job.manpower_required:
            # Update the status of the associated Commission
            commission = job.commission
            commission.status = 'Full'
            commission.save()
    

@receiver(post_save, sender=JobApplication)
def update_job_status(sender, instance, created, **kwargs):
    if created:
        # Check if the manpower required for the job is now full
        job = instance.job
        total_applications = job.job_applications.count()
        if total_applications >= job.manpower_required:
            # Update the status of the job to 'Full'
            job.status = 'Full'
            job.save()
