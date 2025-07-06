from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', "email", "password1", "password2"]

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["company_name", "description", 'VAT_ID', 'policy_url', 'linkedin_url', 'employee_list', 'country_code']