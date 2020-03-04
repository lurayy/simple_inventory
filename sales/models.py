from django.db import models
from inventory.models import CustomUserBase, PurchaseItem
from user_handler.models import Customer



class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(CustomUserBase, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    # currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    # used_currency_rate = models.FloatField()

    invoiced_at = models.DateTimeField()
    due_at = models.DateTimeField()
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


class InvoiceItems(models.Model):
    ''' this model hold the items and the details of that item, that are add to invoice'''
    item = models.ForeignKey(PurchaseItem, on_delete = models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    # this will be item.sale_price, but can be changed if needed.
    price = models.FloatField()
    # add a way to distingush tax and it's price
    #The total price of taxes
    tax_total = models.FloatField()
    # will be calculated using self.price
    sub_total = models.FloatField()
    # sub_total+tax
    total = models.FloatField()