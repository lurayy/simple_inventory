from django.db import models
from inventory.models import  PurchaseItem, Place, Item
from user_handler.models import Customer, CustomUserBase



class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(CustomUserBase, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    # currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    # used_currency_rate = models.FloatField()

    invoiced_on = models.DateTimeField()
    due_on = models.DateTimeField()
    order_number = models.BigIntegerField()
    notes = models.TextField()
    footer = models.TextField()

    paid_amount = models.FloatField()
    
    STATUS_S = (
        ('DRAFT', "Draft"),
        ('SENT', "Sent"),
        ('DUE', "Due"),
        ('PAID', "Paid")
    )
    status = models.CharField(max_length=10, choices=STATUS_S, default='DRAFT')
    #catagory for the invoice ??? 

    def __str__(self):
        return str(self.customer)


class InvoiceItem(models.Model):
    ''' this model hold the items and the details of that item, that are add to invoice'''
    purchase_item = models.ForeignKey(PurchaseItem, on_delete = models.SET_NULL, null=True)
    item  = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    sold_from = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
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