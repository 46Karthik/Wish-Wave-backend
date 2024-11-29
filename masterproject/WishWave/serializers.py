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
            'active',


            # Occasion Fields
            'occasionsbirthday',
            'occasionsweddinganniversary',
            'occasionsworkanniversary',
            'occasionsadhoc',
            'occasionsdiwaligift',
            'occasionspoojagifts',
            'occasionscompanyanniversary',
            
            # Celebration Fields
            'celebrateEmployeeBirthday',
            'celebrateEmpWeddingAnniversary',
            'celebrateEmpWorkAnniversary',
            'celebrateSpouseBirthday',
            'celebrateSpouseWeddingAnniversary',
            'celebrateSpouseWorkAnniversary',
            'celebrateKid1Birthday',
            'celebrateKid2Birthday',
            'celebrateKid3Birthday',
            'uniform',
            'varied',
            'employeeLevels',
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
            'employee_id','employee_name', 'company_id', 'employee_dept', 'employee_email', 'employee_phone',
            'whatsapp_phone_number', 'employee_dob', 'employee_doj', 'anniversary_date', 
            'address', 'address2', 'city', 'state', 'pincode', 'country', 'gender', 'marital_status', 'file_path',
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
            'text_font',
            'active',
        ]

class OpsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsView
        fields = [
            'ops_id', 'company_name', 'occasion', 'event_date', 
            'employee_id', 'name_of_person', 'relation', 'address1', 
            'address2', 'city', 'zipcode', 'email_id', 'phone_number', 
            'subscription', 'image_status', 'email_status', 'whatsapp_status', 
            'cake_order_date', 'cake_delivery_date', 'cake_status', 'cake_otp', 
            'gift_order_date', 'gift_delivery_date', 'gift_status', 'gift_otp'
        ]

class EmailWhatsAppTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailWhatsAppTable
        fields = [
            'order_id', 'employee_id', 'company_id', 'email_id', 
            'phone_number', 'email_image_link', 'whatsapp_image_link', 
            'subscription_details', 'event_date', 'image_generation_timestamp', 
            'mail_schedule_time', 'whatsapp_schedule_time', 
            'mail_sent_time', 'whatsapp_sent_time'
        ]

class CakeAndGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeAndGift
        fields = [
            'order_id', 'employee_id', 'company_id', 'email_id', 'phone_number', 
            'delivery_address1', 'delivery_address2', 'delivery_city', 'delivery_zip',
            
            # Cake Delivery Information
            'cake_scheduled_delivery_date', 'cake_scheduled_order_date', 'cake_vendor_id', 
            'cake_shop_name', 'cake_from_address', 'cake_from_city', 'cake_from_state', 
            'cake_from_pincode', 'cake_flavour', 'cake_weight', 'cake_wish_message', 
            'cake_delivery_person_name', 'cake_delivery_person_number', 
            'cake_delivery_verification_link', 'cake_otp','food_id',
            
            # Gift Delivery Information
            'gift_scheduled_delivery_date', 'gift_scheduled_order_date', 'gift_vendor_id', 
            'gift_shop_name', 'gift_from_address', 'gift_from_city', 'gift_from_state', 
            'gift_from_pincode', 'gift_article_number', 'gift_weight', 
            'gift_delivery_person_name', 'gift_delivery_person_number', 
            'gift_delivery_verification_link', 'gift_otp','gift_id'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product_id', 
            'code', 
            'label', 
            'type', 
            'variant', 
            'weight', 
            'price', 
            'pkg', 
            'delivery', 
            'special_packaging', 
            'total'
        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'subscription_id', 'company_id', 'company_name', 'user_id', 'occasion', 'emp_level', 'family',
            'email', 'whatsapp', 'gift', 'custom_gift', 'gift_cost', 
            'custom_gift_cost', 'email_cost', 'whatsapp_cost','key_name'
        ]
class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = ['email_config_id', 'email_host_user', 'email_host_password', 'company_id', 'active']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
