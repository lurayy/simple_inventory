from django.db import models
from inventory.models import  PurchaseItem, Place, Item, Placement
from user_handler.models import Customer, CustomUserBase, Tax, Discount
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import signals
import uuid 

class InvoiceStatus(models.Model):
    name = models.CharField(max_length=255)
    is_sold  = models.BooleanField(default=False)

class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(CustomUserBase, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    invoiced_on = models.DateTimeField()
    due_on = models.DateTimeField()
    order_number = models.UUIDField(unique=True,default= uuid.uuid4)
    
    total_amount = models.FloatField()
    paid_amount = models.FloatField()
    tax_total = models.PositiveIntegerField()
    discount_total = models.PositiveIntegerField(default=0)
    additional_discount = models.PositiveIntegerField(default=0)

    status = models.ForeignKey(InvoiceStatus, on_delete=models.SET_NULL, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.customer} {self.order_number}'

    def save(self, *args, **kwargs):
        self.total_amount = round(self.total_amount, 2)
        self.paid_amount = round(self.paid_amount, 2)
        super(Invoice, self).save(*args, **kwargs)



class InvoiceItem(models.Model):
    ''' this model hold the items and the details of that item, that are add to invoice'''
    purchase_item = models.ForeignKey(PurchaseItem, on_delete = models.SET_NULL, null=True)
    item  = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    sold_from = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.PositiveIntegerField(default=1)
    
    price = models.FloatField()

    tax_total = models.FloatField(blank=True, null=True)

    sub_total = models.FloatField(blank=True, null=True)

    discount_amount = models.FloatField(blank=True, null=True)

    total_without_discount  = models.FloatField(blank=True, null=True)

    total = models.FloatField(blank=True, null=True)
    
    discount = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)


@receiver(post_save, sender=InvoiceItem)
def post_save_handler(sender, created, instance, **kwargs):
    instance.tax_total = 0
    instance.sub_total = 0
    instance.discount_amount = 0
    instance.total = 0
    applied_taxex = instance.taxes.all().filter(is_active=True)
    for tax in applied_taxex:
        if tax.tax_type == 'fixed':
            instance.tax_total = instance.tax_total + (tax.rate) * instance.quantity
        else:
            instance.tax_total = instance.tax_total + (instance.price*tax.rate*instance.quantity)/100
    applied_discounts = instance.discount.all().filter(is_active=True)
    for discount in applied_discounts:
        if discount.discount_type == 'fixed':
            instance.discount_amount = instance.discount_amount + (discount.rate) * instance.quantity
        else:
            instance.discount_amount = instance.discount_amount + (instance.price*discount.rate*instance.quantity)/100
    instance.sub_total = instance.price*instance.quantity
    instance.total_without_discount = instance.sub_total+instance.tax_total
    instance.total = instance.total_without_discount - instance.discount_amount
    signals.post_save.disconnect(post_save_handler, sender=InvoiceItem)
    instance.save()
    signals.post_save.connect(post_save_handler, sender=InvoiceItem)



@receiver(pre_save, sender=Invoice)
def tranction_handler(sender, instance, **kwargs):
    if instance.id is None:
        if instance.status.is_sold==True:
            sales_sub(instance)
    else:
        old_status = Invoice.objects.get(id=instance.id).status
        if instance.status != old_status:
            if old_status.is_sold !=True: 
                if instance.status.is_sold == True:
                    print("sales done")
                    sales_sub(instance)
            if old_status.is_sold == True:
                if instance.status != True:
                    print("sales revert back")
                    sales_add(instance)
    instance.total_amount = 0
    instance.discount_total = 0
    instance.tax_total = 0
    for invoice_item in instance.invoice_items.all():
        instance.total_amount = instance.total_amount + invoice_item.total 
        instance.discount_total = instance.discount_total + invoice_item.discount_amount
        instance.tax_total = instance.tax_total + invoice_item.tax_total
    instance.paid_amount = instance.total_amount - instance.additional_discount


# @receiver(post_save, sender=InvoiceItem)
# def invoice_item_handler(sender, instance, **kwargs):
#     instance.tax_total = 0
#     calculate_tax(instance)
#     print(instance.tax_total)
#     print(instance.id)
#     instance.sub_total = instance.price*instance.quantity
#     instance.total = instance.sub_total+instance.tax_total
#     signals.post_save.disconnect(invoice_item_handler, sender=InvoiceItem)
#     instance.save()
#     signals.post_save.connect(invoice_item_handler, sender=InvoiceItem)



def sales_sub(invoice):
    for item in invoice.invoice_items.filter():
        if item.purchase_item.stock < item.quantity:
            raise Exception(f'{item.item}\" quantity is greater than it\"s avaible stock.')
        item.purchase_item.stock = item.purchase_item.stock - item.quantity
        item.purchase_item.sold = item.purchase_item.sold + item.quantity
        item.purchase_item.save()
        item.item.stock = item.item.stock - item.quantity
        item.item.sold = item.item.sold + item.quantity
        item.item.save()
        sold_from = Placement.objects.get(placed_on=item.sold_from, purchase_item=item.purchase_item)
        sold_from.stock = sold_from.stock - item.quantity
        sold_from.save()


def sales_add(invoice):
    for item in invoice.invoice_items.filter():
        item.purchase_item.stock = item.purchase_item.stock + item.quantity
        item.purchase_item.sold = item.purchase_item.sold - item.quantity
        item.purchase_item.save()
        item.item.stock = item.item.stock + item.quantity
        item.item.sold = item.item.sold - item.quantity
        item.item.save()
        place = Place.objects.get(name='unassigned')
        sold_from = Placement.objects.get(placed_on=place, purchase_item=item.purchase_item)
        sold_from.stock = sold_from.stock + item.quantity
        sold_from.save()
        item.sold_from = place
        item.save()
