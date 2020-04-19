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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'
    

class PurchaseOrder(models.Model):
    uuid = models.UUIDField(unique=True,default= uuid.uuid4)
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

    def save(self, *args, **kwargs):
        self.total_cost = 0
        for item in self.items.filter(is_active=True):
            self.total_cost = self.total_cost + item.purchase_price*(item.quantity)
        super(PurchaseOrder, self).save(*args, **kwargs)


@receiver(models.signals.post_save, sender=PurchaseOrder)
def post_save_handler_purchase_order(sender, instance, *args, **kwargs):
    instance.total_cost = 0
    if instance.status.is_end == True:
        for item in instance.items.filter(is_active=True):
            item.status = "addedtocirculation"
            item.save()


class ItemCatagory(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    catagory = models.ForeignKey(ItemCatagory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    stock = models.PositiveIntegerField(default=0)
    sales_price = models.FloatField()
    sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} {self.sales_price}'
    
    def is_in_stock(self):
        if self.stock > 0:
            return True
        else:
            return False
    
    class Meta:
        unique_together = ['name', 'catagory', 'sales_price']


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



class Place(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'



class Placement(models.Model):
    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE, related_name='items_places')
    placed_on = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, related_name='placements')
    stock = models.PositiveIntegerField(default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_placements', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.purchase_item} on {self.placed_on}'
    
    class Meta:
        unique_together = ('purchase_item', 'placed_on')
    
    def save(self, *args, **kwargs):
        self.item = self.purchase_item.item
        super(Placement, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        p_i = self.purchase_item
        place =Place.objects.get(is_default=True)
        stock = self.stock
        super(Placement, self).delete(*args, **kwargs)
        new_placement = Placement.objects.create(purchase_item=p_i, stock=stock, placed_on=place)
        new_placement.save()
        


@receiver(pre_save, sender=Place)
def place_pre_save_handler(sender, instance, *args, **kwargs):
    if instance.id:
        if (instance.is_default) and instance.id != Place.objects.get(is_default=True).id:
            if len(Place.objects.filter(is_default=True))>=1:
                raise Exception("Default place for unassigned items already exsists.")
    else:
        if (instance.is_default):
            if len(Place.objects.filter(is_default=True))>=1:
                raise Exception("Default place for unassigned items already exsists.")


@receiver(pre_save, sender=Placement)
def placement_pre_save_handler(sender, instance, *args, **kwargs):
    if instance.id:
        if (instance.placed_on.is_default):
            print("sad")
            print(instance)
            if instance.stock > instance.purchase_item.stock:
                print(instance.stock,  instance.purchase_item.stock)
                raise Exception('Total placed stocked of this item is greater than the purchased item stock.')
        else:
            print("triggered")
            place = Place.objects.get(is_default=True)
            unassigned = Placement.objects.get(purchase_item=instance.purchase_item, placed_on = place)
            if instance.stock > unassigned.stock:
                raise Exception('More stock is assiged than there is unassigned stock')
            print("triggered")
            unassigned.stock = unassigned.stock - instance.stock
            unassigned.save()
        

    if instance.id is None:
        if (instance.placed_on.is_default):
            if instance.stock > instance.purchase_item.stock:
                raise Exception('Total placed stocked of this item is greater than the purchased item stock.')
        else:
            place = Place.objects.get(is_default=True)
            try:
                unassigned = Placement.objects.get(purchase_item=instance.purchase_item, placed_on = place)
            except:
                raise Exception("There are no items(of this particular purchase order) on the default place.")
            if instance.stock > unassigned.stock:
                raise Exception('You are trying to assign more stock to the place than there is. Error instance.stock < unassigned.stock ')
            unassigned.stock = unassigned.stock - instance.stock
            unassigned.save()

@receiver(models.signals.pre_save, sender=PurchaseItem)
def pre_save_handler(sender, instance, *args, **kwargs):
    if (instance.quantity < instance.defective):
        raise Exception("Number of defective items are greater than the quntity of the purchase item ")
    print(instance.stock, instance.quantity, instance.defective, instance.sold)
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
        place = Place.objects.get(is_default=True)
    except:
        place = Place.objects.create(is_default=True, name='Default')
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
