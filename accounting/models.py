from django.db import models
from user_handler.models import Customer, Vendor
import uuid 
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import datetime
from inventory.models import PurchaseOrder
from payment.models import Payment, PaymentMethod
from django.db.models import signals
import django
from user_handler.models import Customer, Vendor

class AccountType(models.Model):
    name = models.CharField(max_length=255)
    HEADER_CHOICE = (
        ('assets', 'Assets'),
        ('expense', 'Expense'),
        ('draw', 'Draw'),
        ('liabilities', 'Liabilities'),
        ('revenue', 'Revenue'),
        ('equity', 'Equity')
    )
    header = models.CharField(max_length=20, choices=HEADER_CHOICE, default='assets')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.header}'

class Account(models.Model):
    uuid = models.UUIDField(unique=True,default= uuid.uuid4)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    opening_balance = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0, blank=True, null=True)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField(blank=True, null=True)
    current_amount = models.FloatField(default=0)

    parent = models.ForeignKey('Account', on_delete=models.SET_NULL, blank=True, null=True, related_name='childs')

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.current_amount}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.current_amount = self.opening_balance
        if self.customer and self.vendor:
            raise Exception("Same Account cannot be use by both customer and vendor.")
        super(Account, self).save(*args, **kwargs)


class LedgerEntry(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    date = models.DateField(default=django.utils.timezone.now)
    is_add = models.BooleanField(default=True)

    bundle_id = models.CharField(max_length=50, blank=True, null=True)                             # To keep track of bundled transactions

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.account} {self.payment}'
    
    def save(self, *args, **kwargs):
        if self.id:
            raise Exception("Cannot update ledger entry.")
        super(LedgerEntry, self).save(*args, **kwargs) 
    
    class Meta:
        unique_together = ['account', 'is_add', 'payment']

@receiver(models.signals.post_save, sender=LedgerEntry)
def ledger_entry_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.is_add:
            instance.account.current_amount += instance.payment.amount
        else:
            instance.account.current_amount -= instance.payment.amount
        instance.account.save()

@receiver(pre_save, sender=LedgerEntry)
def ledger_entry_pre_save(sender, instance, *args, **kwargs):
    if not instance.account.is_active or instance.account.is_closed:
        raise Exception("You Cannot Use Closed Accounts For Transactions.")


class MonthlyStats(models.Model):
    total_assets = models.FloatField(default=0)
    total_liabilities = models.FloatField(default=0)
    total_revenue = models.FloatField(default=0)
    total_expense = models.FloatField(default=0)
    total_draw = models.FloatField(default=0)
    total_equity = models.FloatField(default=0)

    profit = models.FloatField(default=0)
    date = models.DateTimeField(default=0)

    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(pre_save, sender=MonthlyStats)
def monthly_stats_post_save_handler(sender, instance, *args, **kwargs):
    if not instance.id:
        stat = MonthlyStats.objects.filter(date__year=instance.date.year).filter(date__month=instance.date.month)
        if len(stat) > 0:
            raise Exception("Duplicate montly stats.")
    instance.profit = instance.total_revenue - instance.total_expense


def get_stat(date):
    monthly = MonthlyStats.objects.filter(date__year=date.year).filter(date__month=date.month)
    if len(monthly) > 0:
        return monthly[0]
    else:
        monthly = MonthlyStats.objects.create(date=date)
        return monthly


@receiver(models.signals.post_save, sender=LedgerEntry)
def update_monthly_stat_entry_post_save(sender, instance, created, **kwargs):
    if created:
        stat = get_stat(instance.date)
        if instance.account.account_type.header == "assets":
            stat.total_assets += instance.payment.amount        
        elif instance.account.account_type.header == "liabilities":
            stat.total_liabilities += instance.payment.amount
        elif instance.account.account_type.header == "revenue":
            stat.total_revenue += instance.payment.amount
        elif instance.account.account_type.header == "expense":
            stat.total_expense += instance.payment.amount
        elif instance.account.account_type.header == "draw":
            stat.total_draw += instance.payment.amount
        elif instance.account.account_type.header == "equity":
            stat.total_equity += instance.payment.amount
        stat.save()            


# while purchase default expense 
# and another to account
# in system  ... while purchase ->  sub/add from -> account

#if action == True ; it means add, if false is sub.
class AccountingSettings(models.Model):
    default_purchase_account_on_cash = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='purchase_account_on_cash')
    default_purchase_action_on_cash_is_add = models.BooleanField(default=True)

    default_purchase_account_on_credit = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='purchase_account_on_credit')
    default_purchase_action_on_credit_is_add = models.BooleanField(default=True)

    default_purchase_account_on_bank = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='purchase_account_on_bank')
    default_purchase_action_on_bank_is_add = models.BooleanField(default=True)

    default_purchase_account_on_transfer = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='purchase_account_on_transfer')
    default_purchase_action_on_transfer_is_add = models.BooleanField(default=True)

    default_purchase_account_on_pre_paid = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='purchase_account_on_pre_paid')
    default_purchase_action_on_pre_paid_is_add = models.BooleanField(default=True)

    default_invoice_account_on_cash = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='invoice_account_on_cash')
    default_invoice_action_on_cash_is_add = models.BooleanField(default=True)

    default_invoice_account_on_credit = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='invoice_account_on_credit')
    default_invoice_action_on_credit_is_add = models.BooleanField(default=True)

    default_invoice_account_on_bank = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='invoice_account_on_bank')
    default_invoice_action_on_bank_is_add = models.BooleanField(default=True)

    default_invoice_account_on_transfer = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='invoice_account_on_transfer')
    default_invoice_action_on_transfer_is_add = models.BooleanField(default=True)

    default_invoice_account_on_pre_paid = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='invoice_account_on_pre_paid')
    default_invoice_action_on_pre_paid_is_add = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk and AccountingSettings.objects.exists():
            raise Exception('There is can be only one AccountingSettings instance')
        return super(AccountingSettings, self).save(*args, **kwargs)


class FreeEntryLedger(models.Model):
    entry_for = models.ForeignKey(LedgerEntry, on_delete=models.CASCADE)
    amount = models.FloatField()
    remarks = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.entry_for}'
    
    def save(self, *args, **kwargs):
        if self.id:
            raise Exception("Cannot update ledger entry.")
        super(FreeEntryLedger, self).save(*args, **kwargs) 

@receiver(models.signals.post_save, sender=FreeEntryLedger)
def free_ledger_entry_post_save(sender, instance, created, **kwargs):
    if created:
        #updating account
        if instance.entry_for.is_add:
            instance.entry_for.account.current_amount += instance.amount
        else:
            instance.entry_for.account.current_amount -= instance.amount
        instance.entry_for.account.save()

        #updating monthly stats


#all customers has revenue heading/all vendor is under expense heading
# let customer/vendor choose account during payment

# @receiver(models.signals.post_save, sender=Payment)
# def payment_to_account_handler(sender, instance, created, **kwargs):
#     if created:
#         if instance.purchase_order:
#             if instance.method.header == "credit":
#                 temp = LedgerEntry.objects.create(
#                     payment = instance,
#                     account = ,
#                     remarks = "automated entry, PO, "+instance.purchase_order.uuid
#                     date = django.utils.timezone.now,
#                     is_add = 
#                     bundle_id
#                 )


# call this from views
def payemnt_entry_to_system(account, payment):
    print("payment to system")
    settings = AccountingSettings.objects.filter(is_active=True)
    if len(settings) > 0:
        raise Exception("No Active Account Setting Defined. Please configure the account setting before using it.")
    settings = settings[0]
    if payment.invoice:
        entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = account,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add = True
        )
        if payment.method.header == 'credit':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_invoice_account_on_credit,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add = settings.default_invoice_action_on_credit_is_add
        )
        elif payment.method.header == 'cash':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_invoice_account_on_cash,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_invoice_action_on_credit_is_add
        )
        elif payment.method.header == 'pre_paid':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_invoice_account_on_pre_paid,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_invoice_action_on_credit_is_add
        )
        elif payment.method.header == 'transfer':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_invoice_account_on_transfer,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_invoice_action_on_credit_is_add
        )
        elif payment.method.header == 'credit':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_invoice_account_on_bank,
            remarks = 'automated entry invoice '+str(payment.invoice.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_invoice_action_on_credit_is_add
        )
    
    elif payment.purchase_order:
        entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = account,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add = True
        )
        if payment.method.header == 'credit':
            entry_two = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_purchase_account_on_credit,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add = settings.default_purchase_action_on_credit_is_add
        )
        elif payment.method.header == 'cash':
            entry_two = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_purchase_account_on_cash,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_purchase_action_on_credit_is_add
        )
        elif payment.method.header == 'pre_paid':
            entry_two = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_purchase_account_on_pre_paid,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_purchase_action_on_credit_is_add
        )
        elif payment.method.header == 'transfer':
            entry_two = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_purchase_account_on_transfer,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_purchase_action_on_credit_is_add
        )
        elif payment.method.header == 'credit':
            entry_one = LedgerEntry.objects.create(
            payment = payment,
            account = settings.default_purchase_account_on_bank,
            remarks = 'automated entry purchase order'+str(payment.purchase_order.uuid),
            date = django.utils.timezone.now(),
            is_add =  settings.default_purchase_action_on_credit_is_add
        )



# assets , lib, equity, draw , exp, rev 
# exp - rev = profit/loss
# 