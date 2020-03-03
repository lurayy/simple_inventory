from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    is_super = models.BooleanField(default=True)

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


class Item(models.Model):
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    #number of items registered 
    quantity = models.PositiveIntegerField()
    rate = models.FloatField()

    is_active = models.BooleanField(default=True)
    is_in_stock = models.BooleanField(default=True)

    # number of items still in stock
    stock = models.PositiveIntegerField()

    class Meta:
        unique_together = ['vendor', 'rate', 'name']

    def __str__(self):
        return f'{self.name}'
    
    

class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Placement(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    placed_on = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    qunatity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item} on {self.placed_on}'


@receiver(models.signals.post_save, sender=Item)
def placement_creator(sender, instance, created, *args, **kwargs):
    print('triggered')
    if created:
        print('created')
        try:
            place = Place.objects.get(name='Unassigned')
        except:
            place = Place.objects.create(name='Unassigned')
        placement = Placement.objects.create(item=instance, placed_on=place, qunatity=instance.stock)
        placement.save()