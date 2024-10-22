import os
import base64
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Command(BaseCommand):
    help = 'Sends a birthday wish email'

    def handle(self, *args, **options):
        self.send_mail_wish()

    def send_mail_wish(self):
        employee_name = 'foul'
        subject = "Happy Birthday"
        
        # Local image path
        image_path = './output_image.jpg'  # Update this path as necessary
        
        # Encode the image as base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Render the HTML template with the inline image
        html_content = render_to_string('Wish_temp.html', {
            'employee_name': employee_name,
            'image_src': f'data:image/jpeg;base64,{encoded_image}'  
        })
        
        # Create a plain-text version of the email
        text_content = strip_tags(html_content)
        
        from_email = 'karthikJio66@gmail.com' 
        recipient_list = ['karthikfoul66@gmail.com'] 
        
        # Create the email object
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        
        try:
            email.send()
            self.stdout.write(self.style.SUCCESS('Email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))



# import requests
# from django.core.mail import EmailMultiAlternatives
# from django.core.management.base import BaseCommand
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.core.files.base import ContentFile

# class Command(BaseCommand):
#     help = 'Sends a birthday wish email'

#     def handle(self, *args, **options):
#         self.send_mail_wish()

#     def send_mail_wish(self):
#         employee_name = 'foul'
#         subject = "Happy Birthday"
        
#         # Render the HTML template
#         html_content = render_to_string('Wish_temp.html', {
#             'employee_name': employee_name,
#             'image_src': 'https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156873/img5_dvqdtg.jpg'  
#         })
        
#         # Create a plain-text version of the email
#         text_content = strip_tags(html_content)
        
#         from_email = 'karthikJio66@gmail.com' 
#         recipient_list = ['karthikfoul66@gmail.com'] 
        
#         # Create the email object
#         email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
#         email.attach_alternative(html_content, "text/html")
        
#         # Fetch the image from the URL
#         image_url = 'https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156873/img5_dvqdtg.jpg'
#         response = requests.get(image_url)
        
#         if response.status_code == 200:
#             # Attach the image
#             image_name = 'birthday_image.jpg'  # You can change the name if needed
#             email.attach(image_name, response.content, 'image/jpeg')
#         else:
#             self.stdout.write(self.style.WARNING('Failed to fetch image for attachment.'))

#         try:
#             email.send()
#             self.stdout.write(self.style.SUCCESS('Email sent successfully!'))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
