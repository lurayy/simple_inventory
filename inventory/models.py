from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from user_handler.models import CustomUserBase, Vendor, Tax, Discount 
from django.db.models import Q

class PurchaseOrderStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    

class PurchaseOrder(models.Model):
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    invoiced_on = models.DateTimeField()
    completed_on = models.DateTimeField(null=True, blank=True) 
    total_cost = models.FloatField()

    DISCOUNT = (
        ('percent', "percent"),
        ('fixed', "fixed")
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='percent')
    discount = models.PositiveIntegerField(default=0)
    status = models.ForeignKey(PurchaseOrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)


@receiver(models.signals.post_save, sender=PurchaseOrder)
def post_save_handler_purchase_order(sender, instance, *args, **kwargs):
    if instance.status.is_end == True:
        for item in instance.items.filter(is_active=True):
            item.status = "addedtocirculation"
            item.save()
        


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
    
    class Meta:
        unique_together = ('name', 'catagory', 'sales_price')


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
        ('percent', "Percent"),
        ('fixed', 'Fixed')
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='percent')
    discount = models.PositiveIntegerField(default=0)
    STATUS_S = (
        ('delivered','Delivered'),
        ('incomplete', 'Incomplete'),
        ('addedtocirculation', 'Added To Circulation')
    )
    status = models.CharField(max_length=25, choices=STATUS_S, default='incomplete')

    is_active = models.BooleanField(default=True)    
    def __str__(self):
        return f'{self.item} of {self.purchase_order}'


# @receiver(pre_save, sender=Invoice)
# def tranction_handler(sender, instance, created, **kwargs):



class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Placement(models.Model):
    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE, related_name='items_places')
    placed_on = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.purchase_item} on {self.placed_on}'
    
    class Meta:
        unique_together = ('purchase_item', 'placed_on')
    

@receiver(pre_save, sender=Placement)
def placement_pre_save_handler(sender, instance, *args, **kwargs):
    if instance.id:
        if str(instance.placed_on) == "unassigned":
            print("sad")
            print(instance)
            if instance.stock > instance.purchase_item.stock:
                print(instance.stock,  instance.purchase_item.stock)
                raise Exception('Total placed stocked of this item is greater than the purchased item stock.')
        else:
            print("triggered")
            place = Place.objects.get(name = "unassigned")
            unassigned = Placement.objects.get(purchase_item=instance.purchase_item, placed_on = place)
            if instance.stock > unassigned.stock:
                raise Exception('More stock is assiged than there is unassigned stock')
            print("triggered")
            unassigned.stock = unassigned.stock - instance.stock
            unassigned.save()
        

    if instance.id is None:
        if str(instance.placed_on) == 'unassigned':
            if instance.stock > instance.purchase_item.stock:
                raise Exception('Total placed stocked of this item is greater than the purchased item stock.')
        else:
            place = Place.objects.get(name = "unassigned")
            unassigned = Placement.objects.get(purchase_item=instance.purchase_item, placed_on = place)
            if instance.stock > unassigned.stock:
                raise Exception('You are trying to assign more stock to the place than there is. Error instance.stock < unassigned.stock ')
            unassigned.stock = unassigned.stock - instance.stock
            unassigned.save()

@receiver(models.signals.pre_save, sender=PurchaseItem)
def pre_save_handler(sender, instance, *args, **kwargs):
    if (instance.quantity < instance.defective):
        raise Exception("Number of defective items are greater than the quntity of the purchase item ")
    instance.stock = instance.quantity - instance.defective - instance.sold
    if instance.id is not None:
        p_item = PurchaseItem.objects.get(id=instance.id)
        old_status = p_item.status
        old_sold = p_item.sold
    else:
        old_status = ""
        old_sold = 0
    
    # if str(old_status).lower() == str(instance.status).lower() == "addedtocirculation" :
    #     raise Exception("Cannot edit Purchase's item descriptions when it's in cirulation.")
    if instance.quantity != instance.sold + instance.stock + instance.defective:
        print(instance.quantity, instance.sold, instance.stock, instance.defective)
        raise Exception('Items sold, defective and in stock doesnot add up to total quantity of the purchase item.')
    # if old_sold != instance.sold:
    #     raise Exception('Cannot edit already sold items.')
    if str(instance.status).lower() != str(old_status).lower():
        if str(instance.status).lower() == "addedtocirculation":
            instance.item.stock = instance.item.stock + instance.stock
            instance.item.save()
        if str(instance.status).lower() != "addedtocirculation"  and str(old_status).lower() == "addedtocirculation":
            instance.item.stock = instance.item.stock - instance.stock
            instance.item.save()
            for placement in instance.items_places.all():
                placement.delete()    

@receiver(post_save, sender=PurchaseItem)
def post_save_handler(sender, instance, created, **kwargs):
    try:
        place = Place.objects.get(name='unassigned')
    except:
        place = Place.objects.create(name='unassigned')
        place.save()
    if instance.status == "addedtocirculation":
        try:
            placement = Placement.objects.get(purchase_item=instance, placed_on=place)
        except:
            placement = Placement.objects.create(purchase_item=instance, placed_on=place, stock=0)
            placement.save()
            placement.stock = placement.stock + instance.stock
            print(placement.stock, instance.stock)
            placement.save()
