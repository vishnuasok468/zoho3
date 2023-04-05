from django.db import models
from django.contrib.auth.models import User

class customer_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    company_email = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=255)
    industry_type = models.CharField(max_length=255)
