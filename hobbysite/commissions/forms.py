from django import forms
from .models import Commission, Job

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = "__all__"
        exclude = ['author'] # Exclude the author, this is automatically set to the user's Profile