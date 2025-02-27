from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.core.mail import send_mail
from masterproject.views import generate_numeric_otp,return_response,return_sql_results,Decode_JWt,upload_image_to_s3,upload_base64_image_to_s3,delete_image_from_s3
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import base64
from io import BytesIO
import pandas as pd
from datetime import datetime, timedelta
import xlsxwriter
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from PIL import Image, ImageDraw, ImageFont
import requests
import os







#         # permission_classes = [IsAuthenticated]
#         # permission_classes = [AllowAny]

class RegisterCompany(APIView):   
    permission_classes = [IsAuthenticated] 
    # comany table get by id
    def get(self, request, id=None):
        payload = Decode_JWt(request.headers.get('Authorization'))
        if payload['role_id'] == '4':
            if id is not None:
                all_company = Company.objects.get(company_id=id)
                serializer = CompanySerializer(all_company)
                return Response(return_response(2, 'Company found', serializer.data), status=status.HTTP_200_OK)
            else:
                all_company = Company.objects.all()
                serializer = CompanySerializer(all_company, many=True)
                return Response(return_response(2, 'Company found', serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(return_response(1, 'Unauthorized'), status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        # company table
        if Company.objects.filter(company_name=request.data.get('company_name')).exists():
            return Response(return_response(1, 'This company name is already registered.'), status=status.HTTP_200_OK)
        if Company.objects.filter(company_GSTR_no=request.data.get('company_GSTR_no')).exists():
            return Response(return_response(1, 'This GST registration number is already registered.'), status=status.HTTP_200_OK)
        if Company.objects.filter(contact_email=request.data.get('contact_email')).exists():
            return Response(return_response(1, 'This email is already registered.'), status=status.HTTP_200_OK)
        if User.objects.filter(email=request.data.get('contact_email')).exists():
            return Response(return_response(1, 'This email is already registered.'), status=status.HTTP_200_OK)
        if User.objects.filter(username=request.data.get('contact_name')).exists():
            return Response(return_response(1, 'This username is already registered.'), status=status.HTTP_200_OK)
        # user profile table 
        if UserProfile.objects.filter(email_id=request.data.get('contact_email')).exists():
            return Response(return_response(1, 'This email is already registered.'), status=status.HTTP_200_OK)
        if UserProfile.objects.filter(phone_no=request.data.get('contact_phone_no')).exists():
            return Response(return_response(1, 'This phone number is already registered.'), status=status.HTTP_200_OK)
        if UserProfile.objects.filter(username=request.data.get('contact_name')).exists():
            return Response(return_response(1, 'This username is already registered.'), status=status.HTTP_200_OK)
     
        serializer = CompanySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            companyname = request.data.get('company_name')
            company_list = Company.objects.get(company_name=companyname)
            serializer = CompanySerializer(company_list, many=False)
            resister_company_id = serializer.data.get('company_id')
            if resister_company_id:
                user_data = {
                    'username': request.data.get('contact_name'),
                    'email': request.data.get('contact_email'),
                    }
                try:
                    user = User.objects.create_user(**user_data) 
                    user_profile_data = {
                        'user': user, 
                        'company_id': resister_company_id,
                        'role_id': '1',
                        'username': request.data.get('contact_name'),
                        'password': '',
                        'active': True,
                        'email_id': request.data.get('contact_email'),
                        'phone_no': request.data.get('contact_phone_no'),
                        'is_verified': False,
                    }
                    user_profile = UserProfile.objects.create(**user_profile_data)
                    return Response(return_response(2, 'Company registered successfully!'), status=status.HTTP_200_OK)

                except IntegrityError as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        if payload['role_id'] == '4':
            #  update company details as company table
            if Company.objects.filter(company_id=request.data.get('company_id')).exists():
                company = Company.objects.get(company_id=request.data.get('company_id'))
                serializer = CompanySerializer(company, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(return_response(2, 'Company updated successfully'), status=status.HTTP_200_OK)
                else:
                    return Response(return_response(1, 'Company not updated', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(return_response(1, 'Company not found'), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(return_response(1, 'Unauthorized'), status=status.HTTP_401_UNAUTHORIZED)
class send_mail_otp(APIView):
    def post(self, request):
        email = request.data.get('email') 
        if not email:
            return Response(return_response(1, 'Email is required'), status=status.HTTP_200_OK)

        new_otp = generate_numeric_otp()
        print("new_otp", new_otp)

        if not UserProfile.objects.filter(email_id=email).exists():
            return Response(return_response(1, 'User mail Id not found'), status=status.HTTP_200_OK)

        if Company.objects.filter(contact_email=email, active=False).exists():
            return Response(return_response(1, 'Company not Active, please contact admin'), status=status.HTTP_200_OK)

        user_profile = UserProfile.objects.get(email_id=email)
        user_profile.otp = new_otp   
        user_profile.otp_generated_time = timezone.now()   
        user_profile.is_verified = False   
        user_profile.save()
        
        subject = "Your OTP Code"
        from_email = 'karthikfoul66@gmail.com' 
        recipient_list = [email]

        # HTML email template
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
            <div style="text-align: center; padding: 10px; background-color: #1474fc; color: white; border-radius: 8px 8px 0 0;">
                <h2>Your OTP Code</h2>
            </div>
            <div style="padding: 20px; text-align: center;">
                <p>Hello,</p>
                <p>Your One-Time Password (OTP) for account verification is:</p>
                <p style="font-size: 24px; font-weight: bold; color: #1474fc; background-color: #f0f8ff; padding: 10px; border-radius: 4px; display: inline-block;">{new_otp}</p>
                <p>This OTP is valid for <strong>2 minutes</strong>. Please do not share this code with anyone.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <p>Thank you for using our service!</p>
            </div>
            <div style="text-align: center; padding: 10px; background-color: #f1f1f1; border-radius: 0 0 8px 8px; color: #666;">
                &copy; 2024 WishWave. All rights reserved.
            </div>
        </div>
        """
        plain_text_message = strip_tags(html_content)

        # Send email
        try:
            email_message = EmailMultiAlternatives(subject, plain_text_message, from_email, recipient_list)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return Response(return_response(2, 'OTP sent successfully!'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#  def post(self, request):
#         email = request.data.get('email') 
#         if not email:
#             return Response(return_response(1, 'Email is required'), status=status.HTTP_200_OK)
#         new_otp = generate_numeric_otp()
#         print("new_otp",new_otp)
#         if not UserProfile.objects.filter(email_id=email).exists():
#             return Response(return_response(1, 'User mail Id not found'), status=status.HTTP_200_OK)
#         if Company.objects.filter(contact_email=email,active=False).exists():
#             return Response(return_response(1, 'Company not Active please contact admin'), status=status.HTTP_200_OK)
        
#         user_profile = UserProfile.objects.get(email_id=email)
        
#         user_profile.otp = new_otp   
#         user_profile.otp_generated_time = timezone.now()   
#         user_profile.is_verified = False   
#         user_profile.save()
        
#         subject = "Your OTP Code"
#         message = f'Your OTP code is {new_otp}. It will expire in 2 minutes.'
#         from_email = 'karthikfoul66@gamil.com' 
#         recipient_list = [email]

#         try:
#             send_mail(subject, message, from_email, recipient_list)
#             return Response(return_response(2, 'OTP sent successfully!'), status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': 'Failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class verify_otp(APIView):
 def post(self, request):
        email = request.data.get('email')  
        request_otp = request.data.get('otp') 
        if not email:
            return Response(return_response(1, 'Email is required'), status=status.HTTP_200_OK)
        if not request_otp:
            return Response(return_response(1, 'OTP is required'), status=status.HTTP_200_OK)
        user_profile = UserProfile.objects.get(email_id=email)

        if user_profile.otp != request_otp:
            return Response(return_response(1, 'Invalid OTP'), status=status.HTTP_200_OK)
        if user_profile.otp_generated_time < timezone.now() - timedelta(minutes=2):
            return Response(return_response(1, 'OTP has expired'), status=status.HTTP_200_OK)

        user_profile.is_verified = True
        user_profile.save()
        
        company_details = Company.objects.filter(company_id=user_profile.company_id).first()
        serializer = CompanySerializer(company_details)        
        # # Generate JWT token
        refresh = RefreshToken.for_user(user_profile.user)
        refresh['email'] = user_profile.user.email
        refresh['role_id'] = user_profile.role_id
        refresh['company_id'] = user_profile.company_id
        refresh['company_name'] = serializer.data.get('company_name')
        refresh['login_id'] = user_profile.id
        refresh['username'] = user_profile.username

        return Response(return_response(2, 'Login successful', {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }), status=status.HTTP_200_OK)

class get_company_code(APIView):
 def get(self, request):
        last_company = Company.objects.order_by('company_id').last()
        if not last_company:
            return Response(return_response(2, 'No company found', 1), status=status.HTTP_200_OK)
        return Response(return_response(2, 'Company found', last_company.company_id + 1), status=status.HTTP_200_OK)

class EmployeeCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            payload = Decode_JWt(request.headers.get('Authorization'))
            if id is None:
                employee_list = Employees.objects.filter(company_id=payload['company_id'])
                serializer = EmployeeSerializer(employee_list, many=True)
                return Response(return_response(2,"Employee found",serializer.data), status=status.HTTP_200_OK)
            employee = Employees.objects.get(pk=id)
            if payload['company_id'] != employee.company_id:
                return Response(return_response(1, 'Unauthorized'), status=status.HTTP_401_UNAUTHORIZED)
            spouse = Spouse.objects.filter(employee=id).first() 
            children = Child.objects.filter(employee=id) 
            employee_data = EmployeeSerializer(employee).data
            employee_data['spouse'] = SpouseSerializer(spouse).data if spouse else None
            employee_data['children'] = ChildSerializer(children, many=True).data

            return Response(return_response(2,"Emplyess Data Founded",employee_data), status=status.HTTP_200_OK)
        except Employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']
        # request.data['company_id'] =2
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            if Employees.objects.filter(employee_email=request.data.get('employee_email')).exists():
                return Response(return_response(1, 'This  employee email is already registered.'), status=status.HTTP_200_OK)
            serializer.save()
            return Response(return_response(2,"Employee Created Successfully",serializer.data), status=status.HTTP_201_CREATED)
        return Response(return_response(1,serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,id):
        # Expecting the Base64 data in the request body
        if not id:
            return Response(return_response(1, 'Employee id is required'), status=status.HTTP_200_OK)
        try:
            # ipdb.set_trace()
            payload = Decode_JWt(request.headers.get('Authorization'))
            request.data['company_id'] = payload['company_id']
            request.data['employee_id'] = id
            employee=Employees.objects.get(employee_id=request.data.get('employee_id'))
            serializer = EmployeeSerializer(employee, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(return_response(2,"Employee Updated Successfully",serializer.data), status=status.HTTP_201_CREATED)
            return Response(return_response(1,serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

def convert_date_format(date_value):
    """
    Convert a date value (Excel date format) to 'YYYY-MM-DD'.
    If the input is NaT or invalid, return None.
    """
    try:
        # Convert to pandas datetime, then to the desired string format
        return pd.to_datetime(date_value).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None

class EmployeeBulkUploadView(APIView):
    def post(self, request):
        # Extract Base64 data and company_id from the JWT
        base64_data = request.data.get('file')
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']

        if not base64_data:
            return Response({"error": "No Base64 data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Decode Base64 file
        try:
            header, encoded = base64_data.split(',')
            decoded = base64.b64decode(encoded)
        except Exception as e:
            return Response({"error": f"Error decoding Base64 data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Read Excel file with proper engine handling
        try:
            # Default to .xlsx (openpyxl)
            data_frame = pd.read_excel(BytesIO(decoded), engine='openpyxl')
        except ValueError as e:
            return Response({"error": f"Error reading Excel data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ImportError as e:
            return Response({
                "error": "Missing dependency. Install 'openpyxl' for .xlsx or 'xlrd==2.0.1' for .xls support."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unexpected error reading Excel data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        employees_created = []
        errors = []
        company = Company.objects.get(company_id=payload['company_id'])
        saved_employees_count = 0
        # Process each row in the data frame
        for index, row in data_frame.iterrows():
            employee_email = row.get('Email')
            employee_level = row.get('EmployeeLevel')

            # Check for existing email in the database
            if Employees.objects.filter(employee_email=employee_email).exists():
                errors.append({
                    "Row": index + 1,
                    "Error": f"Employee with email {employee_email} already exists."
                })
                continue

            # Validate employee level based on the company
            employee_levels_list = [level.strip() for level in company.employeeLevels.split(",")]
            if company.varied and employee_level not in employee_levels_list:
                errors.append({
                    "Row": index + 1,
                    "Error": f"Employee level {employee_level} is not allowed for this company."
                })
                continue

            # Prepare spouse data conditionally
            spouse_data = None
            if pd.notna(row.get('Spouse frist name')):
                spouse_data = {
                    'spouse_name': row.get('Spouse frist name') + " " + row.get('Spouse last name'),
                    'spouse_dob': convert_date_format(row.get('Spouse DOB')),
                    'spouse_email': row.get('Spouse Email'),
                    'spouse_phone': row.get('Spouse Phone Number'),
                }

            # Prepare children data conditionally
            children_data = []
            for i in range(1, 4):  # Handles Kid1, Kid2, Kid3
                if pd.notna(row.get(f'Kid{i} Name')):
                    children_data.append({
                        'child_name': row.get(f'Kid{i} Name'),
                        'child_gender': row.get(f'Kid {i} Gender'),
                        'child_dob': convert_date_format(row.get(f'Kid{i} DOB')),
                    })
            employee_dob = convert_date_format(row.get('Date of Birth (DOB)'))
            # print(employee_dob, 'Manager Email')
            # Prepare employee data
            employee_data = {
                'company_id': payload['company_id'],
                'employee_name': f"{row.get('Employee First Name')} {row.get('Employee last Name')}",
                'employee_code': row.get('Employee Code'),
                'manager_name': row.get('Manager Name') if pd.notna(row.get('Manager Name')) else None,
                'manager_email': row.get('Manager Email') if pd.notna(row.get('Manager Email')) else None,
                'employee_dept': row.get('EmployeeLevel'),
                'employee_phone': row.get('Phone Number with country code'),
                'whatsapp_phone_number': row.get('Whatsapp Phone number'),
                'employee_doj': convert_date_format(row.get('Date of Joining (DOJ)')),
                'employee_dob':convert_date_format(row.get('Date of Birth (DOB)')),
                'employee_email': employee_email,
                'anniversary_date': convert_date_format (row.get('Anniversary date')),
                'address': row.get('addrees'),
                'state': row.get('state'),
                'pincode': row.get('pincode'),
                'country': row.get('contry'),
                'gender': row.get('Gender'),
                'marital_status': row.get('Marital'),
                'address2': row.get('addrees 2'),
                'city': row.get('city'),
            }

            print (employee_data.get('employee_name'), 'employee_data')
            # Conditionally include spouse and children data
            if spouse_data:
                employee_data['spouse'] = spouse_data
            if children_data:
                employee_data['children'] = children_data
            
            # Serialize and save data
            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                employees_created.append(employee_data)
            else:
                errors.append({
                    "Row": index + 1,
                    "Error": serializer.errors
                })

        if errors:
                error_df = pd.DataFrame(errors)
                error_buffer = BytesIO()
                with pd.ExcelWriter(error_buffer, engine='xlsxwriter') as writer:
                    error_df.to_excel(writer, index=False, sheet_name='Errors')

                error_base64 = base64.b64encode(error_buffer.getvalue()).decode('utf-8')
                return Response({
                    "message": f"{saved_employees_count} employees created successfully.",
                    "error_file": f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{error_base64}"
                }, status=status.HTTP_201_CREATED)
        else:
            for employee in employees_created:
                # save all employees
                serializer = EmployeeSerializer(data=employee)
                if serializer.is_valid():
                    saved_employees_count += 1
                    employee = serializer.save()
            
            return Response({
                "message": f"{saved_employees_count} employees created successfully."
            }, status=status.HTTP_201_CREATED)

class SubscriptionEmployeedata(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
      # Get the employee IDs for the specified company
        employee_ids = Employees.objects.filter(company_id=payload['company_id']).values_list('employee_id', flat=True)

        # Count the spouses associated with these employees
        spouse_count = Spouse.objects.filter(employee_id__in=employee_ids).count()

        # Count the children associated with these employees
        child_count = Child.objects.filter(employee_id__in=employee_ids).count()

        # Get the employee count
        employee_count = employee_ids.count()
        
        # user name as subscription table last updated by
        user_id = Subscription.objects.filter(company_id=payload['company_id'])
        username = UserProfile.objects.get(id=user_id.last().user_id).username
        # Prepare the data dictionary
        listdata = {
            'employee_count': employee_count,
            'spouse_count': spouse_count,
            'child_count': child_count,
            'username': username,
            'last_updated_by': user_id.last().user_id,
        }
    
        return Response(return_response(2, 'List of employee count', listdata), status=status.HTTP_200_OK)
class VendorView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    def post(self, request):
        vendor_data = request.data
        if Vendor.objects.filter(name_of_vendor=request.data.get('name_of_vendor')).exists():
            return Response(return_response(1, 'This vendor name is already registered.'), status=status.HTTP_200_OK)
        if Vendor.objects.filter(email=request.data.get('email')).exists():
            return Response(return_response(1, 'This vendor email is already registered.'), status=status.HTTP_200_OK)
        if Vendor.objects.filter(gst_number=request.data.get('gst_number')).exists():
            return Response(return_response(1, 'This gst number is already registered.'), status=status.HTTP_200_OK)
        if Vendor.objects.filter(headoffice_contact_phone=request.data.get('headoffice_contact_phone')).exists():
            return Response(return_response(1, 'This headoffice contact phone is already registered.'), status=status.HTTP_200_OK)
        if Vendor.objects.filter(headoffice_contact_person_email=request.data.get('headoffice_contact_person_email')).exists():
            return Response(return_response(1, 'This headoffice contact person email is already registered.'), status=status.HTTP_200_OK)
        if Vendor.objects.filter(bank_account_no=request.data.get('bank_account_no')).exists():
            return Response(return_response(1, 'This  bank account number is already registered.'), status=status.HTTP_200_OK)
        serializer = VendorSerializer(data=vendor_data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(return_response(2,"Vendor created successfully"), status=status.HTTP_201_CREATED)
        else:
            return Response(return_response(1, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id is not None:
            all_vendors = Vendor.objects.get(id=id)
            serializer = VendorSerializer(all_vendors)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            all_vendors = Vendor.objects.all()
            serializer = VendorSerializer(all_vendors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Edit Vendor (PUT)
    def put(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
        except Vendor.DoesNotExist:
            return Response(return_response(1, "Vendor not found"), status=status.HTTP_404_NOT_FOUND)

        # Update the vendor details
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, "Vendor updated successfully"), status=status.HTTP_200_OK)
        else:
            return Response(return_response(1, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    # Delete Vendor (DELETE)
    def delete(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
        except Vendor.DoesNotExist:
            return Response(return_response(1, "Vendor not found"), status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response(return_response(2, "Vendor deleted successfully"), status=status.HTTP_200_OK)

class S3ImageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        file = request.FILES.get('file')
        if not file:
            return Response(return_response(1, 'No file provided'), status=status.HTTP_400_BAD_REQUEST)
        file_path = upload_image_to_s3(file, 'template',file.content_type)
        if file_path == "error":
            return Response(return_response(1, 'Invalid AWS credentials'), status=status.HTTP_400_BAD_REQUEST)
        else:
            file_TemplateImage_data = {
                'name': file.name,
                'path': file_path,
                'company_id': payload['company_id'],
            }
            serializer = TemplateImageSerializer(data=file_TemplateImage_data)
            if serializer.is_valid():
                template_image = serializer.save()
                template_image.save()
                file_url = f"https://wishwave.s3.amazonaws.com/{file_path}"
                return Response(return_response(2, 'Template image uploaded successfully', file_url), status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        all_template_image = TemplateImage.objects.filter(company_id=payload['company_id'])
        serializer = TemplateImageSerializer(all_template_image, many=True)
        return Response(return_response(2, 'Template image found', serializer.data), status=status.HTTP_200_OK)

class CompanyTemplateConfigView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        all_template_image = CompanyTemplateConfig.objects.filter(company_id=payload['company_id'])
        serializer = CompanyTemplateConfigSerializer(all_template_image, many=True)
        return Response(return_response(2, 'Template image found', serializer.data), status=status.HTTP_200_OK)
        
    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']
        if request.data['new_logo_upload']  == True:
            file =request.data['new_logo_base64']
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            file_path = upload_base64_image_to_s3(file, 'company', request.data['logo_name'], 'image/png')
            if file_path == "error":
                return Response(return_response(1, 'Invalid AWS credentials'), status=status.HTTP_400_BAD_REQUEST)
            request.data['logo_path'] = file_path
            serializer = CompanyTemplateConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(return_response(2, 'Template Config created successfully'), status=status.HTTP_201_CREATED)
            else:
                return Response(return_response(1, 'Template Config not created',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CompanyTemplateConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(return_response(2, 'Template Config created successfully'), status=status.HTTP_201_CREATED)
            else:
                return Response(return_response(1, 'Template Config not created',serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        company_id = payload.get('company_id')
        request.data['company_id'] = company_id
        try:
            # Get all active configurations for the company
            company_templates = CompanyTemplateConfig.objects.filter(company_id=company_id, active=True)
            if not company_templates.exists():
                return Response({"error": "Company template not found"}, status=status.HTTP_404_NOT_FOUND)
        except CompanyTemplateConfig.DoesNotExist:
            return Response({"error": "Company template not found"}, status=status.HTTP_404_NOT_FOUND)

        # Upload logo if needed
        if 'new_logo_upload' in request.data and request.data['new_logo_upload'] is True:
            file = request.data.get('new_logo_base64')
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            delete_image = delete_image_from_s3(request.data.get('logo_path'))
            if not delete_image:
                return Response({"error": "Logo file not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                file_path = upload_base64_image_to_s3(file, 'company', request.data.get('logo_name'), 'image/png')
                if file_path == "error":
                    return Response(return_response(1, 'Invalid AWS credentials'), status=status.HTTP_400_BAD_REQUEST)

                request.data['logo_path'] = file_path

        # Check if the new request data matches any active template configuration
        existing_template = None
        company_templates = CompanyTemplateConfig.objects.filter(company_id=company_id)
        for template in company_templates:
            if (request.data['template_img_id'] == template.template_img_id and
                request.data['content'] == template.content):
                existing_template = template
                break
        for template in company_templates:
                template.active = False
                template.save()
        request.data['active'] = True
        # If a matching template is found, update it
        if existing_template:
            serializer = CompanyTemplateConfigSerializer(existing_template, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()
                return Response(return_response(2, 'Template Config updated successfully'), status=status.HTTP_200_OK)
            else:
                return Response(return_response(1, 'Template Config not updated', serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        # If no matching template is found, create a new one and deactivate old templates
        else:
            serializer = CompanyTemplateConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(return_response(2, 'Template Config created successfully'), status=status.HTTP_201_CREATED)
            else:
                return Response(return_response(1, 'Template Config not created', serializer.errors), status=status.HTTP_400_BAD_REQUEST)      

           

class OpsTableView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        all_ops_table = OpsView.objects.all()
        serializer = OpsViewSerializer(all_ops_table, many=True)
        return Response(return_response(2, 'Ops Table found', serializer.data), status=status.HTTP_200_OK)
    def post(self, request):
        # Extract filter values from the request
        company_name = request.data.get('company_name')
        occasion = request.data.get('occasion')
        relation = request.data.get('relation')
        event_date = request.data.get('event_date')
        filter_date_from_To = request.data.get('filter_date_from_To')

        # Build filter criteria dynamically
        filter_criteria = {}
        if company_name:
            filter_criteria['company_name'] = company_name
        if occasion:
            filter_criteria['occasion'] = occasion
        if relation:
            filter_criteria['relation'] = relation
        if event_date:
            filter_criteria['event_date'] = event_date

        # Handle `filter_date_from_To`
        if filter_date_from_To:
            today = datetime.now().date()
            if filter_date_from_To == 'today':
                filter_criteria['event_date'] = today
            elif filter_date_from_To == 'tomorrow':
                filter_criteria['event_date'] = today + timedelta(days=1)
            elif filter_date_from_To == '3days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=3))
            elif filter_date_from_To == '5days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=5))
            elif filter_date_from_To == '7days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=7))

        # Filter based on the criteria
        filter_ops_table = OpsView.objects.filter(**filter_criteria)

        # Serialize and return the filtered data
        serializer = OpsViewSerializer(filter_ops_table, many=True)
        return Response(return_response(2, 'Ops Table found', serializer.data), status=status.HTTP_200_OK)

class generate_ops_excel(APIView):
    def post(self, request):
        # Extract filter values from the request
        company_name = request.data.get('company_name')
        occasion = request.data.get('occasion')
        relation = request.data.get('relation')
        event_date = request.data.get('event_date')
        filter_date_from_to = request.data.get('filter_date_from_To')

        # Build filter criteria dynamically
        filter_criteria = self.build_filter_criteria(
            company_name=company_name,
            occasion=occasion,
            relation=relation,
            event_date=event_date,
            filter_date_from_to=filter_date_from_to
        )

        # Filter OpsView data
        filter_ops_table = OpsView.objects.filter(**filter_criteria)

        # Serialize OpsView data
        serializer = OpsViewSerializer(filter_ops_table, many=True)
        ops_data = serializer.data

        if not ops_data:
            return Response({'status': 1, 'message': 'No data found', 'data': []}, status=status.HTTP_200_OK)

        # Fetch related CakeAndGift and Product data
        ops_with_cake_gift = []
        for ops_item in ops_data:
            # Fetch CakeAndGift data for each Ops entry
            food_and_gift = CakeAndGift.objects.filter(
                employee_id=ops_item['employee_id'], occasion=ops_item['occasion']
            )
            gift_serializer = CakeAndGiftSerializer(food_and_gift, many=True)
            cake_and_gift_data = gift_serializer.data

            # Initialize lists to store product names
            food_names = []
            gift_names = []

            for gift in cake_and_gift_data:
                # Fetch and append food product names
                food_ids = gift.get('food_id', '')
                if food_ids:
                    print (food_ids.split(','),'------------')
                    food_products = Product.objects.filter(product_id__in=food_ids.split(','))
                    food_names.extend([product.label for product in food_products])

                # Fetch and append gift product names
                gift_ids = gift.get('gift_id', '')
                if gift_ids:
                    gift_products = Product.objects.filter(product_id__in=gift_ids.split(','))
                    gift_names.extend([product.label for product in gift_products])

            # Add food and gift names to the Ops data
            ops_item['food_product_name1'] = food_names[0] if len(food_names) > 0 else None
            ops_item['food_product_name2'] = food_names[1] if len(food_names) > 1 else None
            ops_item['gift_product_name1'] = gift_names[0] if len(gift_names) > 0 else None
            ops_item['gift_product_name2'] = gift_names[1] if len(gift_names) > 1 else None
            ops_item['cake_and_gift_data'] = cake_and_gift_data
            ops_with_cake_gift.append(ops_item)

        # Create Excel file and convert it to Base64
        excel_base64 = self.create_excel_base64(ops_with_cake_gift)

        # Return the Excel file as a Base64 string in the response
        return Response(
            {'status': 2, 'message': 'Ops Table Excel generated', 'data': {'excel_base64': excel_base64}},
            status=status.HTTP_200_OK
        )

    def build_filter_criteria(self, company_name=None, occasion=None, relation=None, event_date=None, filter_date_from_to=None):
        filter_criteria = {}

        if company_name:
            filter_criteria['company_name'] = company_name
        if occasion:
            filter_criteria['occasion'] = occasion
        if relation:
            filter_criteria['relation'] = relation
        if event_date:
            filter_criteria['event_date'] = event_date

        if filter_date_from_to:
            today = datetime.now().date()
            if filter_date_from_to == 'today':
                filter_criteria['event_date'] = today
            elif filter_date_from_to == 'tomorrow':
                filter_criteria['event_date'] = today + timedelta(days=1)
            elif filter_date_from_to == '3days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=3))
            elif filter_date_from_to == '5days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=5))
            elif filter_date_from_to == '7days':
                filter_criteria['event_date__range'] = (today, today + timedelta(days=7))

        return filter_criteria

    def create_excel_base64(self, data):
        # Flatten the data: Merge CakeAndGift data into the main OpsView data
        merged_data = []
        for item in data:
            # Flatten the Ops data and CakeAndGift data into a single record
            ops_item = {key: item[key] for key in item if key != 'cake_and_gift_data'}
            cake_and_gift_info = item.get('cake_and_gift_data', [])
            for gift in cake_and_gift_info:
                # For each gift, create a new record with both Ops and CakeAndGift details
                new_item = ops_item.copy()
                new_item.update(gift)  # Merge the CakeAndGift details into the Ops item
                merged_data.append(new_item)

        # Convert to a DataFrame
        df = pd.DataFrame(merged_data)

        # Specify required columns
        columns_to_keep = [
            'company_name', 'name_of_person', 'event_date', 'occasion', 'relation', 
            'address1', 'address2', 'city', 'zipcode', 'email_id', 'phone_number', 
            'subscription', 'email_status', 'image_status', 'whatsapp_status', 
            'cake_status', 'gift_status', 'cake_order_date', 'cake_delivery_date', 
            'cake_otp', 'gift_order_date', 'gift_delivery_date', 'gift_otp',
            'cake_shop_name', 'cake_from_address', 'cake_from_city', 'cake_from_state', 
            'cake_from_pincode', 'cake_wish_message', 'gift_shop_name', 'gift_from_address',
            'gift_from_city', 'gift_from_state', 'gift_from_pincode', 'gift_delivery_person_name', 
            'gift_delivery_person_number', 'gift_delivery_verification_link', 
            'gift_scheduled_delivery_date', 'gift_scheduled_order_date', 
            'food_product_name1', 'food_product_name2', 'gift_product_name1', 'gift_product_name2'
        ]

        # Ensure the columns exist in the DataFrame
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]

        # Rename columns to user-friendly names
        custom_column_names = {
            'company_name': 'Company Name', 'name_of_person': 'Name of Person', 
            'event_date': 'Event Date', 'occasion': 'Occasion', 'relation': 'Relation', 
            'address1': 'Address 1', 'address2': 'Address 2', 'city': 'City', 
            'zipcode': 'Zip Code', 'email_id': 'Email ID', 'phone_number': 'Phone Number', 
            'subscription': 'Subscription', 'email_status': 'Email Status', 
            'image_status': 'Image Status', 'whatsapp_status': 'WhatsApp Status', 
            'cake_status': 'Cake Status', 'gift_status': 'Gift Status', 
            'cake_order_date': 'Cake Order Date', 'cake_delivery_date': 'Cake Delivery Date', 
            'cake_otp': 'Cake OTP', 'gift_order_date': 'Gift Order Date', 
            'gift_delivery_date': 'Gift Delivery Date', 'gift_otp': 'Gift OTP',
            'food_product_name1': 'Food Product Name 1', 'food_product_name2': 'Food Product Name 2',
            'gift_product_name1': 'Gift Product Name 1', 'gift_product_name2': 'Gift Product Name 2'
        }

        df.rename(columns=custom_column_names, inplace=True)

        # Convert the DataFrame to an Excel file in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Ops Table')

        # Encode the Excel file as Base64
        buffer.seek(0)
        excel_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        return excel_base64



class SubscriptionTableView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        all_subscription_table = Subscription.objects.filter(company_id=payload.get('company_id'))
        serializer = SubscriptionSerializer(all_subscription_table, many=True)
        return Response(return_response(2, 'Subscription Table found', serializer.data), status=status.HTTP_200_OK)
        
    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        company_id = payload.get('company_id')
        errors = []

        # Retrieve the company name once based on company_id
        try:
            company = Company.objects.get(company_id=company_id)
            company_name = company.company_name  # Assuming 'company_name' is the field name
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        for item in request.data:
            item['company_id'] = company_id
            item['company_name'] = company_name  # Add company name to each item
            item['user_id'] = payload.get('login_id')
            serializer = SubscriptionSerializer(data=item)
            
            if serializer.is_valid():
                serializer.save()  
            else:
                errors.append({"data": item, "errors": serializer.errors})

        if errors:
            return Response(return_response(1, 'Some subscriptions were not created', errors), status=status.HTTP_400_BAD_REQUEST)

        return Response(return_response(2, 'All subscriptions created successfully'), status=status.HTTP_201_CREATED)
    def put(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        company_id = payload.get('company_id')
        errors = []

        # Retrieve the company name once based on company_id
        try:
            company = Company.objects.get(company_id=company_id)
            company_name = company.company_name  # Assuming 'company_name' is the field name
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        for item in request.data:
            item['company_id'] = company_id
            item['company_name'] = company_name  # Add company name to each item
            item['user_id'] = payload.get('login_id')
            subscription_table = Subscription.objects.get(subscription_id= item.get('subscription_id'))
            serializer = SubscriptionSerializer(subscription_table, data=item, partial=True)
            
            if serializer.is_valid():
                serializer.save()  
            else:
                errors.append({"data": item, "errors": serializer.errors})
        if errors:
            return Response(return_response(1, 'Some subscriptions were not Updated', errors), status=status.HTTP_400_BAD_REQUEST)

        return Response(return_response(2, 'All subscriptions Updated successfully'), status=status.HTTP_201_CREATED)

class SubscriptionCompanydata(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        companydetails = Company.objects.get(company_id=payload.get('company_id'))
        serializer = CompanySerializer(companydetails)
        return Response(return_response(2, 'Company details found', serializer.data), status=status.HTTP_200_OK)
        
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        productlist = Product.objects.all()
        serializer = ProductSerializer(productlist, many=True)
        return Response(return_response(2, 'Product details found', serializer.data), status=status.HTTP_200_OK)
        
class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        schedule = Schedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(return_response(2, 'Schedule details found', serializer.data), status=status.HTTP_200_OK)


class EmailConfigView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        company = EmailConfig.objects.filter(company_id=payload['company_id'])
        print(company.count())
        if company.count() == 0:
            return Response(return_response(3, 'Eamail Defult value'), status=status.HTTP_200_OK)
        else:
            email_config = EmailConfig.objects.filter(company_id=payload['company_id'])
            serializer = EmailConfigSerializer(email_config, many=True)
            return Response(return_response(2, 'Email Config found', serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']
        serializer = EmailConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, 'Email Config created successfully'), status=status.HTTP_201_CREATED)
        else:
            return Response(return_response(1, 'Email Config not created', serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        company_id = payload.get('company_id')
        request.data['company_id'] = company_id
        emailconfig=EmailConfig.objects.get(email_config_id=request.data.get('email_config_id'))
        serializer = EmailConfigSerializer(emailconfig, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, 'Email Config updated successfully'), status=status.HTTP_201_CREATED)
        else:
            return Response(return_response(1, 'Email Config not updated', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        
class OpsEditVendorView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        id = request.data.get('employee_id')
        occasion = request.data.get('occasion')
        EmailWhatsAppTable_data = EmailWhatsAppTable.objects.filter(employee_id=id,occasion=occasion)
        email_whatsapp_table_serializer = EmailWhatsAppTableSerializer(EmailWhatsAppTable_data, many=True)
        food_and_gift = CakeAndGift.objects.filter(employee_id=id,occasion=occasion)
        serializer = CakeAndGiftSerializer(food_and_gift, many=True)
        return_data = {
            "email_whatsapp_table": email_whatsapp_table_serializer.data,
            "cake_and_gift": serializer.data
        }
        return Response(return_response(2, 'Cake and Gift found', return_data), status=status.HTTP_200_OK)

class CakeandGiftUpdateView(APIView):
    def patch(self, request):
        try:
            cake_and_gift = CakeAndGift.objects.get(order_id=request.data.get('cake_id'))
        except CakeAndGift.DoesNotExist:
            return Response(return_response(1, "CakeAndGift not found"), status=status.HTTP_404_NOT_FOUND)
        
        serializer = CakeAndGiftSerializer(cake_and_gift, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, "Updated successfully"), status=status.HTTP_200_OK)
        return Response(return_response(1, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class get_company_details(APIView):
    def post (self, request):
        id = request.data.get('id')
        if id is None:
            return Response(return_response(1, 'id is required'), status=status.HTTP_400_BAD_REQUEST)
        try:
            all_company = Company.objects.get(company_id=id)
            get_employee = Employees.objects.filter(company_id=id)
            all_employee = EmployeeSerializer(get_employee, many=True)
            serializer = CompanySerializer(all_company)
            
            responce  ={
                "company": serializer.data,
                "employee": all_employee.data
            }
            return Response(return_response(2, 'Company found', responce), status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response(return_response(1, 'Company not found'), status=status.HTTP_404_NOT_FOUND)

class RewardsMailAction(APIView):
    def post(self, request):
        get_key = request.data.get('key')
        reward_status = 'Submitted'  # Renamed to avoid conflict
        appored_key = '4a5c6e7d8f9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9'
        cancel_key = '9f8e7d6c5b4a3g2h1i0j9k8l7m6n5o4p3q2r1s0t9u8v7w6x5y4z3a2b1c0d9e8f7g6h5i4j3k2l1m0n9o8p7q6r5s4t3u2v1w0x9y8z7a6b5c4d'

        if get_key == appored_key:
            reward_status = 'Approved'
        elif get_key == cancel_key:
            reward_status = 'Cancelled'

        if Reward.objects.filter(reward_id=request.data.get('id')).exists():
            get_reward = Reward.objects.get(reward_id=request.data.get('id'))
            get_reward.status = reward_status
            serializer = RewardSerializer(get_reward, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(return_response(2, 'Successfully updated'), status=status.HTTP_201_CREATED)
        else:
            return Response(return_response(1, 'Reward not found'), status=status.HTTP_404_NOT_FOUND)
 # # HTML email template
    # html_content = """
    # <!DOCTYPE html>
    # <html>
    # <head>
    # <style>
    #     body {
    #         font-family: Arial, sans-serif;
    #         line-height: 1.6;
    #         margin: 0;
    #         padding: 0;
    #     }
    #     .email-container {
    #         max-width: 600px;
    #         margin: 20px auto;
    #         padding: 20px;
    #         border: 1px solid #ddd;
    #         border-radius: 8px;
    #         background-color: #f9f9f9;
    #     }
    #     h2 {
    #         color: #333;
    #     }
    #     p {
    #         color: #555;
    #     }
    #     .button-container {
    #         margin-top: 20px;
    #         text-align: center;
    #     }
    #     .button {
    #         display: inline-block;
    #         margin: 5px;
    #         padding: 10px 20px;
    #         font-size: 16px;
    #         color: white;
    #         text-decoration: none;
    #         border-radius: 4px;
    #         transition: background-color 0.3s ease;
    #     }
    #     .button-approve {
    #         background-color: #28a745;
    #     }
    #     .button-approve:hover {
    #         background-color: #218838;
    #     }
    #     .button-cancel {
    #         background-color: #dc3545;
    #     }
    #     .button-cancel:hover {
    #         background-color: #c82333;
    #     }
    # </style>
    # </head>
    # <body>
    #     <div class="email-container">
    #         <h2>Action Required</h2>
    #         <p>
    #             Hello, <br>
    #             Please review the details and select an action below.
    #         </p>
    #         <div class="button-container">
    #             <!-- Approve Button -->
    #             <a href="https://srv688176.hstgr.cloud/mail-action/{reward_id}/{appored_key}" class="button button-approve">Approve</a>
    #             <!-- Cancel Button -->
    #             <a href="https://srv688176.hstgr.cloud/mail-action/{reward_id}/{cancel_key}" class="button button-cancel">Cancel</a>
    #         </div>
    #         <p>
    #             If you have any questions, feel free to reply to this email.<br>
    #             Thank you!
    #         </p>
    #     </div>
    # </body>
    # </html>
    # """


def send_mail_action(mail_id, reward_id, data):
    subject = "Action Required"
    from_email = 'karthikfoul66@gmail.com'
    recipient_list = [mail_id]  # Use the passed mail_id as the recipient
    appored_key = '4a5c6e7d8f9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9'
    cancel_key = '9f8e7d6c5b4a3g2h1i0j9k8l7m6n5o4p3q2r1s0t9u8v7w6x5y4z3a2b1c0d9e8f7g6h5i4j3k2l1m0n9o8p7q6r5s4t3u2v1w0x9y8z7a6b5c4d'

    # Fetch company data from the database
    company_data = Company.objects.get(company_id=data['company_id'])
    company_name = company_data.company_name

    # Extracting values from the data dictionary
    submitter_emp_code = data.get('submitter_emp_code')
    submitter_emp_name = data.get('submitter_emp_name')
    submitter_dept = data.get('submitter_dept')

    recipient_emp_code = data.get('recipient_emp_code')
    recipient_emp_name = data.get('recipient_emp_name')
    justification = data.get('justification')

    core_value = data.get('core_value')
    delivery = data.get('delivery')
    impact = data.get('impact')
    points = data.get('points')

    # HTML content for the email
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recognition Mail Template</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #dcdcdc;
                }}
                .mail-container {{
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    padding: 20px 30px;
                    max-width: 600px;
                    margin: 50px auto;
                    line-height: 1.6;
                    color: #333;
                }}
                .mail-container h2 {{
                    text-align: center;
                    color: #007bff;
                    margin-bottom: 10px;
                }}
                .mail-container p {{
                    margin-bottom: 20px;
                    font-size: 14px;
                    color: #555;
                }}
                .mail-container .highlight {{
                    font-weight: bold;
                    color: #000;
                }}
                .mail-container .section {{
                    margin-bottom: 15px;
                }}
                .mail-container .section label {{
                    display: block;
                    font-weight: bold;
                    margin-bottom: 5px;
                    font-size: 14px;
                }}
                .mail-container .section span {{
                    display: block;
                    font-size: 14px;
                    color: #555;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #888;
                }}
                .button-container {{
                    margin-top: 20px;
                    text-align: center;
                }}
                .button {{
                    display: inline-block;
                    margin: 5px;
                    padding: 10px 20px;
                    font-size: 16px;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    transition: background-color 0.3s ease;
                }}
                .button-approve {{
                    background-color: #28a745;
                }}
                .button-approve:hover {{
                    background-color: #218838;
                }}
                .button-cancel {{
                    background-color: #dc3545;
                }}
                .button-cancel:hover {{
                    background-color: #c82333;
                }}
            </style>
        </head>
        <body>
        <div class="mail-container">
            <h2>Welcome {company_name}!!!</h2>
            <p>Good job in your efforts to appreciate!</p>
            <div class="section">
                <label>Your Employee ID:</label>
                <span class="highlight">{submitter_emp_code} - {submitter_emp_name}</span>
            </div>
            <div class="section">
                <label>Like to Recognise:</label>
                <span class="highlight">{recipient_emp_code} - {recipient_emp_name}</span>
            </div>
            <div class="section">
                <label>Department:</label>
                <span>{submitter_dept}</span>
            </div>
            <div class="section">
                <label>For:</label>
                <span>{justification}</span>
            </div>
            <div class="section">
                <label>Award Category (Core Values):</label>
                <span>{core_value}</span>
            </div>
            <div class="section">
                <label>Delivering:</label>
                <span>{delivery}</span>
            </div>
            <div class="section">
                <label>Business Impact:</label>
                <span>{impact}</span>
            </div>
            <div class="section">
                <label>Points Rewarded:</label>
                <span class="highlight">{points} Points</span>
            </div>
            <div class="button-container">
                <!-- Approve Button -->
                <a href="https://srv688176.hstgr.cloud/mail-action/{reward_id}/{appored_key}" class="button button-approve">Approve</a>
                <!-- Cancel Button -->
                <a href="https://srv688176.hstgr.cloud/mail-action/{reward_id}/{cancel_key}" class="button button-cancel">Cancel</a>
            </div>
            <div class="footer">
                <p>Thank you for being an integral part of our success!</p>
            </div>
        </div>
        </body>
        </html>
        """

    # Generate plain text version
    plain_text_message = strip_tags(html_content)

    try:
        # Send email
        email_message = EmailMultiAlternatives(subject, plain_text_message, from_email, recipient_list)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle errors
        return Response(
            {"message": f"Error sending email: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class RewardsView(APIView):  
    def post(self, request):
        try:
            serializer = RewardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                get_reward_id = serializer.data.get('reward_id')
                if serializer.data.get('recipient_manager_email') is not None:
                    # send mail action
                    get_mail_id = serializer.data.get('recipient_manager_email')
                    print ('-----------serializer.data',serializer.data)
                    send_mail_action(get_mail_id,get_reward_id,serializer.data)
                return Response(return_response(2, 'Successfully created', serializer.data), status=status.HTTP_201_CREATED)
            else:
                return Response(return_response(1, 'Rewards not created', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Reward.DoesNotExist:
            return Response(return_response(1, 'Rewards not found'), status=status.HTTP_404_NOT_FOUND)
class RewardslistView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        payload = Decode_JWt(request.headers.get('Authorization'))
        try:
            all_reward = Reward.objects.filter(company_id=payload['company_id'])
            serializer = RewardSerializer(all_reward, many=True)
            return Response(return_response(2, 'Rewards found', serializer.data), status=status.HTTP_200_OK)
        except Reward.DoesNotExist:
            return Response(return_response(1, 'Rewards not found'), status=status.HTTP_404_NOT_FOUND)

class generate_image(APIView):
    def post(self, request):
        try:
            data = request.data
            image_url = data.get('image')
            text = data.get('text', '')
            text2 = data.get('text2', '')
            logo_url = data.get('logo')
            text_position = data.get('textPosition', {})
            text2_position = data.get('text2Position', {})
            logo_position = data.get('logoPosition', {})
            font_family = data.get('fontFamily', 'arial.ttf')  # Default font
            font_size = data.get('fontSize', 20)
            font_size2 = data.get('fontSize2', 20)
            font_color = data.get('fontColor', '#000000')

            # Define a cross-platform font path
            def get_font_path(font_name):
                if os.name == 'nt':  # Windows
                    # Try a few common fonts
                    possible_font_paths = [
                        os.path.join('C:', 'Windows', 'Fonts', 'arial.ttf'),
                        os.path.join('C:', 'Windows', 'Fonts', 'verdana.ttf')
                    ]
                    for font_path in possible_font_paths:
                        if os.path.isfile(font_path):
                            return font_path
                else:  # Linux
                    # On Linux, DejaVuSans is common and might be preinstalled
                    return '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

                return None

            # Check if the specified font exists
            font_path = get_font_path(font_family)
            if not font_path:
                return Response({'error': f'Font file not found for {font_family}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Download the base image
            response = requests.get(image_url)
            if response.status_code != 200:
                return Response({'error': 'Failed to fetch image from URL'}, status=status.HTTP_400_BAD_REQUEST)
            image_bytes = BytesIO(response.content)
            base_image = Image.open(image_bytes).convert('RGBA')  # Convert to RGBA

            # Create a drawing context
            draw = ImageDraw.Draw(base_image)

            # Load fonts with fallback logic for both systems
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                return Response({'error': f'Failed to load font from {font_path}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                font2 = ImageFont.truetype(font_path, font_size2)
            except IOError:
                return Response({'error': f'Failed to load second font from {font_path}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Draw the first text
            text_x = int((text_position.get('x', 0) / 100) * base_image.width)
            text_y = int((text_position.get('y', 0) / 100) * base_image.height)
            draw.multiline_text((text_x, text_y), text, font=font, fill=font_color, align='center')

            # Draw the second text
            text2_x = int((text2_position.get('x', 0) / 100) * base_image.width)
            text2_y = int((text2_position.get('y', 0) / 100) * base_image.height)
            draw.multiline_text((text2_x, text2_y), text2, font=font2, fill=font_color, align='center')

            # Draw the logo (same as before)
            if logo_url:
                logo_response = requests.get(logo_url)
                if logo_response.status_code != 200:
                    return Response({'error': 'Failed to fetch logo from URL'}, status=status.HTTP_400_BAD_REQUEST)
                logo_bytes = BytesIO(logo_response.content)
                logo_image = Image.open(logo_bytes).convert('RGBA')

                logo_width = int((logo_position.get('width', 10) / 100) * base_image.width)
                logo_height = int((logo_position.get('height', 10) / 100) * base_image.height)
                logo_x = int((logo_position.get('x', 0) / 100) * base_image.width)
                logo_y = int((logo_position.get('y', 0) / 100) * base_image.height)

                # Use LANCZOS instead of ANTIALIAS for better quality resampling
                logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                base_image.paste(logo_image, (logo_x, logo_y), logo_image)

            # Convert RGBA to RGB before saving as JPEG (JPEG doesn't support transparency)
            base_image = base_image.convert('RGB')

            # Convert the final image to base64
            output_buffer = BytesIO()
            base_image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)
            final_base64_image = base64.b64encode(output_buffer.read()).decode('utf-8')

            return Response({'base64Image': f'data:image/jpeg;base64,{final_base64_image}'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)