from django.db import models
from inventory.models import  PurchaseItem, Place, Item, Placement
from user_handler.models import Customer, CustomUserBase
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save



class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(CustomUserBase, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    # currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    # used_currency_rate = models.FloatField()

    invoiced_on = models.DateTimeField()
    due_on = models.DateTimeField()
    order_number = models.BigIntegerField()
    paid_amount = models.FloatField()
    
    STATUS_S = (
        ('sent', "Sent"),
        ('due', "Due"),
        ('paid', "Paid"),
        ('completed', 'Completed'),
        ('shiped','Shiped')
    )
    status = models.CharField(max_length=10, choices=STATUS_S, default='COMPLETED')
    #catagory for the invoice ??? 

    def __str__(self):
        return str(self.customer)



class InvoiceItem(models.Model):
    ''' this model hold the items and the details of that item, that are add to invoice'''
    purchase_item = models.ForeignKey(PurchaseItem, on_delete = models.SET_NULL, null=True)
    item  = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    sold_from = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    tax_total = models.FloatField()
    sub_total = models.FloatField()
    total = models.FloatField()
    DISCOUNT = (
        ('PERCENT', "percent"),
        ('fixed', 'fixed')
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT, default='PERCENT')
    discount = models.PositiveIntegerField(default=0)

@receiver(pre_save, sender=Invoice)
def tranction_handler(sender, instance, **kwargs):
    if instance.id is None:
        if instance.status == "completed" or instance.status == "shiped":
            sales_sub(invoice)
    else:
        old_status = Invoice.objects.get(id=instance.id).status
        if instance.status != old_status:
            if old_status !="shiped" and  old_status != "completed": 
                if instance.status == "completed" or instance.status == "shiped":
                    print("sales done")
                    sales_sub(instance)
            if old_status == "completed" or old_status == "shiped":
                if instance.status != "completed" or instance.status != "shiped":
                    print("sales revert back")
                    sales_add(instance)



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
