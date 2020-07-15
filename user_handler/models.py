from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from .models_permission import CustomPermission
import random

class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    role = models.ForeignKey(CustomPermission, on_delete=models.PROTECT, related_name='role_users', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def image_directory_path(instance, filename):
    return 'image/user_{0}/image_{1}.jpg'.format(instance.user.username, random.randint(0,100))


class Profile(models.Model):
    user = models.OneToOneField(CustomUserBase, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    phone_number2 = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to= image_directory_path, null=True, blank=True)
    post = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.user)


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



class CustomerCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name}'

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
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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
