from django.db import models
from user_handler.models import Customer, Vendor
import uuid 

class EntryType(models.Model):
    name = models.CharField(max_length=255)

    HEADER_CHOICE = (
        ('assets', 'Assets'),
        ('liabilities', 'Liabilities'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
        ('draw', 'Draw'),
        ('equity', 'Equity'),
    )
    header = models.CharField(max_length=20, choices=HEADER_CHOICE, default='income')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.header}'

class Account(models.Model):
    uuid = models.UUIDField(unique=True,default= uuid.uuid4)
    name = models.CharField(max_length=255)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, blank=True, null=True)
    opening_balance = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0, blank=True, null=True)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField(blank=True, null=True)
    due = models.FloatField(default=0)
    credit = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class LedgerEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    header = models.ForeignKey(EntryType, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    amount = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.account} {self.date}'

class MonthlyStats(models.Model):
    total_assets = models.FloatField()
    total_liabilities = models.FloatField()
    total_revenue = models.FloatField(default=0)
    total_expense = models.FloatField(default=0)
    total_draw = models.FloatField(default=0)
    total_equity = models.FloatField(default=0)

    profit = models.FloatField(default=0)
    to_be_paid = models.FloatField(default=0)
    to_pay = models.FloatField(default=0)
    date = models.DateTimeField(default=0)


class AccountingSettings(models.Model):
    default_purchase_order_entry_type_on_dr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='purchase_order_default_entries_dr')
    default_sales_entry_type_on_dr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='sales_default_entries_dr')

    default_purchase_order_entry_type_on_cr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='purchase_order_default_entries_cr')
    default_sales_entry_type_on_cr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='sales_default_entries_cr')

    default_purchase_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_purchases')

    default_sales = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_sales')

    def save(self, *args, **kwargs):
        if not self.pk and AccountingSettings.objects.exists():
        # if you'll not check for self.pk 
        # then error will also raised in update of exists model
            raise Exception('There is can be only one AccountingSettings instance')
        return super(AccountingSettings, self).save(*args, **kwargs)


class DefaultLedgerEntry(models.Model):
    from payment.models import PaymentMethod

    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE)
    entry_type_on_cr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='default_cr')
    entry_type_on_dr = models.ForeignKey(EntryType, on_delete=models.CASCADE, related_name='default_dr')

