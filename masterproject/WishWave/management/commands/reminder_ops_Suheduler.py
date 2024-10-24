import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from WishWave.models import Employees, CompanyTemplateConfig, TemplateImage,OpsTable
from WishWave.serializers import OpsTableSerializer
from masterproject.views import upload_image_to_s3_Scheduler

class Command(BaseCommand):
    help = 'Generates scheduler based data in Ops table'

    def insetdata_in_opsTable(self):
          # Get today's date and the date for tomorrow
        today = timezone.now().date()
        terget_date = today + timedelta(days=7)
        print(terget_date)
        employees = Employees.objects.filter(employee_dob__day=terget_date.day, employee_dob__month=terget_date.month)
        for employee in employees:
            if employee.company_id is not None:
                    if OpsTable.objects.filter(employee_id =employee.employee_id).exists():
                        print("Employee already exists")
                    else:
                        create_ops_tabel_object = {
                            'company_id' : employee.company_id,
                            'employee_id' : employee.employee_id,
                            'employee_name' : employee.employee_name,
                            'img_path': "",
                            'image_generate': False,
                            'mail_send': False,
                            'whats_app_send': False,
                            'gift_sent': False,
                            'cake_send': False,
                        } 
                        # print(create_ops_tabel_object)
                        serializer = OpsTableSerializer(data=create_ops_tabel_object)
                        if serializer.is_valid():
                            serializer.save()
                            print("success")
                        else:
                            print(serializer.errors)            
    def handle(self, *args, **options):
        self.insetdata_in_opsTable()

