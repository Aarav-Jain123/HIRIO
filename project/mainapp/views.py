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
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
@login_required(login_url="/landing/")
def index(requests):
    return HttpResponse('Hello World')


def otp(requests):
    return HttpResponse('OTP')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data.get('email'), password=form.data.get('password1'))
            if user is None:
                request.session['auth_token'] = otp_generator()
                request.session['signup_data'] = form.data
                send_otp(form.data.get('email'), request.session['auth_token'])
                request.session.set_expiry(300)
            else:
                messages.error(request, '''Seems like the account already exists, please go to /login.''')
                return redirect('/signup')
            return redirect('/otp')
    else:
        form = RegisterForm()
    
    logout(request)

    return render(request, 'registration/signup.html', {"form": form})


def landing_page(requests):
    return render(requests, 'main/Revolutionize HR_ Building an AI-Powered Assistant.html')


def otp_generator():
    r1, r2, r3, r4, r5, r6 = randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9)
    r = f'{r1}{r2}{r3}{r4}{r5}{r6}'
    return r


def send_otp(email, token):
    subject = 'Your OTP is here'
    msg = f'Here is your otp: {token}.'
    from_email = settings.EMAIL_HOST_USER
    recipients = [email]
    send_mail(subject, msg, from_email, recipients)


def authenticate_user(userr_id):
    userr = UserProfile.objects.filter(user_id=userr_id).exists()
    
    return userr


def add_user(request):
    user = authenticate(username=request.session['email'], password=request.session['password'])
    if user is not None:
        login(request, user)
    if user is None:
        user = User.objects.create_user(username=request.session['email'], name=request.session['name'], email=request.session['email'])
        user.set_password(request.session['password'])
        user.save()
        
        custom_user = UserProfile.objects.create(user=user)
        custom_user.save()
        

@login_required(login_url="/")
def logout_page(request):
    logout(request)
    return redirect('/landing/')


def delete_user_page(request):
    auth_data = request.data
    username_of_user = request.user.username
    
    try:
    
        user = authenticate(username=username_of_user, password=auth_data['password'])
        if user:
            user.objects.delete()
            res = [{'key': 0, 'response': 'User deleted successfully!'}]
        
            return Response(data=res)
        else:
            res = [{'key': 0, 'response': 'Something seems wrong, please check your credentials.'}]
        
    except Exception as e:
        res = [{'key': 0, 'response': e}]
    
    return Response(data=res)


def otp_page(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == request.session['auth_token']:
            data = request.session['signup_data']
            user = User.objects.create_user(first_name=data.get('first_name'), username=data.get('email'), email=data.get('email'))
            user.set_password(data.get('password1'))
            user.save()
            
            custom_user = UserProfile.objects.create(userr=user, email=data.get('email'), name=data.get('first_name'))
            custom_user.save()
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request, 'Invalid OTP')            
    return render(request, 'registration/otp.html')