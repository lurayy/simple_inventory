from django.db import models
from user_handler.models import Customer, Vendor
import uuid 

class EntryType(models.Model):
    name = models.CharField()

    HEADER_CHOICE = (
        ('assets', 'Assets'),
        ('liabilities', 'Liabilities'),
        ('income', 'Income'),
        ('expense', 'Expense')
    )

    header = models.CharField(max_length=20, choices=HEADER_CHOICE, default='income')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.hearder}'

class Account(models.Model):
    uuid = models.UUIDField(unique=True,default= uuid.uuid4)
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    opening_balance = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    due = models.FloatField()
    credit = models.FloatField()

    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class LedgerEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='entries')
    header = models.ForeignKey(EntryType, on_delete=models.SET_NULL, related_name='entries')
    remarks = models.TextField()
    date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

