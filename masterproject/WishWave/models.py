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
    address = models.TextField(null=True, blank=True)  # New field
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