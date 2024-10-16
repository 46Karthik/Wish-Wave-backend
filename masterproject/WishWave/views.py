from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .models import Company, UserProfile,Employees,Spouse,Child
from .serializers import CompanySerializer, UserProfileSerializer,EmployeeSerializer,SpouseSerializer,ChildSerializer
from django.core.mail import send_mail
from masterproject.views import generate_numeric_otp,return_response,return_sql_results,Decode_JWt
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import base64
from io import BytesIO
import pandas as pd


#         # permission_classes = [IsAuthenticated]
#         # permission_classes = [AllowAny]

class RegisterCompany(APIView):    
    def get(self, request):
        company_list = Company.objects.all()
        serializer = CompanySerializer(company_list, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
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
            company_list = Company.objects.all().get(company_name=companyname)
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
class send_mail_otp(APIView):
 def post(self, request):
        email = request.data.get('email') 
        if not email:
            return Response(return_response(1, 'Email is required'), status=status.HTTP_200_OK)
        new_otp = generate_numeric_otp()
        print("new_otp",new_otp)
        if not UserProfile.objects.filter(email_id=email).exists():
            return Response(return_response(1, 'User mail Id not found'), status=status.HTTP_200_OK)

        user_profile = UserProfile.objects.get(email_id=email)

        user_profile.otp = new_otp   
        user_profile.otp_generated_time = timezone.now()   
        user_profile.is_verified = False   
        user_profile.save()
        
        subject = "Your OTP Code"
        message = f'Your OTP code is {new_otp}. It will expire in 2 minutes.'
        from_email = 'karthikfoul66@gamil.com' 
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response(return_response(2, 'OTP sent successfully!'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        # # Generate JWT token
        refresh = RefreshToken.for_user(user_profile.user)
        refresh['email'] = user_profile.user.email
        refresh['role_id'] = user_profile.role_id
        refresh['company_id'] = user_profile.company_id

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
    permission_classes = [IsAuthenticated]
    def get(self, request, employee_id=None):
        try:
            payload = Decode_JWt(request.headers.get('Authorization'))
            employee = Employees.objects.get(pk=employee_id)
            if payload['company_id'] != employee.company_id:
                return Response(return_response(1, 'Unauthorized'), status=status.HTTP_401_UNAUTHORIZED)
            spouse = Spouse.objects.filter(employee=employee_id).first() 
            children = Child.objects.filter(employee=employee_id) 
            employee_data = EmployeeSerializer(employee).data
            employee_data['spouse'] = SpouseSerializer(spouse).data if spouse else None
            employee_data['children'] = ChildSerializer(children, many=True).data

            return Response(employee_data, status=status.HTTP_200_OK)
        except Employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']
        # request.data['company_id'] =2
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeBulkUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Expecting the Base64 data in the request body
        base64_data = request.data.get('file')
        payload = Decode_JWt(request.headers.get('Authorization'))
        request.data['company_id'] = payload['company_id']

        if not base64_data:
            return Response({"error": "No Base64 data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Split the Base64 data to get the actual Base64 string
        print(base64_data)
        try:
            header, encoded = base64_data.split(',')
            decoded = base64.b64decode(encoded)
        except Exception as e:
            return Response({"error": f"Error decoding Base64 data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Read the Excel file from the decoded data
        try:
            data_frame = pd.read_excel(BytesIO(decoded))
        except Exception as e:
            return Response({"error": f"Error reading Excel data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        employees_created = []

        for index, row in data_frame.iterrows():
            spouse_data = {
                'spouse_name': row.get('Spouse name'),
                'spouse_dob': row.get('Spouse DOB'),
                'spouse_email': row.get('Spouse Email'),
                'spouse_phone': row.get('Spouse Phone Number'),
            }

            children_data = []
            if pd.notna(row.get('Kid1 Name')):
                children_data.append({
                    'child_name': row.get('Kid1 Name'),
                    'child_gender': row.get('Kid 1 Gender'),
                    'child_dob': row.get('Kid1 DOB'),
                })
            if pd.notna(row.get('Kid 2 name')):
                children_data.append({
                    'child_name': row.get('Kid 2 name'),
                    'child_gender': row.get('Kid 2 Gender'),
                    'child_dob': row.get('Kid 2 DOB'),
                })
            if pd.notna(row.get('Kid 3 Name')):
                children_data.append({
                    'child_name': row.get('Kid 3 Name'),
                    'child_gender': row.get('Kid 3 Gender'),
                    'child_dob': row.get('Kid 3 DOB'),
                })

            employee_data = {
                'company_id': payload['company_id'],
                'employee_name': row.get('Name'),
                'employee_phone': row.get('Phone Number with country code'),
                'whatsapp_phone_number': row.get('Whatsapp Phone number'),
                'employee_doj': row.get('Date of Joining (DOJ)'),
                'employee_dob': row.get('Date of Birth (DOB)'),
                'employee_dept': row.get('Department'),
                'employee_email': row.get('Email'),
                'anniversary_date': row.get('Anniversary date'),
                'address': row.get('addrees'),
                'state': row.get('state'),
                'pincode': row.get('pincode'),
                'country': row.get('contry'),
                'gender': 'Male' if row.get('Kid 1 Gender') == 'Male' else 'Female',  # Adjust based on your requirements
                'marital_status': 'Married' if pd.notna(row.get('Spouse name')) else 'Single',  # Set based on spouse information
                'spouse': spouse_data,
                'children': children_data,
            }

            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                employee = serializer.save()
                employees_created.append(employee)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"{len(employees_created)} employees created successfully"}, status=status.HTTP_201_CREATED)

