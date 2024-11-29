import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.core.management.base import BaseCommand
from WishWave.models import Employees,OpsView,EmailWhatsAppTable,Schedule
from io import BytesIO
import requests
from datetime import datetime, date
from masterproject.views import get_company_email_config,decrypt_password
from django.utils import timezone
import json
class Command(BaseCommand):
    help = 'Downloads an image, sends an email with the image, and deletes the image afterward.'

    def handle(self, *args, **options):
        self.Sendmail_Today_Employee_wish()
    # def download_and_send_image(self, email_list, image_url,employee_id):
    #     try:
    #         # Step 1: Download the image
    #         response = requests.get(image_url)
    #         if response.status_code == 200:
    #             image_data = BytesIO(response.content)  # Image is stored in memory
    #             self.stdout.write(self.style.SUCCESS(f"Image successfully downloaded from {image_url}"))
    #             mail_config = get_company_email_config(employee.company_id)
    #             user = mail_config.get('user')
    #             pwd = mail_config.get('pwd')
                
    #             # Step 2: Send the email with the image attached
    #             from_addr = user

    #             for email in email_list:
                    
    #                 to_addr = email
    #                 msg = MIMEMultipart()
    #                 msg['From'] = from_addr
    #                 msg['To'] = to_addr
    #                 msg['Subject'] = "Happy Birthday!"

    #                 body = """
    #                 <html>
    #                     <body>
    #                        <img src='cid:Mailtrapimage' style="width: 100%; max-width: 600px; height: auto;">
    #                     </body>
    #                 </html>
    #                 """
    #                 msg.attach(MIMEText(body, 'html'))

    #                 # Step 3: Attach the downloaded image to the email
    #                 image = MIMEImage(image_data.getvalue())
    #                 image.add_header('Content-ID', '<Mailtrapimage>')
    #                 msg.attach(image)

    #                 # Step 4: Send the email
    #                 try:
    #                     with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #                         server.ehlo()
    #                         server.starttls()
    #                         server.ehlo()
    #                         server.login(user, pwd)
    #                         server.sendmail(from_addr, to_addr, msg.as_string())
    #                         OpsView.objects.filter(employee_id=employee_id).update(email_status=True)
                             
    #                         # self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
    #                         return f"Email successfully sent to {email}"
    #                 except Exception as e:
    #                     self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

    #         else:
    #             self.stdout.write(self.style.ERROR(f"Failed to download image, status code: {response.status_code}"))

    #     except Exception as e:
    #         self.stdout.write(self.style.ERROR(f"Error while downloading or sending the image: {e}"))

    def Sendmail_Today_Employee_wish(self):
        today = date.today()  # Get today's date
        
        # Step 1: Filter employees whose birthday is today (day and month match) and their OpsTable is not empty
        event_list =  OpsView.objects.filter(event_date=today)
        operation_status = {
                "title": "Email Scheduler",
                "count_of_person": 0,
                "success": [],
                "status": [],
            }
        operation_status["count_of_person"] = event_list.count()

        for event in event_list:
            employee = Employees.objects.get(employee_id=event.employee_id)
            Email_status = {
                    "empid": event.employee_id,
                    "opsid": event.ops_id,
                    "company_id": employee.company_id,
                    "Email_ID": event.email_id,
                    "image_path": "None",
                    "success": False,
                    "error": [],
                }
            Subscription_plan = event.subscription
            if Subscription_plan == "E":
                if  EmailWhatsAppTable.objects.filter(employee_id =event.employee_id).exists():
                    image_path_OpsTable = EmailWhatsAppTable.objects.get(employee_id =event.employee_id).email_image_link
                    Email_status["image_path"] = image_path_OpsTable
                    email_list = [event.email_id] 
                    image_url = f"https://wishwave.s3.amazonaws.com/{image_path_OpsTable}"
                    employee_id = event.employee_id
                    
                    # self.download_and_send_image(email_list, image_url,employee_id)
                    try:
                        # Step 1: Download the image
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_data = BytesIO(response.content)  # Image is stored in memory
                            self.stdout.write(self.style.SUCCESS(f"Image successfully downloaded from {image_url}"))

                            mail_config = get_company_email_config(employee.company_id)
                            username = mail_config.get('user')
                            # from_addr = user
                            pwds = mail_config.get('pwd')
                            print(username,"---------------")
                            try:
                                decrypted_password = decrypt_password(pwds)
                                print("Decrypted Password:", decrypted_password)
                            except ValueError as e:
                                print("Error:", e)
                            print(pwds,"---------------")
                    
                            # Step 2: Send the email with the image attached
                            
                            
                            # # Step 2: Send the email with the image attached
                            from_addr = "karthikfoul66@gmail.com"
                            user = 'karthikfoul66@gmail.com'
                            pwd = 'veri lfrz yymz cytu'

                            for email in email_list:
                                
                                to_addr = email
                                msg = MIMEMultipart()
                                msg['From'] = from_addr
                                msg['To'] = to_addr
                                msg['Subject'] = f"Happy {event.occasion}!"

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
                                        OpsView.objects.filter(employee_id=employee_id).update(email_status=True)
                                        Email_status["success"] = True
                                        self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
                                        
                                except Exception as e:
                                    Email_status["error"].append(f"Failed to send email to {email}: {e}")
                                    self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

                        else:
                            Email_status["error"].append(f"Failed to download image, status code: {response.status_code}")
                            self.stdout.write(self.style.ERROR(f"Failed to download image, status code: {response.status_code}"))

                    except Exception as e:
                        Email_status["error"].append(f"Error while downloading or sending the image: {e}")
                        self.stdout.write(self.style.ERROR(f"Error while downloading or sending the image: {e}"))
                else:
                    Email_status["error"].append(f'Email image not found for employee id : {event.employee_id}')
            else:
                Email_status["error"].append(f'Subscription details not found for employee id : {event.employee_id}, Occasion : {event.occasion},Subscription Plan : {Subscription_plan}')
            operation_status["status"].append(Email_status)
        print(operation_status)
        schedule_details = {
            "schedule_name": "Email Scheduler",
            "details": json.dumps(operation_status)
        }
       # Create a new record
        Schedule.objects.create(
            schedule_name=schedule_details["schedule_name"],
            details=schedule_details["details"]
        )
        print("Schedule created successfully")