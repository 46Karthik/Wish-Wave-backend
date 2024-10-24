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


import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Employees, CompanyTemplateConfig, TemplateImage,OpsTable
from masterproject.views import upload_image_to_s3_Scheduler

class Command(BaseCommand):
    help = 'Generates and saves an image with text and logo overlay for employees whose birthdays are tomorrow.'

    def create_image_with_overlay(self, image_url, text1, text2, logo_url, text1_coords, text2_coords, logo_coords, 
                                   text1_size, text2_size, text1_color, text2_color, logo_size, employee_id,logo_found):
        # Fetch the main image from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Get image dimensions to scale text/logo placement accordingly
        img_width, img_height = img.size

        # Load the font and set font sizes dynamically for text1 and text2
        try:
            font1 = ImageFont.truetype("arial.ttf", text1_size)
            font2 = ImageFont.truetype("arial.ttf", text2_size)
        except IOError:
            font1 = ImageFont.load_default()
            font2 = ImageFont.load_default()

        draw = ImageDraw.Draw(img)

        # Convert percentage-based coordinates to actual pixel values
        text1_x = int(img_width * (text1_coords[0] / 100))
        text1_y = int(img_height * (text1_coords[1] / 100))
        draw.text((text1_x, text1_y), text1, fill=text1_color, font=font1)

        text2_x = int(img_width * (text2_coords[0]  / 100))
        text2_y = int(img_height * (text2_coords[1] / 100))
        draw.text((text2_x, text2_y), text2, fill=text2_color, font=font2)
        
        if logo_found:
            # Fetch the logo image from the URL
            response_logo = requests.get(logo_url)
            logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")
            logo_width = (logo_size / 100) * img_width
            aspect_ratio = logo.width / logo.height
            logo_height = int(logo_width / aspect_ratio)
            logo = logo.resize((int(logo_width), int(logo_height)), Image.Resampling.LANCZOS)

            logo_x = int((logo_coords[0] / 100) * img_width)
            logo_y = int((logo_coords[1] / 100) * img_height)
            img.paste(logo, (logo_x, logo_y), logo)
            
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        # Use a specific file name for the uploaded image
        file_name = f"{employee_id}_birthday_image.jpg"
        uploaded_image_path = upload_image_to_s3_Scheduler(img_bytes, 'generatedgreeting', 'image/jpeg', file_name)

        return uploaded_image_path

    def tomorrowBirthday(self):
          # Get today's date and the date for tomorrow
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        # Filter employees whose birthdays are tomorrow
        employees = Employees.objects.filter(
            employee_dob__day=tomorrow.day, 
            employee_dob__month=tomorrow.month
            # employee_dob__day=today.day,
            # employee_dob__month=today.month
            )
        for employee in employees:
            if employee.company_id is not None:
                if CompanyTemplateConfig.objects.filter(company_id=employee.company_id).exists():                       
                    # Get company template config
                    company_template_config = CompanyTemplateConfig.objects.get(company_id=employee.company_id)
                    template_data = TemplateImage.objects.get(img_Id=company_template_config.template_img_id)
                
                    image_url = f"https://wishwave.s3.amazonaws.com/{template_data.path}"
                    logo_url = f"https://wishwave.s3.amazonaws.com/{company_template_config.logo_path}"
                    overlay_input1 = company_template_config.content
                    overlay_input2 = employee.employee_name

                    text1_coords = (company_template_config.content_x - 23, company_template_config.content_y)
                    text2_coords = (company_template_config.employname_x - 8, company_template_config.employname_y)
                    logo_coords = (company_template_config.logo_x - 9, company_template_config.logo_y - 8)

                    text1_size = company_template_config.text_size + 6
                    text2_size = 30 + 20
                    text1_color = company_template_config.text_colourcode
                    text2_color = company_template_config.text_colourcode
                    logo_size = float(company_template_config.logo_size)
                    logo_found = False if company_template_config.logo_path in [None, ""] else True
                    
                    # Generate the image
                    output_image_path = self.create_image_with_overlay(
                        image_url, overlay_input1, overlay_input2, logo_url,
                        text1_coords, text2_coords, logo_coords,
                        text1_size, text2_size, text1_color, text2_color,
                        logo_size, employee.employee_id,logo_found
                    )

                    if output_image_path not in ["error", "None"]:
                        # employee.file_path = output_image_path
                        # employee.save()
                        if OpsTable.objects.filter(employee_id =employee.employee_id).exists():
                            OpsTable.objects.filter(employee_id =employee.employee_id).update(img_path=output_image_path,image_generate=True)
                            print("Employee updated in OpsTable")
                        else:
                            print("OpsTable not Employee found")
                            
                        
                else:
                    print("Company template config not set")
    def handle(self, *args, **options):
        self.tomorrowBirthday()
        # current_time = timezone.now().time()
        # # Check if the current time is 6 PM
        # if current_time.hour == 18 and current_time.minute == 0:
        #     self.tomorrowBirthday()
        # else:
        #     print("This script runs only at 6 PM.")

