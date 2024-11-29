 # help = 'Generates scheduler based data in Ops table'
    # def insetdata_in_opsTable(self):
    #       # Get today's date and the date for tomorrow
    #     today = timezone.now().date()
    #     terget_date = today + timedelta(days=7)
    #     print(terget_date)

    #     # Employee Brithday 
    #     employees = Employees.objects.filter(employee_dob__day=terget_date.day, employee_dob__month=terget_date.month)
    #     for employee in employees:
    #         if employee.company_id is not None:
    #                 def format_date(date):
    #                         return date.strftime('%Y-%m-%d') if date else None
    #                 subscriptionCodeVaue = ""
    #                 if OpsView.objects.filter(employee_id =employee.employee_id,occasion ='birthday',relation ='Employee').exists():
    #                     print("Employee already exists")
    #                 else:
    #                     # get company details
    #                     company = Company.objects.get(company_id=employee.company_id)
    #                     subscriptions = Subscription.objects.filter(company_id=employee.company_id,occasion ='birthday',key_name = employee.employee_dept)
    #                     try:
    #                         subscription_Code_result = ""
    #                         company = Company.objects.get(company_id=employee.company_id)
    #                         subscription = Subscription.objects.get(company_id=employee.company_id, occasion='birthday',key_name = employee.employee_dept)
    #                         if subscription.email:
    #                             subscription_Code_result += "E"
    #                         if subscription.whatsapp:
    #                             subscription_Code_result += "W"
    #                         if subscription.gift not in [None, ""]:
    #                             subscription_Code_result += "G"
    #                         if subscription.custom_gift not in [None, ""]:
    #                             subscription_Code_result += "C"
    #                         print(subscription_Code_result)
    #                     except Subscription.DoesNotExist:
    #                         print("No subscription found for the given company and occasion.")
    #                     except Subscription.MultipleObjectsReturned:
    #                         print("Multiple subscriptions found. Please check your data.")

                        
                        
    #                     create_ops_table_object = {
    #                         "company_id": employee.company_id,
    #                         "company_name": company.company_name,
    #                         "occasion": "Birthday",
    #                         "event_date": format_date(terget_date),
    #                         "employee_id": employee.employee_id,
    #                         "name_of_person": employee.employee_name,
    #                         "relation": "Employee",
    #                         "address1": employee.address,
    #                         "address2": employee.address2, 
    #                         "city": employee.city,
    #                         "zipcode": employee.pincode,
    #                         "email_id": employee.employee_email,
    #                         "phone_number": employee.whatsapp_phone_number,
    #                         "subscription": subscription_Code_result,
    #                         "image_status": "False",
    #                         "email_status": "False",
    #                         "whatsapp_status": "False",
    #                         "cake_status": "False",
    #                         "gift_status": "False",
    #                         "cake_order_date": None,
    #                         "cake_delivery_date": None,
    #                         "cake_otp": "",
    #                         "gift_order_date": None,
    #                         "gift_delivery_date": None,
    #                         "gift_otp": ""
    #                     }
    #                     # print(create_ops_table_object)
                        
    #                     create_EmailWhatsAppTable ={
    #                         "employee_id": employee.employee_id,
    #                         "company_id": employee.company_id,
    #                         "email_id": employee.employee_email,
    #                         "phone_number": employee.whatsapp_phone_number,
    #                         "email_image_link": "",
    #                         "whatsapp_image_link": "",
    #                         "subscription_details": subscription_Code_result,
    #                         "event_date": format_date(terget_date),
    #                         "image_generation_timestamp": None,
    #                         "mail_schedule_time": format_date(terget_date),
    #                         "whatsapp_schedule_time": format_date(terget_date),
    #                         "mail_sent_time": None,
    #                         "whatsapp_sent_time": None
    #                     }

    #                     vendor_details = Vendor.objects.filter(pin=employee.pincode).first()
    #                     if  vendor_details is None:
    #                         print("vendor not found")
    #                     create_cake_and_gift = {
    #                         "employee_id":  employee.employee_id,
    #                         "company_id":  employee.company_id,
    #                         "email_id":  employee.employee_email,
    #                         "phone_number":  employee.whatsapp_phone_number,
    #                         "delivery_address1": employee.address,
    #                         "delivery_address2": employee.address2,
    #                         "delivery_city": employee.city,
    #                         "delivery_zip": employee.pincode,

    #                         "cake_scheduled_delivery_date": None,
    #                         "cake_scheduled_order_date": None,
    #                         "cake_vendor_id": vendor_details.id,
    #                         "cake_shop_name": vendor_details.name_of_vendor ,
    #                         "cake_from_address": vendor_details.address_1,
    #                         "cake_from_city": vendor_details.city,
    #                         "cake_from_state": vendor_details.state,
    #                         "cake_from_pincode": vendor_details.pin,
    #                         "cake_flavour": "",
    #                         "cake_weight": None,
    #                         "cake_wish_message": f"Happy Birthday, {employee.employee_name}!",
    #                         "cake_delivery_person_name": "",
    #                         "cake_delivery_person_number": "",
    #                         "cake_delivery_verification_link": "",
    #                         "cake_otp": "",

    #                         "gift_scheduled_delivery_date": None,
    #                         "gift_scheduled_order_date": None,
    #                         "gift_vendor_id": vendor_details.id,
    #                         "gift_shop_name": vendor_details.name_of_vendor,
    #                         "gift_from_address": vendor_details.address_1,
    #                         "gift_from_city": vendor_details.city,
    #                         "gift_from_state": vendor_details.state,
    #                         "gift_from_pincode": vendor_details.pin,
    #                         "gift_article_number": "",
    #                         "gift_weight": None,
    #                         "gift_delivery_person_name": "",
    #                         "gift_delivery_person_number": "",
    #                         "gift_delivery_verification_link": "",
    #                         "gift_otp": ""
    #                     }
    #                     Opsserializer = OpsViewSerializer(data=create_ops_table_object)
    #                     EmailWhatsappSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
    #                     CakeAndGift_Serializer = CakeAndGiftSerializer(data=create_cake_and_gift)
    #                     if Opsserializer.is_valid():
    #                         if EmailWhatsappSerializer.is_valid():
    #                             if CakeAndGift_Serializer.is_valid():
    #                                 Opsserializer.save()
    #                                 EmailWhatsappSerializer.save()
    #                                 CakeAndGift_Serializer.save()
    #                             else:
    #                                 print(CakeAndGift_Serializer.errors)
    #                         else:
    #                             print(EmailWhatsappSerializer.errors)          
    #                     else:
    #                         # print('Error')
    #                         print(Opsserializer.errors)            
    # def handle(self, *args, **options):
    #     self.insetdata_in_opsTable()




   # ------------------------------------- 2nd `if` block ------------------------------------

   # from django.core.management.base import BaseCommand
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO
# import requests
# from WishWave.models import Company, Employees, Spouse, Child, TemplateImage, CompanyTemplateConfig
# from django.utils import timezone
# from datetime import timedelta
# from masterproject.views import upload_image_to_s3_Scheduler

# class Command(BaseCommand):
#     help = 'Generates and saves an image with text and logo overlay'

#     # Other methods...
#     def create_image_with_overlay(self, image_url, text1, text2, logo_url, text1_coords, text2_coords, logo_coords, 
#                                 text1_size, text2_size, text1_color, text2_color, output_path, logo_size,employee_id):
#         # Fetch the main image from the URL
#         response = requests.get(image_url)
#         img = Image.open(BytesIO(response.content))

#         # Get image dimensions to scale text/logo placement accordingly
#         img_width, img_height = img.size

#         # Load the font and set font sizes dynamically for text1 and text2
#         try:
#             font1 = ImageFont.truetype("arial.ttf", text1_size)
#             font2 = ImageFont.truetype("arial.ttf", text2_size)
#         except IOError:
#             font1 = ImageFont.load_default()
#             font2 = ImageFont.load_default()

#         draw = ImageDraw.Draw(img)

#         # Convert percentage-based coordinates to actual pixel values
#         text1_x = int(img_width * (text1_coords[0] / 100))
#         text1_y = int(img_height * (text1_coords[1] / 100))
#         draw.text((text1_x, text1_y), text1, fill=text1_color, font=font1)

#         text2_x = int(img_width * (text2_coords[0]  / 100))
#         text2_y = int(img_height * (text2_coords[1] / 100))
#         draw.text((text2_x, text2_y), text2, fill=text2_color, font=font2)

#         # Fetch the logo image from the URL
#         response_logo = requests.get(logo_url)
#         logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")

#         logo_width = (logo_size / 100) * img_width
#         aspect_ratio = logo.width / logo.height
#         logo_height = int(logo_width / aspect_ratio)
#         logo = logo.resize((int(logo_width), int(logo_height)), Image.Resampling.LANCZOS)

#         logo_x = int((logo_coords[0] / 100) * img_width)
#         logo_y = int((logo_coords[1] / 100) * img_height)
#         img.paste(logo, (logo_x, logo_y), logo)

#         img_bytes = BytesIO()
#         img.save(img_bytes, format='JPEG')
#         img_bytes.seek(0)

#         # Use a specific file name for the uploaded image
#         file_name = f"{employee_id}_birthday_image.jpg"
#         uploaded_image_path = upload_image_to_s3_Scheduler(img_bytes, 'generatedgreeting', 'image/jpeg', file_name)

#         return uploaded_image_path

#     def tomorrowBirthday(self):
#         # Get today's date and the date for tomorrow
#         today = timezone.now().date()
#         tomorrow = today + timedelta(days=1)
        
#         # Get all employees
#         data = Employees.objects.all()
#         for employee in data:
#             # Check if the employee's birthday is tomorrow
#             if employee.employee_dob.day == tomorrow.day and employee.employee_dob.month == tomorrow.month:
#                 # print(f"Employee with birthday tomorrow: {employee.employee_name}, DOB: {employee.employee_dob}")
#                 if employee.company_id is not None:
#                     # Get the company
#                     CompanyTemplateConfig_data = CompanyTemplateConfig.objects.get(company_id=employee.company_id)
#                     template_data = TemplateImage.objects.get(img_Id=CompanyTemplateConfig_data.template_img_id)
#                     image_url = f"https://wishwave.s3.amazonaws.com/{template_data.path}"
#                     logo_url = f"https://wishwave.s3.amazonaws.com/{CompanyTemplateConfig_data.logo_path}"
#                     overlay_input1 = CompanyTemplateConfig_data.content
#                     overlay_input2 = employee.employee_name

#                     contant_coords = (CompanyTemplateConfig_data.content_x, CompanyTemplateConfig_data.content_y) 
#                     emp_name =(CompanyTemplateConfig_data.employname_x, CompanyTemplateConfig_data.employname_y)
#                     logo_coords_database_value = (CompanyTemplateConfig_data.logo_x, CompanyTemplateConfig_data.logo_y)
#                     contant_Text_size = CompanyTemplateConfig_data.text_size
#                     text_colour = CompanyTemplateConfig_data.text_colourcode
#                     logo_size = float(CompanyTemplateConfig_data.logo_size)


#                     # Adjust text2 and logo coordinates
#                     text1_coords = (contant_coords[0] - 23  , contant_coords[1])
#                     text2_coords = (emp_name[0] - 8, emp_name[1])
#                     logo_coords = (logo_coords_database_value[0] - 9, logo_coords_database_value[1] - 8)

                                
#                     # Font sizes and colors for text1 and text2
#                     text1_size = contant_Text_size + 6  # Font size for text1 (add 6 for extra padding)
#                     text2_size = 30 + 20  # Font size for text2 (add 20 for extra padding)
#                     text1_color = text_colour  # Font color for text1
#                     text2_color = text_colour  # Font color for text2

                    
#                     # Path to save the generated image
#                     output_path = "output_image_with_overlay.jpg"
#                     employee_id = employee.employee_id

#                     output_image_path = self.create_image_with_overlay(
#                             image_url, overlay_input1, overlay_input2, logo_url, 
#                             text1_coords, text2_coords, logo_coords, 
#                             text1_size, text2_size, text1_color, text2_color, 
#                             output_path, logo_size,employee_id
#                         )
#                     if output_image_path not in ["error", "None"]:
#                         # print(output_image_path)
#                         # updata path in employee table
#                         employee.file_path = output_image_path
#                         employee.save()
#                         print(employee.file_path)
#     def handle(self, *args, **options):
#           # self.tomorrowBirthday()
#         current_time = timezone.now().time() 
#         # Check if the current time is 6 PM
#         if current_time.hour == 18 and current_time.minute == 0:
#             self.tomorrowBirthday()
#         else:
#             print("This script runs only at 6 PM.")
            

#         # 0 18 * * *
