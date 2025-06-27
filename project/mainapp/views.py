from rest_framework.decorators import api_view
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from random import randint
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import random
import json


# Create your views here.
def index(requests):
    return HttpResponse('Hello World')


def otp(requests):
    return HttpResponse('OTP')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})