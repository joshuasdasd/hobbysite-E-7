from django import forms
from .models import Commission, Job, JobApplication

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CommissionForm, self).__init__(*args, **kwargs)
        self.fields['author'].disabled = True


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        exclude = ['slots']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(JobApplicationForm, self).__init__(*args, **kwargs)
        self.fields['job'].disabled = True
        self.fields['applicant'].disabled = True