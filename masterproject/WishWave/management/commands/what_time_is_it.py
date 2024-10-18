from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

class Command(BaseCommand):
    help = 'Generates and saves an image with a text and logo overlay'

    def create_image_with_overlay(self, image_url, text, logo_url, text_coords, logo_coords, output_path):
        # Fetch the main image from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Get image dimensions to scale text/logo placement accordingly
        img_width, img_height = img.size

        # Load the font and dynamically scale the font size based on the image size
        font_size = int(img_width * 0.05)  # Adjust the multiplier as necessary
        font = ImageFont.truetype("arial.ttf", font_size)

        # Create an ImageDraw object
        draw = ImageDraw.Draw(img)

        # Convert percentage-based text coordinates to actual pixel values
        text_x = int(img_width * (text_coords[0] / 100))
        text_y = int(img_height * (text_coords[1] / 100))

        # Overlay text at the calculated coordinates
        # Adjust the position slightly (e.g., down by a few pixels)
        draw.text((text_x, text_y - 10), text, fill="red", font=font)

        # Fetch the logo image from the URL
        response_logo = requests.get(logo_url)
        logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")

        # Resize the logo proportionally based on the image size
        logo_size = int(img_width * 0.15)  # Adjust this multiplier as necessary
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Convert percentage-based logo coordinates to actual pixel values
        logo_x = int((logo_coords[0] / 100) * img_width)
        logo_y = int((logo_coords[1] / 100) * img_height)

        # Adjust the logo position slightly (e.g., up by a few pixels)
        img.paste(logo, (logo_x, logo_y), logo)

        # Save the output image to the specified path
        img.save(output_path)
        print(f"Image saved to {output_path}")

    def handle(self, *args, **options):
        self.generate_image()

    def generate_image(self):
        # Default values for image and overlay
        image_url = "https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156873/img5_dvqdtg.jpg"
        logo_url = "https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156915/WishWave_gmqjng.png"
        overlay_input = "Karthik"
        text_coords = (42, 70)  # formula correct values "-8"
        logo_coords = (9.722041026159655, 8.07601813704261)  # Percentages
        # logo_coords = (1.02, 6.07601813704261)  # Percentages

        # Path to save the generated image
        output_path = "output_image.jpg"

        # Generate and save the image with text and logo overlay
        self.create_image_with_overlay(image_url, overlay_input, logo_url, text_coords, logo_coords, output_path)
