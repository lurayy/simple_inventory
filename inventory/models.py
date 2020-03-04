from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from user_handler.models import CustomUserBase, Vendor

class PurchaseOrder(models.Model):
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    invoiced_on = models.DateTimeField()
    completed_on = models.DateTimeField(null=True, blank=True) 
    total_cost = models.FloatField()

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
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
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
