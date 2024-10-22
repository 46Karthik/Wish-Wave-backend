from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Company, Employees, Spouse, Child, TemplateImage, CompanyTemplateConfig
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Generates and saves an image with text and logo overlay'

    def create_image_with_overlay(self, image_url, text1, text2, logo_url, text1_coords, text2_coords, logo_coords, 
                                  text1_size, text2_size, text1_color, text2_color, output_path, logo_size):
        # Fetch the main image from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Get image dimensions to scale text/logo placement accordingly
        img_width, img_height = img.size

        # Load the font and set font sizes dynamically for text1 and text2
        try:
            font1 = ImageFont.truetype("arial.ttf", text1_size)  # Ensure you have the correct font
            font2 = ImageFont.truetype("arial.ttf", text2_size)
        except IOError:
            # Fallback to default font in case Arial is not available
            font1 = ImageFont.load_default()
            font2 = ImageFont.load_default()

        # Create an ImageDraw object
        draw = ImageDraw.Draw(img)

        # Convert percentage-based text1 coordinates to actual pixel values
        text1_x = int(img_width * (text1_coords[0] / 100))
        text1_y = int(img_height * (text1_coords[1] / 100))

        # Overlay text1 at the calculated coordinates with the specified font size and color
        draw.text((text1_x, text1_y), text1, fill=text1_color, font=font1)

        # Convert percentage-based text2 coordinates to actual pixel values
        text2_x = int(img_width * (text2_coords[0]  / 100))
        text2_y = int(img_height * (text2_coords[1] / 100))

        # Overlay text2 at the calculated coordinates with the specified font size and color
        draw.text((text2_x, text2_y), text2, fill=text2_color, font=font2)

        # Fetch the logo image from the URL
        response_logo = requests.get(logo_url)
        logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")

        # Calculate the logo width based on the given logoSize percentage
        logo_width = (logo_size / 100) * img_width  # logoSize is now in percentage

        # Maintain aspect ratio by adjusting the height proportionally
        aspect_ratio = logo.width / logo.height
        logo_height = int(logo_width / aspect_ratio)

        # Resize the logo using the calculated dimensions
        logo = logo.resize((int(logo_width), int(logo_height)), Image.Resampling.LANCZOS)

        # Convert percentage-based logo coordinates to actual pixel values
        logo_x = int((logo_coords[0] / 100) * img_width)
        logo_y = int((logo_coords[1] / 100) * img_height)

        # Paste the logo on the image at the calculated coordinates
        img.paste(logo, (logo_x, logo_y), logo)

        # Save the output image to the specified path
        img.save(output_path)
        print(f"Image saved to {output_path}")

    def handle(self, *args, **options):
        # self.generate_image()
        self.tomorrowBirthday(self)

    def generate_image(self):
        # Default values for image and overlay
        image_url = "https://wishwave.s3.amazonaws.com/template/img5.jpeg"
        logo_url = "https://wishwave.s3.amazonaws.com/company/testcompanyLogo%20(1).png"
        overlay_input1 = "Wishing you all the best on your birthday and always!"
        overlay_input2 = "karthik"

        # Coordinates for text and logo  
        contant_coords = (51.388707692826316, 85.78693622688351)  # Text1 coordinates (percentage-based)
        emp_name = (50.007909418824156, 72.30123997082421)  # Text2 coordinates (percentage-based)
        logo_coords_database_value = (11.621717401564185, 8.373854266388586) 
        contant_Text_size = 24
        text_colour = "#2f2f2f"
            
        # Adjust text2 and logo coordinates
        text1_coords = (contant_coords[0] - 23  , contant_coords[1])
        text2_coords = (emp_name[0] - 8, emp_name[1])
        logo_coords = (logo_coords_database_value[0] - 9, logo_coords_database_value[1] - 8)

        # Font sizes and colors for text1 and text2
        text1_size = contant_Text_size + 6  # Font size for text1 (add 6 for extra padding)
        text2_size = 30 + 20  # Font size for text2 (add 20 for extra padding)
        text1_color = text_colour  # Font color for text1
        text2_color = text_colour  # Font color for text2

        # Path to save the generated image
        output_path = "output_image_with_overlay.jpg"

        # Set logo size as a percentage of the image width
        logo_size = 20  # Example: 20% of the image width

        # Generate and save the image with text1, text2, and logo overlay
        self.create_image_with_overlay(
            image_url, overlay_input1, overlay_input2, logo_url, 
            text1_coords, text2_coords, logo_coords, 
            text1_size, text2_size, text1_color, text2_color, 
            output_path, logo_size
        )

    def tomorrowBirthday(self):
        # Get today's date and the date for tomorrow


        # Get all employees
        data = Employees.objects.all()
        for employee in data:
            print(employee)
            # # Check if the employee's birthday is tomorrow
            # if employee.employee_dob.day == tomorrow.day and employee.employee_dob.month == tomorrow.month:
            #     print(f"Employee with birthday tomorrow: {employee.employee_name}, DOB: {employee.employee_dob}")
            