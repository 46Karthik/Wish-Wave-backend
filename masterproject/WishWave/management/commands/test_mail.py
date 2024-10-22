import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

class Command(BaseCommand):
    help = 'Generates an image, sends an email with the image, and deletes the image afterward.'

    def handle(self, *args, **options):
        email_list = ['karthikfoul66@gmail.com']
        # Step 1: Generate the image
        output_image_path = self.generate_image()
        # Step 2: Send the image via email
        self.send_email(email_list, output_image_path)
        # Step 3: Delete the image file after sending the email
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
            self.stdout.write(self.style.SUCCESS(f"Image {output_image_path} deleted after sending the email"))

    def generate_image(self):
        image_url = "https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156873/img5_dvqdtg.jpg"
        logo_url = "https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156915/WishWave_gmqjng.png"
        text = "Karthik"
        text_coords = (42, 70)  # Percentage values
        logo_coords = (9.72, 8.08)  # Percentage values
        output_path = "output_image.jpg"

        # Fetch the main image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Get image dimensions and load the font
        img_width, img_height = img.size
        font_size = int(img_width * 0.05)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw text on the image
        draw = ImageDraw.Draw(img)
        text_x = int(img_width * (text_coords[0] / 100))
        text_y = int(img_height * (text_coords[1] / 100))
        draw.text((text_x, text_y), text, fill="red", font=font)

        # Fetch and overlay the logo
        response_logo = requests.get(logo_url)
        logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")
        logo_size = int(img_width * 0.15)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        logo_x = int(img_width * (logo_coords[0] / 100))
        logo_y = int(img_height * (logo_coords[1] / 100))
        img.paste(logo, (logo_x, logo_y), logo)

        # Save the output image
        img.save(output_path)
        self.stdout.write(self.style.SUCCESS(f"Image generated and saved to {output_path}"))

        return output_path

    def send_email(self, email_list, image_path):
        from_addr = "karthikfoul66@gmail.com"
        user = 'karthikfoul66@gmail.com'
        pwd = 'veri lfrz yymz cytu'

        for email in email_list:
            to_addr = email
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = "Happy Birthday!"

            body = """
            <html>
                <body>
                   <img src='cid:Mailtrapimage' style="width: 100%; max-width: 600px; height: auto;">
                </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))

            # Attach the generated image
            with open(image_path, 'rb') as fp:
                image = MIMEImage(fp.read())
                image.add_header('Content-ID', '<Mailtrapimage>')
                msg.attach(image)

            # Send the email using Gmail's SMTP server
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(user, pwd)
                    server.sendmail(from_addr, to_addr, msg.as_string())
                    self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

