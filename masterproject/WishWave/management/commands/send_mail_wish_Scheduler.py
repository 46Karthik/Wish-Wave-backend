# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from django.core.management.base import BaseCommand
# from WishWave.models import Employees
# from io import BytesIO
# import requests
# from datetime import datetime
# from django.utils import timezone
# from datetime import timedelta

# class Command(BaseCommand):
#     help = 'Downloads an image, sends an email with the image, and deletes the image afterward.'

#     def handle(self, *args, **options):
#         current_time = timezone.now().time() 
#         # Check if the current time is 6 PM
#         if current_time.hour == 6 and current_time.minute == 0:
#             # Call the function to send today's employee birthday wishes
#             self.Sendmail_Today_Employee_wish()
#         else:
#             print("This script runs only at 6 AM.")

       

#     def download_and_send_image(self, email_list, image_url):
#         try:
#             # Step 1: Download the image
#             response = requests.get(image_url)
#             if response.status_code == 200:
#                 image_data = BytesIO(response.content)  # Image is stored in memory
#                 self.stdout.write(self.style.SUCCESS(f"Image successfully downloaded from {image_url}"))

#                 # Step 2: Send the email with the image attached
#                 from_addr = "karthikfoul66@gmail.com"
#                 user = 'karthikfoul66@gmail.com'
#                 pwd = 'veri lfrz yymz cytu'

#                 for email in email_list:
#                     to_addr = email
#                     msg = MIMEMultipart()
#                     msg['From'] = from_addr
#                     msg['To'] = to_addr
#                     msg['Subject'] = "Happy Birthday!"

#                     body = """
#                     <html>
#                         <body>
#                            <img src='cid:Mailtrapimage' style="width: 100%; max-width: 600px; height: auto;">
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(body, 'html'))

#                     # Step 3: Attach the downloaded image to the email
#                     image = MIMEImage(image_data.getvalue())
#                     image.add_header('Content-ID', '<Mailtrapimage>')
#                     msg.attach(image)

#                     # Step 4: Send the email
#                     try:
#                         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#                             server.ehlo()
#                             server.starttls()
#                             server.ehlo()
#                             server.login(user, pwd)
#                             server.sendmail(from_addr, to_addr, msg.as_string())
#                             self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
#                     except Exception as e:
#                         self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

#             else:
#                 self.stdout.write(self.style.ERROR(f"Failed to download image, status code: {response.status_code}"))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Error while downloading or sending the image: {e}"))

#     def Sendmail_Today_Employee_wish(self):
#         today = datetime.today()  # Get today's date
#         data = Employees.objects.all()

#         for employee in data:
#             # Check if the employee's birthday matches today's date
#             if employee.employee_dob.day == today.day and employee.employee_dob.month == today.month:
#                 email_list = [employee.employee_email]  # Use the employee's email
#                 image_url = f"https://wishwave.s3.amazonaws.com/{employee.file_path}"
#                 self.download_and_send_image(email_list, image_url)


import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.core.management.base import BaseCommand
from WishWave.models import Employees,OpsTable
from io import BytesIO
import requests
from datetime import datetime, date
from django.utils import timezone

class Command(BaseCommand):
    help = 'Downloads an image, sends an email with the image, and deletes the image afterward.'

    def handle(self, *args, **options):
        self.Sendmail_Today_Employee_wish()
        # current_time = timezone.now().time()
        # # Check if the current time is 6 AM
        # if current_time.hour == 6 and current_time.minute == 0:
        #     # Call the function to send today's employee birthday wishes
        #     self.Sendmail_Today_Employee_wish()
        # else:
        #     print("This script runs only at 6 AM.")

    def download_and_send_image(self, email_list, image_url,employee_id):
        try:
            # Step 1: Download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)  # Image is stored in memory
                self.stdout.write(self.style.SUCCESS(f"Image successfully downloaded from {image_url}"))

                # Step 2: Send the email with the image attached
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

                    # Step 3: Attach the downloaded image to the email
                    image = MIMEImage(image_data.getvalue())
                    image.add_header('Content-ID', '<Mailtrapimage>')
                    msg.attach(image)

                    # Step 4: Send the email
                    try:
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.ehlo()
                            server.starttls()
                            server.ehlo()
                            server.login(user, pwd)
                            server.sendmail(from_addr, to_addr, msg.as_string())
                            OpsTable.objects.filter(employee_id=employee_id).update(mail_send=True)
                            self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

            else:
                self.stdout.write(self.style.ERROR(f"Failed to download image, status code: {response.status_code}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error while downloading or sending the image: {e}"))

    def Sendmail_Today_Employee_wish(self):
        today = date.today()  # Get today's date

        # Step 1: Filter employees whose birthday is today (day and month match)
        employees_with_birthday_today = Employees.objects.filter(
            employee_dob__day=today.day,
            employee_dob__month=today.month
        )

        # Step 2: Iterate over the filtered employee data
        for employee in employees_with_birthday_today:
            if OpsTable.objects.filter(employee_id =employee.employee_id).exists():
                image_path_OpsTable = OpsTable.objects.get(employee_id =employee.employee_id).img_path
                email_list = [employee.employee_email]  # Use the employee's email
                image_url = f"https://wishwave.s3.amazonaws.com/{image_path_OpsTable}"
                employee_id = employee.employee_id
                self.download_and_send_image(email_list, image_url,employee_id)
            else:
                print("Ops table Employee not found ",employee.employee_id)
