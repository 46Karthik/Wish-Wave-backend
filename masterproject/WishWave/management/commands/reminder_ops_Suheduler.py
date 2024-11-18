import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Employees, CompanyTemplateConfig, TemplateImage,OpsView,Company,Subscription
from WishWave.serializers import OpsViewSerializer,EmailWhatsAppTableSerializer
from masterproject.views import upload_image_to_s3_Scheduler

class Command(BaseCommand):
    help = 'Generates scheduler based data in Ops table'
    def insetdata_in_opsTable(self):
          # Get today's date and the date for tomorrow
        today = timezone.now().date()
        terget_date = today + timedelta(days=7)
        print(terget_date)

        # Employee Brithday 
        employees = Employees.objects.filter(employee_dob__day=terget_date.day, employee_dob__month=terget_date.month)
        for employee in employees:
            if employee.company_id is not None:
                    def get_initials(input_list):
                            result = ""
                            if "BdayEmail" in input_list:
                                result += "E"
                            if "WhatsApp" in input_list:
                                result += "W"
                            if "Cake" in input_list:
                                result += "C"
                            if "Gift" in input_list:
                                result += "G"    
                            return result
                    def format_date(date):
                            return date.strftime('%Y-%m-%d') if date else None
                    subscriptionCodeVaue = ""
                    if OpsView.objects.filter(employee_id =employee.employee_id).exists():
                        print("Employee already exists")
                    else:
                        # get company details
                        company = Company.objects.get(company_id=employee.company_id)
                        subscriptions = Subscription.objects.filter(company_id=employee.company_id)
                        if subscriptions.exists():
                            subscription_codes = [subscription.subscription_type for subscription in subscriptions]
                            subscription_type_initials = get_initials(subscription_codes)
                            subscriptionCodeVaue = subscription_type_initials
                        else:
                            print("No subscriptions found for this company.")

                        
                        
                        create_ops_table_object = {
                            "company_id": employee.company_id,
                            "company_name": company.company_name,
                            "occasion": "Birthday",
                            "event_date": format_date(terget_date),
                            "employee_id": employee.employee_id,
                            "name_of_person": employee.employee_name,
                            "relation": "Employee",
                            "address1": employee.address,
                            "address2": employee.address2, 
                            "city": employee.city,
                            "zipcode": employee.pincode,
                            "email_id": employee.employee_email,
                            "phone_number": employee.whatsapp_phone_number,
                            "subscription": subscriptionCodeVaue,
                            "image_status": "False",
                            "email_status": "False",
                            "whatsapp_status": "False",
                            "cake_status": "False",
                            "gift_status": "False",
                            "cake_order_date": None,
                            "cake_delivery_date": None,
                            "cake_otp": "",
                            "gift_order_date": None,
                            "gift_delivery_date": None,
                            "gift_otp": ""
                        }
                        # print(create_ops_table_object)
                        
                        create_EmailWhatsAppTable ={
                            "employee_id": employee.employee_id,
                            "company_id": employee.company_id,
                            "email_id": employee.employee_email,
                            "phone_number": employee.whatsapp_phone_number,
                            "email_image_link": "",
                            "whatsapp_image_link": "",
                            "subscription_details": subscriptionCodeVaue,
                            "event_date": format_date(terget_date),
                            "image_generation_timestamp": None,
                            "mail_schedule_time": format_date(terget_date),
                            "whatsapp_schedule_time": format_date(terget_date),
                            "mail_sent_time": None,
                            "whatsapp_sent_time": None
                        }
                        create_cake_and_gift = {
                            "employee_id":  employee.employee_id,
                            "company_id":  employee.company_id,
                            "email_id":  employee.email_id,
                            "phone_number":  employee.phone_number,
                            "delivery_address1": employee.address,
                            "delivery_address2": employee.address2,
                            "delivery_city": employee.city,
                            "delivery_zip": employee.pincode,

                            "cake_scheduled_delivery_date": "2024-11-07",
                            "cake_scheduled_order_date": "2024-10-30",
                            "cake_vendor_id": 2001,
                            "cake_shop_name": "Sweet Treats Bakery",
                            "cake_from_address": "456 Cake St",
                            "cake_from_city": "Brooklyn",
                            "cake_from_state": "NY",
                            "cake_from_pincode": "11201",
                            "cake_flavour": "Chocolate",
                            "cake_weight": 1.5,
                            "cake_wish_message": "Happy Birthday, John!",
                            "cake_delivery_person_name": "Alice Johnson",
                            "cake_delivery_person_number": "0987654321",
                            "cake_delivery_verification_link": "https://example.com/verify/cake/123456",
                            "cake_otp": "123456",

                            "gift_scheduled_delivery_date": "2024-11-07",
                            "gift_scheduled_order_date": "2024-10-30",
                            "gift_vendor_id": 3001,
                            "gift_shop_name": "Gift Emporium",
                            "gift_from_address": "789 Gift Ave",
                            "gift_from_city": "Queens",
                            "gift_from_state": "NY",
                            "gift_from_pincode": "11385",
                            "gift_article_number": "GFT-00123",
                            "gift_weight": 2.0,
                            "gift_delivery_person_name": "Bob Smith",
                            "gift_delivery_person_number": "1122334455",
                            "gift_delivery_verification_link": "https://example.com/verify/gift/654321",
                            "gift_otp": "654321"
                        }
                        Opsserializer = OpsViewSerializer(data=create_ops_table_object)
                        EmailWhatsappSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
                        if Opsserializer.is_valid():
                            if EmailWhatsappSerializer.is_valid():
                               print("success")
                            #    Opsserializer.save()
                            #    EmailWhatsappSerializer.save()
                            else:
                                print(EmailWhatsappSerializer.errors)          
                        else:
                            # print('Error')
                            print(Opsserializer.errors)            
    def handle(self, *args, **options):
        self.insetdata_in_opsTable()

