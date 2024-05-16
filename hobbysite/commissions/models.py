from django.db import models
from user_management.models import Profile

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_commissions', null=True)

    status = models.CharField(max_length=12, choices=(
        ('Open', 'Open'),
        ('Full' ,'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ), default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (by {self.author})"
    
    class Meta:
        ordering = ["created_on"]


class Job(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='jobs')
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    slots = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices = (('Open', 'Open'),('Full', 'Full')), default='Open')
    class Meta:
        ordering = ["-status", "-manpower_required", "role"]

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices = (('Pending', 'Pending'),('Accepted', 'Accepted'), ('Rejected', 'Rejected')), default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-status", "-applied_on"]


