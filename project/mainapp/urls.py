from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='Index'),
    path('signup/', signup, name='Signup'),
    path('otp/', otp, name='OTP'),
    path('logoutt/', logout_page, name='Logout'),
    path('landing/', landing_page, name='Landing page'),
    path('company-create-form/', create_company, name='Company creation form'),
    path('company-dashboard/<slug:slug>/', company_dashboard, name='Company dashboard'),
    path('chat-model/', chatModel, name='chat model')
]