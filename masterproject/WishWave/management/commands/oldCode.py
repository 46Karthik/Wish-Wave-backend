 # help = 'Generates scheduler based data in Ops table'
    # def insetdata_in_opsTable(self):
    #       # Get today's date and the date for tomorrow
    #     today = timezone.now().date()
    #     terget_date = today + timedelta(days=7)
    #     print(terget_date)

    #     # Employee Brithday 
    #     employees = Employees.objects.filter(employee_dob__day=terget_date.day, employee_dob__month=terget_date.month)
    #     for employee in employees:
    #         if employee.company_id is not None:
    #                 def format_date(date):
    #                         return date.strftime('%Y-%m-%d') if date else None
    #                 subscriptionCodeVaue = ""
    #                 if OpsView.objects.filter(employee_id =employee.employee_id,occasion ='birthday',relation ='Employee').exists():
    #                     print("Employee already exists")
    #                 else:
    #                     # get company details
    #                     company = Company.objects.get(company_id=employee.company_id)
    #                     subscriptions = Subscription.objects.filter(company_id=employee.company_id,occasion ='birthday',key_name = employee.employee_dept)
    #                     try:
    #                         subscription_Code_result = ""
    #                         company = Company.objects.get(company_id=employee.company_id)
    #                         subscription = Subscription.objects.get(company_id=employee.company_id, occasion='birthday',key_name = employee.employee_dept)
    #                         if subscription.email:
    #                             subscription_Code_result += "E"
    #                         if subscription.whatsapp:
    #                             subscription_Code_result += "W"
    #                         if subscription.gift not in [None, ""]:
    #                             subscription_Code_result += "G"
    #                         if subscription.custom_gift not in [None, ""]:
    #                             subscription_Code_result += "C"
    #                         print(subscription_Code_result)
    #                     except Subscription.DoesNotExist:
    #                         print("No subscription found for the given company and occasion.")
    #                     except Subscription.MultipleObjectsReturned:
    #                         print("Multiple subscriptions found. Please check your data.")

                        
                        
    #                     create_ops_table_object = {
    #                         "company_id": employee.company_id,
    #                         "company_name": company.company_name,
    #                         "occasion": "Birthday",
    #                         "event_date": format_date(terget_date),
    #                         "employee_id": employee.employee_id,
    #                         "name_of_person": employee.employee_name,
    #                         "relation": "Employee",
    #                         "address1": employee.address,
    #                         "address2": employee.address2, 
    #                         "city": employee.city,
    #                         "zipcode": employee.pincode,
    #                         "email_id": employee.employee_email,
    #                         "phone_number": employee.whatsapp_phone_number,
    #                         "subscription": subscription_Code_result,
    #                         "image_status": "False",
    #                         "email_status": "False",
    #                         "whatsapp_status": "False",
    #                         "cake_status": "False",
    #                         "gift_status": "False",
    #                         "cake_order_date": None,
    #                         "cake_delivery_date": None,
    #                         "cake_otp": "",
    #                         "gift_order_date": None,
    #                         "gift_delivery_date": None,
    #                         "gift_otp": ""
    #                     }
    #                     # print(create_ops_table_object)
                        
    #                     create_EmailWhatsAppTable ={
    #                         "employee_id": employee.employee_id,
    #                         "company_id": employee.company_id,
    #                         "email_id": employee.employee_email,
    #                         "phone_number": employee.whatsapp_phone_number,
    #                         "email_image_link": "",
    #                         "whatsapp_image_link": "",
    #                         "subscription_details": subscription_Code_result,
    #                         "event_date": format_date(terget_date),
    #                         "image_generation_timestamp": None,
    #                         "mail_schedule_time": format_date(terget_date),
    #                         "whatsapp_schedule_time": format_date(terget_date),
    #                         "mail_sent_time": None,
    #                         "whatsapp_sent_time": None
    #                     }

    #                     vendor_details = Vendor.objects.filter(pin=employee.pincode).first()
    #                     if  vendor_details is None:
    #                         print("vendor not found")
    #                     create_cake_and_gift = {
    #                         "employee_id":  employee.employee_id,
    #                         "company_id":  employee.company_id,
    #                         "email_id":  employee.employee_email,
    #                         "phone_number":  employee.whatsapp_phone_number,
    #                         "delivery_address1": employee.address,
    #                         "delivery_address2": employee.address2,
    #                         "delivery_city": employee.city,
    #                         "delivery_zip": employee.pincode,

    #                         "cake_scheduled_delivery_date": None,
    #                         "cake_scheduled_order_date": None,
    #                         "cake_vendor_id": vendor_details.id,
    #                         "cake_shop_name": vendor_details.name_of_vendor ,
    #                         "cake_from_address": vendor_details.address_1,
    #                         "cake_from_city": vendor_details.city,
    #                         "cake_from_state": vendor_details.state,
    #                         "cake_from_pincode": vendor_details.pin,
    #                         "cake_flavour": "",
    #                         "cake_weight": None,
    #                         "cake_wish_message": f"Happy Birthday, {employee.employee_name}!",
    #                         "cake_delivery_person_name": "",
    #                         "cake_delivery_person_number": "",
    #                         "cake_delivery_verification_link": "",
    #                         "cake_otp": "",

    #                         "gift_scheduled_delivery_date": None,
    #                         "gift_scheduled_order_date": None,
    #                         "gift_vendor_id": vendor_details.id,
    #                         "gift_shop_name": vendor_details.name_of_vendor,
    #                         "gift_from_address": vendor_details.address_1,
    #                         "gift_from_city": vendor_details.city,
    #                         "gift_from_state": vendor_details.state,
    #                         "gift_from_pincode": vendor_details.pin,
    #                         "gift_article_number": "",
    #                         "gift_weight": None,
    #                         "gift_delivery_person_name": "",
    #                         "gift_delivery_person_number": "",
    #                         "gift_delivery_verification_link": "",
    #                         "gift_otp": ""
    #                     }
    #                     Opsserializer = OpsViewSerializer(data=create_ops_table_object)
    #                     EmailWhatsappSerializer = EmailWhatsAppTableSerializer(data=create_EmailWhatsAppTable)
    #                     CakeAndGift_Serializer = CakeAndGiftSerializer(data=create_cake_and_gift)
    #                     if Opsserializer.is_valid():
    #                         if EmailWhatsappSerializer.is_valid():
    #                             if CakeAndGift_Serializer.is_valid():
    #                                 Opsserializer.save()
    #                                 EmailWhatsappSerializer.save()
    #                                 CakeAndGift_Serializer.save()
    #                             else:
    #                                 print(CakeAndGift_Serializer.errors)
    #                         else:
    #                             print(EmailWhatsappSerializer.errors)          
    #                     else:
    #                         # print('Error')
    #                         print(Opsserializer.errors)            
    # def handle(self, *args, **options):
    #     self.insetdata_in_opsTable()