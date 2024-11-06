from django.urls import path
from .views import *


urlpatterns = [
    path('get-company/', RegisterCompany.as_view(), name='get-company'),
    path('get-company/<int:id>/', RegisterCompany.as_view(), name='get-company'),
    path('register-company/', RegisterCompany.as_view(), name='register-company'),
    path('update-company/', RegisterCompany.as_view(), name='update-company'),
    path('genrate-otp/', send_mail_otp.as_view(), name='genrate-otp'),
    path('verify-otp/', verify_otp.as_view(), name='verify_otp'),
    path('get-Company-code/', get_company_code.as_view(), name='get-Company-code'),
    path('add_employee/', EmployeeCreateView.as_view(), name='add_employee'),
    path('employee/',EmployeeCreateView.as_view(), name='get_employee'),
    path('employee/<int:id>/', EmployeeCreateView.as_view(), name='get_employee'),
    path('employee-bulk-upload/', EmployeeBulkUploadView.as_view(), name='employee-bulk-upload'),
    path('vendor/', VendorView.as_view(), name='vendor'),
    path('vendor/<int:id>/', VendorView.as_view(), name='vendor'),
    path('Upload-image/', S3ImageView.as_view(), name='Upload-image'),
    path('template-image/', TemplateImageView.as_view(), name='template-image'),
    path('company-template-config/', CompanyTemplateConfigView.as_view(), name='company-template-config'),
    path('ops-table/', OpsTableView.as_view(), name='ops-table'),
    path('Subscription/', SubscriptionTableView.as_view(), name='Subscription-table'),
    path('SubscriptionEmployeedata/', SubscriptionEmployeedata.as_view(), name='Subscription-employeedata'),
]