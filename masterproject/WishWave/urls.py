from django.urls import path
from .views import *


urlpatterns = [
    path('get-company/', RegisterCompany.as_view(), name='get-company'),
    path('register-company/', RegisterCompany.as_view(), name='register-company'),
    path('genrate-otp/', send_mail_otp.as_view(), name='genrate-otp'),
    path('verify-otp/', verify_otp.as_view(), name='verify_otp'),
    path('get-Company-code/', get_company_code.as_view(), name='get-Company-code'),
]