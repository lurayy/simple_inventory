from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    USER_TYPES = (
    ('STAFF', "Staff"),
    ('MANAGER', "Manager")
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='STAFF')

   
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Vendor(models.Model):
    ''' Vendor model'''
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)

    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(null=True, max_length=255)
    tax_number = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=25)
    phone2 = models.CharField(max_length=25)
    address = models.TextField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Customer(models.Model):
    ''' model schema for customer '''
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(null=True, max_length=255)
    tax_number = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=25)
    phone2 = models.CharField(max_length=25)
    address = models.TextField()


    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} + {self.last_name}'

class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.PositiveIntegerField()
    tax_types = (
        ('fixed', "Fixed"),
        ('normal', "Normal")
    )
    tax_type = models.CharField(max_length=30, choices=tax_types, default='normal')
    code = models.CharField(max_length=255, null=True, blank=True, default=" ")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.rate}'

class Discount(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    discount_types =(
        ('fixed',"Fixed"),
        ('percent', "Percent")
    )
    discount_type = models.CharField(max_length=20, default="Percent")
    rate = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.code} {self.rate}'
