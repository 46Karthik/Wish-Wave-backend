from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    role_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company_id = models.CharField(max_length=255, null=False)
    role_id = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)                    
    modified_date = models.DateTimeField(auto_now=True)       
    email_id = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=255, unique=True)
    otp = models.CharField(max_length=10, blank=True, null=True)
    otp_generated_time = models.DateTimeField(auto_now_add=True)     
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)   
    country = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_GSTR_no = models.CharField(max_length=255, blank=True, null=True)  
    company_type = models.CharField(max_length=255, blank=True, null=True)    
    industry = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, blank=True, null=True)         
    address2 = models.CharField(max_length=255, blank=True, null=True)         
    address3 = models.CharField(max_length=255, blank=True, null=True)         
    city = models.CharField(max_length=255, blank=True, null=True)             
    state = models.CharField(max_length=255, blank=True, null=True)            
    pincode = models.CharField(max_length=20, blank=True, null=True)           
    contact_name = models.CharField(max_length=255, blank=True, null=True)     
    contact_email = models.EmailField(blank=True, null=True)                   
    contact_phone_no = models.CharField(max_length=20, blank=True, null=True)  
    contact_designation = models.CharField(max_length=255, blank=True, null=True) 
    contact_role_app = models.CharField(max_length=255, blank=True, null=True)     
    active = models.BooleanField(default=False)                                
    created_date = models.DateTimeField(auto_now_add=True)                    
    modified_date = models.DateTimeField(auto_now=True)  

     # Occasion Fields
    occasionsbirthday = models.BooleanField(default=False)
    occasionsweddinganniversary = models.BooleanField(default=False)
    occasionsworkanniversary = models.BooleanField(default=False)
    occasionsadhoc = models.BooleanField(default=False)
    occasionsdiwaligift = models.BooleanField(default=False)
    occasionspoojagifts = models.BooleanField(default=False)
    occasionscompanyanniversary = models.BooleanField(default=False)
    
    celebrateEmployeeBirthday = models.BooleanField(default=False)
    celebrateEmpWeddingAnniversary = models.BooleanField(default=False)
    celebrateEmpWorkAnniversary = models.BooleanField(default=False)
    celebrateSpouseBirthday = models.BooleanField(default=False)
    celebrateSpouseWeddingAnniversary = models.BooleanField(default=False)
    celebrateSpouseWorkAnniversary = models.BooleanField(default=False)
    celebrateKid1Birthday = models.BooleanField(default=False)
    celebrateKid2Birthday = models.BooleanField(default=False)
    celebrateKid3Birthday = models.BooleanField(default=False)   

    uniform = models.BooleanField(default=False) 
    varied = models.BooleanField(default=False)
    employeeLevels = models.CharField(max_length=255, blank=True, null=True)   

    def __str__(self):
        return self.company_name


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    company_id = models.CharField(max_length=255, null=True, blank=True)
    employee_name = models.CharField(max_length=100)
    employee_dept = models.CharField(max_length=100)
    employee_email = models.EmailField(max_length=100)
    employee_phone = models.CharField(max_length=20)
    whatsapp_phone_number = models.CharField(max_length=20, null=True, blank=True)  # New field
    employee_dob = models.DateField()
    employee_doj = models.DateField()
    anniversary_date = models.DateField(null=True, blank=True)  # New field
    address = models.TextField(null=True, blank=True)  
    address2 = models.TextField(null=True, blank=True)  
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)  # New field
    pincode = models.CharField(max_length=10, null=True, blank=True)  # New field
    country = models.CharField(max_length=100, null=True, blank=True)  # New field
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
    marital_status = models.CharField(max_length=8, choices=MARITAL_STATUS_CHOICES)
    file_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_name

class Spouse(models.Model):
    spouse_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    spouse_name = models.CharField(max_length=100, null=True, blank=True)
    spouse_dob = models.DateField(null=True, blank=True)
    spouse_email = models.EmailField(max_length=100, null=True, blank=True)
    spouse_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.spouse_name if self.spouse_name else "Unnamed Spouse"

class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100, null=True, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    child_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    child_dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.child_name if self.child_name else "Unnamed Child"


class Vendor(models.Model):
    vendor_type = models.CharField(max_length=255)
    name_of_vendor = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    town_village = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    gps_location_link = models.URLField(blank=True, null=True)
    manager_name = models.CharField(max_length=255)
    manager_phone = models.CharField(max_length=20)
    manager_email = models.EmailField(max_length=255, unique=True)
    store_general_contact = models.CharField(max_length=20, blank=True, null=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True, null=True)
    headoffice_address = models.CharField(max_length=255, null=True, blank=True)
    headoffice_phone = models.CharField(max_length=20, null=True, blank=True)
    headoffice_email = models.EmailField(max_length=255, null=True, blank=True)
    headoffice_contact_person = models.CharField(max_length=255, null=True, blank=True)
    headoffice_contact_designation = models.CharField(max_length=255, null=True, blank=True)
    headoffice_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    headoffice_contact_person_email = models.EmailField(max_length=255, unique=True)
    bank_name = models.CharField(max_length=255)
    bank_account_no = models.CharField(max_length=50)
    bank_ifsc = models.CharField(max_length=20)
    bank_branch = models.CharField(max_length=255)
    bank_address = models.CharField(max_length=255)
    bank_account_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def _str_(self):
        return self.name_of_vendor

class TemplateImage(models.Model):
    img_Id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)    
    path = models.CharField(max_length=1024)  
    company_id = models.IntegerField()      

    def __str__(self):
        return self.name 

class CompanyTemplateConfig(models.Model):
    config_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    company_id = models.IntegerField()  # Reference to the company (foreign key in actual cases)
    template_img_id = models.IntegerField()
    logo_name = models.CharField(max_length=255,blank=True,null=True)  # Name of the logo
    logo_path = models.CharField(max_length=255,blank=True,null=True)  # Path to the logo (stored in S3 or file system)
    logo_size = models.CharField(max_length=50,blank=True,null=True)  # Size of the logo (e.g., '100x100')
    logo_x = models.FloatField(blank=True,null=True)  # X coordinate for logo placement
    logo_y = models.FloatField(blank=True,null=True)  # Y coordinate for logo placement
    content = models.TextField()  # Content to be displayed in the template
    content_x = models.FloatField()  # X coordinate for content placement
    content_y = models.FloatField()  # Y coordinate for content placement
    employname_x = models.FloatField()  # X coordinate for employee name placement
    employname_y = models.FloatField()  # Y coordinate for employee name placement
    text_colourcode = models.CharField(max_length=7)  # Colour code for text (e.g., '#FFFFFF')
    text_size = models.IntegerField()  # Size of the text
    text_font = models.CharField(max_length=100)  # Font type for the text
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Config {self.config_id} for Company {self.company_id}"


class OpsView(models.Model):
    ops_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    occasion = models.CharField(max_length=100)
    event_date = models.DateField()
    
    employee_id = models.IntegerField()
    name_of_person = models.CharField(max_length=255)
    relation = models.CharField(max_length=100,blank=True, null=True)
    address1 = models.CharField(max_length=255,blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    zipcode = models.CharField(max_length=20,blank=True, null=True)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subscription = models.CharField(max_length=50,blank=True, null=True)
    image_status = models.CharField(max_length=50,blank=True, null=True)
    email_status = models.CharField(max_length=50,blank=True, null=True)
    whatsapp_status = models.CharField(max_length=50,blank=True, null=True)
    
    cake_order_date = models.DateField(blank=True, null=True)
    cake_delivery_date = models.DateField(blank=True, null=True)
    cake_status = models.CharField(max_length=50, blank=True, null=True)
    cake_otp = models.CharField(max_length=10, blank=True, null=True)
    
    gift_order_date = models.DateField(blank=True, null=True)
    gift_delivery_date = models.DateField(blank=True, null=True)
    gift_status = models.CharField(max_length=50, blank=True, null=True)
    gift_otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.occasion} on {self.event_date}"


class EmailWhatsAppTable(models.Model):
    order_id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=100)
    company_id = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    email_image_link = models.URLField(max_length=500,blank=True, null=True)
    whatsapp_image_link = models.URLField(max_length=500,blank=True, null=True)
    subscription_details = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    image_generation_timestamp = models.DateTimeField(auto_now_add=True)
    mail_schedule_time = models.DateTimeField(blank=True, null=True)
    whatsapp_schedule_time = models.DateTimeField()
    mail_sent_time = models.DateTimeField(null=True, blank=True)
    whatsapp_sent_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Schedule for {self.employee_id} - Order {self.order_id}"
class CakeAndGift(models.Model):
    order_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField()
    company_id = models.IntegerField()
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=15)
    delivery_address1 = models.CharField(max_length=255)
    delivery_address2 = models.CharField(max_length=255, blank=True, null=True)
    delivery_city = models.CharField(max_length=100)
    delivery_zip = models.CharField(max_length=10)

    # Cake Delivery Information
    cake_scheduled_delivery_date = models.DateField()
    cake_scheduled_order_date = models.DateField()
    cake_vendor_id = models.IntegerField()
    cake_shop_name = models.CharField(max_length=100)

    cake_from_address = models.CharField(max_length=255)
    cake_from_city = models.CharField(max_length=100)
    cake_from_state = models.CharField(max_length=100)
    cake_from_pincode = models.CharField(max_length=10)
    cake_flavour = models.CharField(max_length=50)
    cake_weight = models.DecimalField(max_digits=5, decimal_places=2)  # assuming weight in kg
    cake_wish_message = models.TextField(blank=True, null=True)
    cake_delivery_person_name = models.CharField(max_length=100)
    cake_delivery_person_number = models.CharField(max_length=15)
    cake_delivery_verification_link = models.URLField(blank=True, null=True)
    cake_otp = models.CharField(max_length=6)

    # Gift Delivery Information
    gift_scheduled_delivery_date = models.DateField()
    gift_scheduled_order_date = models.DateField()
    gift_vendor_id = models.IntegerField()
    gift_shop_name = models.CharField(max_length=100)

    gift_from_address = models.CharField(max_length=255)
    gift_from_city = models.CharField(max_length=100)
    gift_from_state = models.CharField(max_length=100)
    gift_from_pincode = models.CharField(max_length=10)
    gift_article_number = models.CharField(max_length=50)
    gift_weight = models.DecimalField(max_digits=5, decimal_places=2)  # assuming weight in kg
    gift_delivery_person_name = models.CharField(max_length=100)
    gift_delivery_person_number = models.CharField(max_length=15)
    gift_delivery_verification_link = models.URLField(blank=True, null=True)
    gift_otp = models.CharField(max_length=6)

    def __str__(self):
        return f"Delivery for Employee ID: {self.employee_id} (Company ID: {self.company_id})"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    variant = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pkg = models.DecimalField(max_digits=10, decimal_places=2)
    delivery = models.DecimalField(max_digits=10, decimal_places=2)
    special_packaging = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.label} - {self.variant}"

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    company_id = models.IntegerField()
    company_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    occasion = models.CharField(max_length=100)
    emp_level = models.CharField(max_length=50)  # Employee level, e.g., Junior, Senior
    family = models.CharField(max_length=50)  # Indicates if family members are included
    email = models.BooleanField(default=False)  # Indicates if email is sent
    whatsapp = models.BooleanField(default=False)  # Indicates if WhatsApp message is sent
    gift = models.CharField(max_length=100, blank=True, null=True)  # Standard gift description
    custom_gift = models.CharField(max_length=100, blank=True, null=True)  # Custom gift description
    gift_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    custom_gift_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    email_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    whatsapp_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)  # Key name


    def __str__(self):
        return f"Subscription {self.subscription_id} for Company {self.company_id}"

class EmailConfig(models.Model):
    email_config_id = models.AutoField(primary_key=True)
    email_host_user = models.EmailField()
    email_host_password = models.CharField(max_length=255)
    company_id = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email_host_user} ({'Active' if self.active else 'Inactive'})"