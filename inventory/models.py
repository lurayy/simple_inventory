from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    
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


class PurchaseOrder(models.Model):
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    invoiced_on = models.DateTimeField()
    completed_on = models.DateTimeField(null=True, blank=True) 
    
    DISCOUNT = (
        ('PERCENT', "percent"),
        ('FIXED', "fixed")
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='PERCENT')

    discount = models.PositiveIntegerField()


class Item(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    stock = models.PositiveIntegerField()
    sales_price = models.FloatField()

    class Meta:
        unique_together = ['sales_price', 'name']

    def __str__(self):
        return f'{self.name}'
    
    def is_in_stock(self):
        if self.stock > 0:
            return True
        else:
            return False

class PurchaseItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    name = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    non_discount_price = models.FloatField()
    purchase_price = models.FloatField()
    stock = models.PositiveIntegerField()
    DISCOUNT = (
        ('PERCENT', "percent"),
        ('fixed', 'fixed')
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='PERCENT')

    discount = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.item}'

class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Placement(models.Model):
    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE)
    placed_on = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    qunatity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.purchase_item} on {self.placed_on}'


# @receiver(models.signals.post_save, sender=PurchaseItem)
# def placement_creator(sender, instance, created, *args, **kwargs):
#     print('triggered')
#     if created:
#         print('created')
#         try:
#             place = Place.objects.get(name='Unassigned')
#         except:
#             place = Place.objects.create(name='Unassigned')
#         placement = Placement.objects.create(purchase_item=instance, placed_on=place, qunatity=instance.stock)
#         placement.save()
#         item_s = Item.objects.get(id=instance.item)
#         item_s = instance.stock + item_s.stock
#         item_s.save()
