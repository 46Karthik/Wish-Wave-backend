import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Employees, CompanyTemplateConfig, TemplateImage,OpsView,EmailWhatsAppTable,Schedule
from masterproject.views import upload_image_to_s3_Scheduler
import json

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

    def tomorrowEvent(self):
          # Get today's date and the date for tomorrow
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)  
        tomorrow_event_pepole = OpsView.objects.filter(event_date=tomorrow)
        operation_status = {
                "title": "Image Generation",
                "type": "",
                "count_of_person": 0,
                "success": [],
                "status": [],
            }
        operation_status["count_of_person"] = tomorrow_event_pepole.count()
        for tomorrow_event in tomorrow_event_pepole:
            employee_id = tomorrow_event.employee_id
            employee = Employees.objects.get(employee_id=employee_id)
            employee_status = {
                    "empid": employee.employee_id,
                    "opsid": tomorrow_event.ops_id,
                    "company_id": employee.company_id,
                    "config_id": 0,
                    "image_path": "None",
                    "success": False,
                    "error": [],
                }
            
            print(employee.company_id)
            if employee.company_id is not None:
                if CompanyTemplateConfig.objects.filter(company_id=employee.company_id,active=True).exists():                       
                    # Get company template config
                    company_template_config = CompanyTemplateConfig.objects.get(company_id=employee.company_id,active=True)
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
                        OpsView.objects.filter(ops_id=tomorrow_event.ops_id).update(image_status=True)
                        EmailWhatsAppTable.objects.filter(employee_id=tomorrow_event.employee_id).update(email_image_link=output_image_path,image_generation_timestamp=timezone.now())
                        employee_status["image_path"] = output_image_path
                        employee_status["config_id"] = company_template_config.config_id
                        employee_status["success"] = True
                else:
                    employee_status["error"].append(f"Company template config not found for company id : {employee.company_id}")
            else :
                employee_status["error"].append(f"Company not found")
            operation_status["status"].append(employee_status)
        print(operation_status)   
        schedule_details = {
            "schedule_name": "Image Generation Schedule",
            "details": json.dumps(operation_status)
        }
       # Create a new record
        Schedule.objects.create(
            schedule_name=schedule_details["schedule_name"],
            details=schedule_details["details"]
        )
        print("Schedule created successfully")
     
    def handle(self, *args, **options):
        self.tomorrowEvent()




