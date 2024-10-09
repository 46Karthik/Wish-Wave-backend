from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'company_id',
            'country', 
            'company_name', 
            'company_GSTR_no', 
            'company_type', 
            'industry', 
            'address1', 
            'address2', 
            'address3', 
            'city', 
            'state', 
            'pincode', 
            'contact_name', 
            'contact_email', 
            'contact_phone_no', 
            'contact_designation', 
            'contact_role_app', 
            'active'
        ]
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'company_id',
            'role_id',
            'username',
            'password',
            'active',
            'created_date',
            'modified_date',
            'email_id',
            'phone_no',
            'otp',
            'otp_generated_time',
            'is_verified',
        ]