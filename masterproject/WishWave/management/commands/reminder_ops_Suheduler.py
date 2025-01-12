import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Employees, CompanyTemplateConfig, TemplateImage,OpsView,Company,Subscription,Vendor,CakeAndGift,Spouse,Child,Schedule
from WishWave.serializers import OpsViewSerializer,EmailWhatsAppTableSerializer,CakeAndGiftSerializer,ScheduleSerializer
from masterproject.views import upload_image_to_s3_Scheduler
import json

class Command(BaseCommand):
    help = 'Generates scheduler based data in Ops table'

    def insetdata_in_opsTable(self, filters, title,type):
        """
        Inserts data into OpsTable based on dynamic filters and returns the operation status.

        :param filters: Dictionary of conditions to filter employees.
        :param title: Title of the operation (e.g., 'birthday', 'anniversary').
        :return: A dictionary summarizing the operation status.
        """
        if type == "Employee":
            # Status tracker for the current operation
            operation_status = {
                "title": title,
                "type": "Employee",
                "count_of_person": 0,
                "success": [],
                "status": [],
            }

            # Get today's date and calculate the target date
            today = timezone.now().date()
            target_date = today + timedelta(days=7)

            # Filter employees dynamically based on provided filters
            employees = Employees.objects.filter(**filters)
            operation_status["count_of_person"] = employees.count()
            print(employees.count(),"-------------")

            for employee in employees:
                employee_status = {
                    "empid": employee.employee_id,
                    "success": False,
                    "error": [],
                }

                if employee.company_id is not None:
                    def format_date(date):
                        return date.strftime('%Y-%m-%d') if date else None

                    subscription_code_result = ""

                    if OpsView.objects.filter(employee_id=employee.employee_id, occasion=title, relation='Employee',created_at__date=datetime.date.today()).exists():
                        employee_status["error"].append(f"Employee already exists in Ops table.employee id:{employee.employee_id}")
                    else:
                        try:
                            company = Company.objects.get(company_id=employee.company_id)
                            subscription = Subscription.objects.get(
                                company_id=employee.company_id,
                                occasion='birthday',
                                key_name=employee.employee_dept
                            )
                            if subscription.email:
                                subscription_code_result += "E"
                            if subscription.whatsapp:
                                subscription_code_result += "W"
                            if subscription.gift not in [None, ""]:
                                subscription_code_result += "G"
                            if subscription.custom_gift not in [None, ""]:
                                subscription_code_result += "C"
                        except Subscription.DoesNotExist:
                            employee_status["error"].append(f"No subscription found for the given company-occasion. Company ID: {employee.company_id} Employee ID: ${employee.employee_id}")
                        except Subscription.MultipleObjectsReturned:
                            employee_status["error"].append(f"Multiple subscriptions found. Please check your data. Company ID: {employee.company_id}")

                        food_vendor_details = Vendor.objects.filter(pin=employee.pincode,vendor_type="FOOD").first()
                        gift_vendor_details = Vendor.objects.filter(pin=employee.pincode,vendor_type="GIFT").first()
                        if food_vendor_details is None:
                            employee_status["error"].append(f"Food Vendor not found for the provided pincode.Employee ID : {employee.employee_id} , Pincode : {employee.pincode}")
                        if gift_vendor_details is None:
                            employee_status["error"].append(f"Gift Vendor not found for the provided pincode.Employee ID :{employee.employee_id} ,Pincode : {employee.pincode} ")
                        # Construct the objects to be created
                        create_ops_table_object = {
                            "company_id": employee.company_id,
                            "company_name": company.company_name,
                            "occasion": title,
                            "event_date": format_date(target_date),
                            "employee_id": employee.employee_id,
                            "name_of_person": employee.employee_name,
                            "relation": "Employee",
                            "address1": employee.address,
                            "address2": employee.address2,
                            "city": employee.city,
                            "zipcode": employee.pincode,
                            "email_id": employee.employee_email,
                            "phone_number": employee.whatsapp_phone_number,
                            "subscription": subscription_code_result,
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

                        create_EmailWhatsAppTable = {
                            "employee_id": employee.employee_id,
                            "company_id": employee.company_id,
                            "occasion": title,
                            "email_id": employee.employee_email,
                            "phone_number": employee.whatsapp_phone_number,
                            "email_image_link": "",
                            "whatsapp_image_link": "",
                            "subscription_details": subscription_code_result,
                            "event_date": format_date(target_date),
                            "image_generation_timestamp": None,
                            "mail_schedule_time": format_date(target_date),
                            "whatsapp_schedule_time": format_date(target_date),
                            "mail_sent_time": None,
                            "whatsapp_sent_time": None
                        }
                        create_cake_and_gift = {
                                "employee_id": employee.employee_id,
                                "company_id": employee.company_id,
                                "email_id": employee.employee_email,
                                "occasion": title,
                                "phone_number": employee.whatsapp_phone_number,
                                "delivery_address1": employee.address,
                                "delivery_address2": employee.address2,
                                "delivery_city": employee.city,
                                "delivery_zip": employee.pincode,
                                "food_id": subscription.gift,
                                "cake_scheduled_delivery_date": None,
                                "cake_scheduled_order_date": None,
                                "cake_vendor_id": getattr(food_vendor_details, 'id', None),
                                "cake_shop_name": getattr(food_vendor_details, 'name_of_vendor', ""),
                                "cake_from_address": getattr(food_vendor_details, 'address_1', ""),
                                "cake_from_city": getattr(food_vendor_details, 'city', ""),
                                "cake_from_state": getattr(food_vendor_details, 'state', ""),
                                "cake_from_pincode": getattr(food_vendor_details, 'pin', ""),
                                "cake_flavour": "",
                                "cake_weight": None,
                                "cake_wish_message": f"Happy {title}, {employee.employee_name}!",
                                "cake_delivery_person_name": "",
                                "cake_delivery_person_number": "",
                                "cake_delivery_verification_link": "",
                                "cake_otp": "",
                                "gift_id": subscription.custom_gift,
                                "gift_scheduled_delivery_date": None,
                                "gift_scheduled_order_date": None,
                                "gift_vendor_id": getattr(gift_vendor_details, 'id', None),
                                "gift_shop_name": getattr(gift_vendor_details, 'name_of_vendor', ""),
                                "gift_from_address": getattr(gift_vendor_details, 'address_1', ""),
                                "gift_from_city": getattr(gift_vendor_details, 'city', ""),
                                "gift_from_state": getattr(gift_vendor_details, 'state', ""),
                                "gift_from_pincode": getattr(gift_vendor_details, 'pin', ""),
                                "gift_article_number": "",
                                "gift_weight": None,
                                "gift_delivery_person_name": "",
                                "gift_delivery_person_number": "",
                                "gift_delivery_verification_link": "",
                                "gift_otp": ""
                            }
                        print("create_ops_table_object",create_ops_table_object)

                        Opsserializer = OpsViewSerializer(data=create_ops_table_object)
                        EmailWhatsAppSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
                        CakeAndGift_Serializer = CakeAndGiftSerializer(data=create_cake_and_gift)

                        if Opsserializer.is_valid() and EmailWhatsAppSerializer.is_valid() and CakeAndGift_Serializer.is_valid():
                            Opsserializer.save()
                            EmailWhatsAppSerializer.save()
                            CakeAndGift_Serializer.save()
                            employee_status["success"] = True
                            operation_status["success"].append(employee.employee_id)
                        else:
                            employee_status["error"].append(f'Validation failed for one or more Opsserializer.- {Opsserializer.errors},')
                            employee_status["error"].append(f'Validation failed for one or more EmailWhatsAppSerializer.- {EmailWhatsAppSerializer.errors},')
                            employee_status["error"].append(f'Validation failed for one or more CakeAndGiftSerializer.- {CakeAndGift_Serializer.errors},')
                operation_status["status"].append(employee_status)

            return operation_status

        elif type == "spouse":
            operation_status = {
                "title": title,
                "type": "spouse",
                "count_of_person": 0,
                "success": [],
                "status": [],
            }
            # Get today's date and calculate the target date
            today = timezone.now().date()
            target_date = today + timedelta(days=7)

            # Filter employees dynamically based on provided filters
            spouses = Spouse.objects.filter(**filters)
            operation_status["count_of_person"] = spouses.count()
            
            
            for spouse in spouses:
                spouse_status = {
                    "spouseid": spouse.spouse_id,
                    "success": False,
                    "error": [],
                }
                if spouse.employee.employee_id is not None:
                    def format_date(date):
                        return date.strftime('%Y-%m-%d') if date else None
                    
                    try:
                        employee = Employees.objects.get(employee_id=spouse.employee.employee_id)
                        company = Company.objects.get(company_id=employee.company_id)
                        subscription_code_result = ""
                        if OpsView.objects.filter(employee_id=employee.employee_id, occasion=title, relation='Spouse',created_at__date=datetime.date.today()).exists():
                            spouse_status["error"].append(f"Spouse already exists in Ops table for Employee ID: {employee.employee_id}.")
                        else:
                            try:
                                subscription = Subscription.objects.get(
                                    company_id=employee.company_id,
                                    occasion='birthday',
                                    emp_level='Family',
                                    family='Spouse'
                                )
                                if subscription.email:
                                    subscription_code_result += "E"
                                if subscription.whatsapp:
                                    subscription_code_result += "W"
                            except Subscription.DoesNotExist:
                                spouse_status["error"].append(f"No subscription found for the given company-occasion and spouse  ID: {spouse.spouse_id}.")
                            except Subscription.MultipleObjectsReturned:
                                spouse_status["error"].append(f"Multiple subscriptions found for company ID: {employee.company_id}, spouse ID: {spouse.spouse_id}. Please check your data.")

                            except Exception as e:
                                spouse_status["error"].append(f"Error processing subscription for spouse ID:{spouse.spouse_id}: {str(e)}")
                            # Construct objects for creation
                            create_ops_table_object = {
                                "company_id": employee.company_id,
                                "company_name": company.company_name,
                                "occasion": title,
                                "event_date": format_date(target_date),
                                "employee_id": employee.employee_id,
                                "name_of_person": spouse.spouse_name,
                                "relation": "spouse",
                                "address1": employee.address,
                                "address2": employee.address2,
                                "city": employee.city,
                                "zipcode": employee.pincode,
                                "email_id": spouse.spouse_email,
                                "phone_number": spouse.spouse_phone,
                                "subscription": subscription_code_result,
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

                            create_EmailWhatsAppTable = {
                                "employee_id": employee.employee_id,
                                "company_id": employee.company_id,
                                "occasion": title,
                                "email_id": spouse.spouse_email,
                                "phone_number": spouse.spouse_phone,
                                "email_image_link": "",
                                "whatsapp_image_link": "",
                                "subscription_details": subscription_code_result,
                                "event_date": format_date(target_date),
                                "image_generation_timestamp": None,
                                "mail_schedule_time": format_date(target_date),
                                "whatsapp_schedule_time": format_date(target_date),
                                "mail_sent_time": None,
                                "whatsapp_sent_time": None
                            }

                            Opsserializer = OpsViewSerializer(data=create_ops_table_object)
                            EmailWhatsAppSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
                            if Opsserializer.is_valid() and EmailWhatsAppSerializer.is_valid():
                                Opsserializer.save()
                                EmailWhatsAppSerializer.save()
                                spouse_status["success"] = True
                                operation_status["success"].append(employee.employee_id)
                            else:
                                spouse_status["error"].append(f'Validation failed for one or more Opsserializer.- {Opsserializer.errors},')
                                spouse_status["error"].append(f'Validation failed for one or more EmailWhatsAppSerializer.- {EmailWhatsAppSerializer.errors},')
                    except Employees.DoesNotExist:
                        spouse_status["error"].append(f"Employee ID: {spouse.employee_id} does not exist.")
                    except Company.DoesNotExist:
                        spouse_status["error"].append(f"Company for employee ID: {spouse.employee_id} does not exist.")
                    except Exception as e:
                        spouse_status["error"].append(f"Unexpected error: {str(e)}")
                operation_status["status"].append(spouse_status)
            return operation_status

        # KID Operations
        elif type == "kid":
            operation_status = {
                "title": title,
                "type": "kid",
                "count_of_person": 0,
                "success": [],
                "status": [],
            }
            # Get today's date and calculate the target date
            today = timezone.now().date()
            target_date = today + timedelta(days=7)

            # Filter employees dynamically based on provided filters
            Childrens = Child.objects.filter(**filters)
            operation_status["count_of_person"] = Childrens.count()
            
            
            for child in Childrens:
                kid_status = {
                    "kid_id": child.child_id,
                    "success": False,
                    "error": [],
                }
                if child.employee.employee_id is not None:
                    def format_date(date):
                        return date.strftime('%Y-%m-%d') if date else None
                    
                    try:
                        employee = Employees.objects.get(employee_id=child.employee.employee_id)
                        company = Company.objects.get(company_id=employee.company_id)
                        subscription_code_result = ""
                        if OpsView.objects.filter(employee_id=employee.employee_id, occasion=title, relation='Kid',created_at__date=datetime.date.today()).exists():
                            kid_status["error"].append(f"Kid already exists in Ops table for employee ID :{employee.employee_id}, Kid ID :{child.child_id}.")
                        else:
                            try:
                                subscription = Subscription.objects.get(
                                    company_id=employee.company_id,
                                    occasion='birthday',
                                    emp_level='Family',
                                    family = 'Kid 1' or 'Kid 2' or 'Kid 3'
                                )
                                if subscription.email:
                                    subscription_code_result += "E"
                                if subscription.whatsapp:
                                    subscription_code_result += "W"
                            except Subscription.DoesNotExist:
                                kid_status["error"].append(f"No subscription found for the given company-occasion and Kid {child.child_id}.")
                            except Subscription.MultipleObjectsReturned:
                                kid_status["error"].append(f"Multiple subscriptions found for company ID : {employee.company_id}, Kid ID : {child.child_id}. Please check your data.")

                            except Exception as e:
                                kid_status["error"].append(f"Error processing subscription forcompany ID : {employee.company_id}, Kid {child.child_id}: {str(e)}")
                            # Construct objects for creation
                            create_ops_table_object = {
                                "company_id": employee.company_id,
                                "company_name": company.company_name,
                                "occasion": title,
                                "event_date": format_date(target_date),
                                "employee_id": employee.employee_id,
                                "name_of_person": child.child_name,
                                "relation":  'kid',
                                "address1": employee.address,
                                "address2": employee.address2,
                                "city": employee.city,
                                "zipcode": employee.pincode,
                                "email_id": employee.employee_email,
                                "phone_number": employee.whatsapp_phone_number,
                                "subscription": subscription_code_result,
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

                            create_EmailWhatsAppTable = {
                                "employee_id": employee.employee_id,
                                "company_id": employee.company_id,
                                "occasion": title,
                                "email_id": employee.employee_email,
                                "phone_number": employee.whatsapp_phone_number,
                                "email_image_link": "",
                                "whatsapp_image_link": "",
                                "subscription_details": subscription_code_result,
                                "event_date": format_date(target_date),
                                "image_generation_timestamp": None,
                                "mail_schedule_time": format_date(target_date),
                                "whatsapp_schedule_time": format_date(target_date),
                                "mail_sent_time": None,
                                "whatsapp_sent_time": None
                            }

                            Opsserializer = OpsViewSerializer(data=create_ops_table_object)
                            EmailWhatsAppSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
                            if Opsserializer.is_valid() and EmailWhatsAppSerializer.is_valid():
                                Opsserializer.save()
                                EmailWhatsAppSerializer.save()
                                kid_status["success"] = True
                                operation_status["success"].append(employee.employee_id)
                            else:
                                kid_status["error"].append(f'Validation failed for one or more Opsserializer.- {Opsserializer.errors},')
                                kid_status["error"].append(f'Validation failed for one or more EmailWhatsAppSerializer.- {EmailWhatsAppSerializer.errors},')
                    except Employees.DoesNotExist:
                        kid_status["error"].append(f"Kid ID: {child.child_id} does not exist.")
                    except Company.DoesNotExist:
                        kid_status["error"].append(f"Company for employee ID : {employee.employee_id},Kid ID : {child.child_id} does not exist.")
                    except Exception as e:
                        kid_status["error"].append(f"Unexpected error: {str(e)}")
                operation_status["status"].append(kid_status)
            return operation_status

            # Status tracker for the current operation

    def handle(self, *args, **options):
        # Define filters and titles
        Employeeoperations = [
            {
                "filters": {
                    'employee_dob__day': (timezone.now() + timedelta(days=7)).day,
                    'employee_dob__month': (timezone.now() + timedelta(days=7)).month
                },
                "title": "birthday"
            },
            {
                "filters": {
                    'anniversary_date__day': (timezone.now() + timedelta(days=7)).day,
                    'anniversary_date__month': (timezone.now() + timedelta(days=7)).month
                },
                "title": "weddinganniversary"
            },
            {
                "filters": {
                    'employee_doj__day': (timezone.now() + timedelta(days=7)).day,
                    'employee_doj__month': (timezone.now() + timedelta(days=7)).month
                },
                "title": "workanniversary"
            },
        ]
        spouseoperations = [
            {
                "filters": {
                    'spouse_dob__day': (timezone.now() + timedelta(days=7)).day,
                    'spouse_dob__month': (timezone.now() + timedelta(days=7)).month
                },
                "title": "birthday"
            }]
        kidoperations = [
            {
                "filters": {
                    'child_dob__day': (timezone.now() + timedelta(days=7)).day,
                    'child_dob__month': (timezone.now() + timedelta(days=7)).month
                },
                "title": "birthday"
            }]


        # Execute operations and collect results
        status = []
        for operation in Employeeoperations:
            result = self.insetdata_in_opsTable(operation["filters"], operation["title"],"Employee")
            status.append(result)
        for operation in spouseoperations:
            result = self.insetdata_in_opsTable(operation["filters"], operation["title"],"spouse")
            status.append(result)
        for operation in kidoperations:
            result = self.insetdata_in_opsTable(operation["filters"], operation["title"],"kid")
            status.append(result)

        # add Schedules details in database
        schedule_details = {
            "schedule_name": "7-Days-Schedule",
            "details": json.dumps(status)
        }
    #    Create a new record
        Schedule.objects.create(
            schedule_name=schedule_details["schedule_name"],
            details=schedule_details["details"]
        )
        print(status)


