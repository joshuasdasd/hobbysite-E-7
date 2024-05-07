from django.db import models
from user_management.models import Profile

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_commissions', null=True)

    status = models.CharField(max_length=12, choices=(
        ('OPEN', 'Open'),
        ('FULL' ,'Full'),
        ('COMPLETED', 'Completed'),
        ('DISCONTINUED', 'Discontinued'),
    ), default='OPEN')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (by {self.author})"
    
    class Meta:
        ordering = ["created_on"]


class Job(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(max_length=10, choices = (('OPEN', 'Open'),('FULL', 'full')), default='OPEN')

    class Meta:
        ordering = ["-status", "-manpower_required", "role"]

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices = (('PENDING', 'Pending'),('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')), default='PENDING')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["status", "-applied_on"]


