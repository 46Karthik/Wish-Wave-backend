# from django.core.mail import send_mail
# from django.core.management.base import BaseCommand
# from rest_framework.response import Response
# from rest_framework import status

# class Command(BaseCommand):
#     help = 'Sends a birthday wish email'

#     def handle(self, *args, **options):
#         self.send_mail_wish()

#     def send_mail_wish(self):
#         name = 'foul'
#         subject = "Happy Birthday"
#         message = f"Dear {name},\n\nWe just wanted to wish you a wonderful birthday in advance! 🎉\n\nBest wishes from all of us!"
#         from_email = 'karthikJio66@gmail.com' 
#         recipient_list = ['karthikfoul66@gmail.com'] 
        
#         try:
#             send_mail(subject, message, from_email, recipient_list)
#             self.stdout.write(self.style.SUCCESS('Email sent successfully!'))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))



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
        
        # Render the HTML template
        html_content = render_to_string('Wish_temp.html', {
            'employee_name': employee_name,
            'image_src': 'https://res.cloudinary.com/dzofo8q8p/image/upload/v1729156873/img5_dvqdtg.jpg'  
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
