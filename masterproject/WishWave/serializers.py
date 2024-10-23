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



class SpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spouse
        fields = ['spouse_name', 'spouse_dob', 'spouse_email', 'spouse_phone']

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['child_name', 'child_gender', 'child_dob']

class EmployeeSerializer(serializers.ModelSerializer):
    spouse = SpouseSerializer(required=False)
    children = ChildSerializer(many=True, required=False)

    class Meta:
        model = Employees
        fields = [
            'employee_name', 'company_id', 'employee_dept', 'employee_email', 'employee_phone',
            'whatsapp_phone_number', 'employee_dob', 'employee_doj', 'anniversary_date', 
            'address', 'state', 'pincode', 'country', 'gender', 'marital_status', 'file_path',
            'spouse', 'children'
        ]
    def create(self, validated_data):
        # Extract nested data for Spouse and Children
        spouse_data = validated_data.pop('spouse', None)
        children_data = validated_data.pop('children', [])

        # Create the Employee object
        employee = Employees.objects.create(**validated_data)

        # Create the Spouse object if spouse data is provided
        if spouse_data:
            Spouse.objects.create(employee=employee, **spouse_data)

        # Create the Child objects if children data is provided
        for child_data in children_data:
            Child.objects.create(employee=employee, **child_data)

        return employee

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id',
            'vendor_type',
            'name_of_vendor',
            'contact_no',
            'mobile_no',
            'email',
            'address_1',
            'address_2',
            'town_village',
            'city',
            'state',
            'pin',
            'gps_location_link',
            'manager_name',
            'manager_phone',
            'manager_email',
            'store_general_contact',
            'gst_number',
            'price',
            'remark',
            'headoffice_address',
            'headoffice_phone',
            'headoffice_email',
            'headoffice_contact_person',
            'headoffice_contact_designation',
            'headoffice_contact_phone',
            'headoffice_contact_person_email',
            'bank_name',
            'bank_account_no',
            'bank_ifsc',
            'bank_branch',
            'bank_address',
            'bank_account_name',
        ]   

class TemplateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateImage
        fields = ['img_Id','name', 'path', 'company_id']

class CompanyTemplateConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTemplateConfig
        fields = [
            'config_id', 
            'company_id', 
            'template_img_id', 
            'logo_name', 
            'logo_path', 
            'logo_size', 
            'logo_x', 
            'logo_y', 
            'content', 
            'content_x', 
            'content_y', 
            'employname_x', 
            'employname_y', 
            'text_colourcode', 
            'text_size', 
            'text_font'
        ]