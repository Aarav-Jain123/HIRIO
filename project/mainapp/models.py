from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from autoslug import AutoSlugField


# Create your models here.
class UserProfile(models.Model):
    userr = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(default='-', max_length=150)
    name = models.CharField(default='', max_length=150)
    
    
    def __str__(self):
        return self.email


class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    VAT_ID = models.CharField(max_length=200, editable=True)
    policy_url = models.URLField(max_length=200, editable=True)
    # policy_rag_file = models.FileField(null=True, editable=True, upload_to='vectored_policy/', blank=True)
    linkedin_url = models.URLField(max_length=200, editable=True)
    employee_list = models.FileField(editable=True, upload_to=f'employee_lists/{company_name}', validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])]) 
    country_code = models.CharField(max_length=20, editable=True, default='-')
    company_link = AutoSlugField(populate_from='company_name', unique=True)
    
    
    def __str__(self):
        return self.company_name + "\n" + self.description
