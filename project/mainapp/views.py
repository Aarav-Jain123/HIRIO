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
from .vatVerifier import verify_vat
from django.shortcuts import get_object_or_404
from .aiFunctionalities import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@login_required(login_url="/landing/")
def index(request):
    if request.method == "POST":
        company_id = request.POST.get("company-id")
        if company_id:
            company_to_delete = Company.objects.filter(id=company_id).first()
            if company_to_delete and (company_to_delete.owner == request.user):
                company_to_delete.delete()
                return redirect('/')  # or your URL name

    companies = Company.objects.filter(owner=request.user)
    return render(request, 'main/index.html', {'companies': companies})


def otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        try:
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
        except Exception as e:
            print(e)        
    return render(request, 'registration/otp.html')


def signup(request):
    logout(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
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
            except Exception as e:
                print(e)
    else:
        form = RegisterForm()
    
    logout(request)

    return render(request, 'registration/signup.html', {"form": form})


def landing_page(requests):
    logout(requests)
    return render(requests, 'main/landingPage.html')


def otp_generator():
    r1, r2, r3, r4, r5, r6 = randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9)
    r = f'{r1}{r2}{r3}{r4}{r5}{r6}'
    return r


def send_otp(email, token):
    subject = 'Your OTP is here'
    msg = f'Here is your otp: {token}.'
    try:
        from_email = settings.EMAIL_HOST_USER
        recipients = [email]
        send_mail(subject, msg, from_email, recipients)
    except Exception as e:
        print(e)


def authenticate_user(userr_id):
    userr = UserProfile.objects.filter(user_id=userr_id).exists()
    
    return userr


def add_user(request):
    try:
        user = authenticate(username=request.session['email'], password=request.session['password'])
        if user is not None:
            login(request, user)
        if user is None:
            user = User.objects.create_user(username=request.session['email'], name=request.session['name'], email=request.session['email'])
            user.set_password(request.session['password'])
            user.save()
            
            custom_user = UserProfile.objects.create(user=user)
            custom_user.save()
    except Exception as e:
        print(e)
        

@login_required(login_url="/")
def logout_page(request):
    logout(request)
    return redirect('/landing/')


@login_required(login_url="/login")
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            # vat = verify_vat(country_code=form.data.get('country_code'), vat_number=form.data.get('country_code'))['valid']
            # if vat:
                company = form.save(commit=False)
                company.owner = request.user
                f = train_rag(url=company.policy_url, company_name=company.company_name)
                company.save()
                messages.success(request, f)
                return redirect('Company dashboard', slug=company.company_link)
            # else:
                # messages.error(request, 'VAT ID is invalid')
    else:
        form = CompanyForm()

    return render(request, 'main/companyForm.html', {"form": form})


@login_required(login_url='/landing/')
def company_dashboard(request, slug):
    companies = Company.objects.filter(company_name=slug)
    company = get_object_or_404(companies, company_link=slug)
    return render(request, 'main/companyDashboard.html', {'company_name': company.company_name})

# @csrf_exempt
@api_view(['POST'])
def chatModel(request):
    res = request.data 
    answer = load_ai(res["company_name"], res['form-prompt'])
    response = [{'key': 0, 'answer': answer}] 
    print(response)
    return Response() # para: data=response
