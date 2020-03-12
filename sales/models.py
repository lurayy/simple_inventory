from django.db import models
from inventory.models import  PurchaseItem, Place, Item, Placement
from user_handler.models import Customer, CustomUserBase, Tax, Discount
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import signals


class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(CustomUserBase, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    invoiced_on = models.DateTimeField()
    due_on = models.DateTimeField()
    order_number = models.BigIntegerField()
    
    paid_amount = models.FloatField()
    
    tax_total = models.PositiveIntegerField()

    STATUS_S = (
        ('sent', "Sent"),
        ('due', "Due"),
        ('paid', "Paid"),
        ('completed', 'Completed'),
        ('shiped','Shiped')
    )
    status = models.CharField(max_length=10, choices=STATUS_S, default='COMPLETED')
    is_active = models.BooleanField(default=True)
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

    tax_total = models.FloatField(blank=True)

    sub_total = models.FloatField(blank=True)

    discount_amount = models.FloatField(blank=True)

    total_without_discount  = models.FloatField(blank=True)

    total = models.FloatField(blank=True)
    
    discount = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        if self.id is None:
            super(InvoiceItem, self).save(*args, **kwargs)
        #reseting values
        self.tax_total = 0
        self.sub_total = 0
        self.discount_amount = 0
        self.total = 0

        applied_taxex = self.taxes.all().filter(is_active=True)
        for tax in applied_taxex:
            if tax.tax_type == 'fixed':
                self.tax_total = self.tax_total + (tax.rate) * self.quantity
            else:
                self.tax_total = self.tax_total + (self.price*tax.rate*self.quantity)/100
        applied_discounts = self.discount.all().filter(is_active=True)
        for discount in applied_discounts:
            if discount.discount_type == 'fixed':
                self.discount_amount = self.discount_amount + (discount.rate) * self.quantity
            else:
                self.discount_amount = self.discount_amount + (self.price*discount.rate*self.quantity)/100
        self.sub_total = self.price*self.quantity
        self.total_without_discount = self.sub_total+self.tax_total
        self.total = self.total_without_discount - self.discount_amount
        super(InvoiceItem, self).save(*args, **kwargs)


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
