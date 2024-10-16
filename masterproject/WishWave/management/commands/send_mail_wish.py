# # employees/management/commands/check_birthdays.py

# from django.core.mail import send_mail
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# # from employees.models import Employee  # Update the import path based on your model location

# class Command(BaseCommand):
#     help = 'Checks for upcoming employee birthdays and sends reminder emails'

#     # def handle(self, *args, **kwargs):
#     #     today = timezone.now().date()
#     #     tomorrow = today + timedelta(days=1)

#     #     # Query to find employees with birthdays tomorrow
#     #     upcoming_birthdays = Employee.objects.filter(employee_dob__month=tomorrow.month, employee_dob__day=tomorrow.day)

#     #     for employee in upcoming_birthdays:
#     #         self.send_birthday_email(employee)

#     # def send_birthday_email(self, employee):
#     #     subject = f"Happy Upcoming Birthday, {employee.employee_name}!"
#     #     message = f"Dear {employee.employee_name},\n\nWe just wanted to wish you a wonderful birthday in advance! 🎉\n\nBest wishes from all of us!"
        
#     #     # Send the email
#     #     try:
#     #         send_mail(
#     #             subject,
#     #             message,
#     #             'karthikfoul66@gmail.com',  # From email
#     #             [employee.employee_email],  # To email
#     #             fail_silently=False,
#     #         )
#     #         self.stdout.write(self.style.SUCCESS(f"Sent birthday email to {employee.employee_name} ({employee.employee_email})"))
#     #     except Exception as e:
#     #         self.stdout.write(self.style.ERROR(f"Failed to send email to {employee.employee_name}: {e}"))

#     def send_Mail_Wish():
#             name = 'foul'
#             subject = "Happy brithday"
#             message = f"Dear {name},\n\nWe just wanted to wish you a wonderful birthday in advance! 🎉\n\nBest wishes from all of us!"
#             from_email = 'karthikfoul66@gamil.com' 
#             recipient_list = 'karthikJio66@gamil.com' 

#             try:
#                 send_mail(subject, message, from_email, recipient_list)
#                 return Response(return_response(2, 'Email sent successfully!'), status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': 'Failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Sends a birthday wish email with HTML content and an image from a URL'

    def handle(self, *args, **options):
        self.send_mail_wish()

    def send_mail_wish(self):
        name = 'Foul'
        subject = "Happy Birthday!"
        from_email = 'karthikjio66@gamil.com'
        to_email = ['karthikfoul66@gamil.com']

        # URL to the hosted image
        image_url = 'https://res.cloudinary.com/dzofo8q8p/image/upload/v1729078619/image-with-text-and-logo_4_cudwl1.png'  # Replace with your actual image URL

        # Prepare HTML content with the image URL
        html_content = render_to_string('Wish_temp.html', {
            'employee_name': name,
            'image_url': image_url
        })

        # Create the email
        msg = EmailMultiAlternatives(subject, '', from_email, to_email)

        # Attach HTML content as an alternative
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        try:
            msg.send()
            self.stdout.write(self.style.SUCCESS('HTML email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
