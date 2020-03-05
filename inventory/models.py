from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
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
    discount = models.PositiveIntegerField(default=0)
    STATUS_S = (
        ('DRAFT', "Draft"),
        ('SENT', "Sent"),
        ('DUE', "Due"),
        ('PAID', "Paid"),
        ('DELIVERED','Delivered'),
        ('COMPLETED', 'complete')
    )
    status = models.CharField(max_length=10, choices=STATUS_S, default='DRAFT')


class ItemCatagory(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    catagory = models.ForeignKey(ItemCatagory, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sales_price = models.FloatField()
    sold = models.PositiveIntegerField(default=0)

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
    quantity = models.PositiveIntegerField(default=0)
    non_discount_price = models.FloatField(default=0)
    sold = models.PositiveIntegerField(default=0)
    purchase_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    defective = models.PositiveIntegerField(default=0)
    DISCOUNT = (
        ('PERCENT', "percent"),
        ('fixed', 'fixed')
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='PERCENT')
    discount = models.PositiveIntegerField(default=0)
    STATUS_S = (
        ('delivered','Delivered'),
        ('incomplete', 'Incomplete'),
        ('addedtocirculation', 'Added To Circulation')
    )
    status = models.CharField(max_length=25, choices=STATUS_S, default='INCOMPLETE')
    
    def __str__(self):
        return f'{self.item}'


class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Placement(models.Model):
    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE)
    placed_on = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    qunatity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.purchase_item} on {self.placed_on}'


@receiver(models.signals.pre_save, sender=PurchaseItem)
def pre_save_handler(sender, instance, *args, **kwargs):
    if (instance.quantity < instance.defective):
        raise Exception("Number of defective items are greater than the quntity of the purchase item ")
    instance.stock = instance.quantity - instance.defective    
    if instance.id is not None:
        p_item = PurchaseItem.objects.get(id=instance.id)
        old_status = p_item.status
        old_sold = p_item.sold
    else:
        old_status = ""
        old_sold = 0
    if str(old_status).lower() == str(instance.status).lower() == "addedtocirculation" :
        raise Exception("Cannot edit Purchase's item descriptions when it's in cirulation.")
    if str(instance.status).lower() != str(old_status).lower():
        if str(instance.status).lower() == "addedtocirculation":
            instance.item.stock = instance.item.stock + instance.stock
            instance.item.save()
        if str(old_status).lower() == "addedtocirculation"  and str(instance.status).lower() != str(old_status).lower():
            instance.item.stock = instance.item.stock - instance.stock
            instance.item.save()
    if old_sold != instance.sold:
        raise Exception('Cannot edit already sold items.')