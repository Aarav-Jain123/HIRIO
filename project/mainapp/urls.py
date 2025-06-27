from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='Index'),
    # path('home/', home_page, name='Home'),    
    path('signup/', signup, name='Signup'),
    # path('shop/', books_page, name='Rewards'),
    path('otp/', otp, name='OTP'),
    # path('quiz/', quiz, name='Quiz'),
    # path('logout/', logout_page, name='Logout'),
    # path('fact-abt-water/', fact_abt_water, name='Fact about water'),
    path('landing/', landing_page, name='Landing page')
]