from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Company, Employees, Spouse, Child, TemplateImage, CompanyTemplateConfig
from django.utils import timezone
from datetime import timedelta
from masterproject.views import upload_image_to_s3

class Command(BaseCommand):
    help = 'Generates and saves an image with text and logo overlay'

    def create_image_with_overlay(self, image_url, text1, text2, logo_url, text1_coords, text2_coords, logo_coords, 
                                   text1_size, text2_size, text1_color, text2_color, logo_size):
        # Create an in-memory image
        img = Image.new('RGB', (800, 600), color='white')  # Create a blank image or load from URL as needed

        # Load the font and set font sizes dynamically for text1 and text2
        try:
            font1 = ImageFont.truetype("arial.ttf", text1_size)  # Ensure you have the correct font
            font2 = ImageFont.truetype("arial.ttf", text2_size)
        except IOError:
            font1 = ImageFont.load_default()
            font2 = ImageFont.load_default()

        draw = ImageDraw.Draw(img)

        # Overlay text1
        draw.text(text1_coords, text1, fill=text1_color, font=font1)

        # Overlay text2
        draw.text(text2_coords, text2, fill=text2_color, font=font2)

        # Create a BytesIO object to hold the image
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)  # Move to the beginning of the BytesIO object

        return img_byte_arr

    def tomorrowBirthday(self):
        # Get today's date and the date for tomorrow
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        # Get all employees
        data = Employees.objects.all()
        for employee in data:
            # Check if the employee's birthday is tomorrow
            if employee.employee_dob.day == tomorrow.day and employee.employee_dob.month == tomorrow.month:
                if employee.company_id is not None:
                    # Get the company
                    CompanyTemplateConfig_data = CompanyTemplateConfig.objects.get(company_id=employee.company_id)
                    template_data = TemplateImage.objects.get(img_Id=CompanyTemplateConfig_data.template_img_id)
                    image_url = f"https://wishwave.s3.amazonaws.com/{template_data.path}"
                    logo_url = f"https://wishwave.s3.amazonaws.com/{CompanyTemplateConfig_data.logo_path}"
                    text1 = CompanyTemplateConfig_data.content
                    text2 = employee.employee_name

                    contant_coords = (CompanyTemplateConfig_data.content_x, CompanyTemplateConfig_data.content_y) 
                    emp_name =(CompanyTemplateConfig_data.employname_x, CompanyTemplateConfig_data.employname_y)
                    logo_coords_database_value = (CompanyTemplateConfig_data.logo_x, CompanyTemplateConfig_data.logo_y)
                    contant_Text_size = CompanyTemplateConfig_data.text_size
                    text_colour = CompanyTemplateConfig_data.text_colourcode
                    logo_size = float(CompanyTemplateConfig_data.logo_size)

                    # Adjust text2 and logo coordinates
                    text1_coords = (contant_coords[0] - 23  , contant_coords[1])
                    text2_coords = (emp_name[0] - 8, emp_name[1])
                    logo_coords = (logo_coords_database_value[0] - 9, logo_coords_database_value[1] - 8)

                    # Font sizes and colors for text1 and text2
                    text1_size = contant_Text_size + 6  # Font size for text1 (add 6 for extra padding)
                    text2_size = 30 + 20  # Font size for text2 (add 20 for extra padding)
                    text1_color = text_colour  # Font color for text1
                    text2_color = text_colour  # Font color for text2

                    # Generate the image
                    file = self.create_image_with_overlay(image_url, text1, text2, logo_url, text1_coords, text2_coords,
                                                          logo_coords=None, text1_size=text1_size,
                                                          text2_size=text2_size, text1_color=text1_color,
                                                          text2_color=text2_color, logo_size=logo_size)

                    file.name = f"generated_image{employee.employee_id}.jpg"  

                    # Upload to S3
                    file_path = upload_image_to_s3(file, 'generatedgreeting','image/jpg')

                    print(f"File uploaded to: {file_path}")

    def handle(self, *args, **options):
        self.tomorrowBirthday()
