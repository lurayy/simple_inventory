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
    header = models.CharField(max_length=20, choices=HEADER_CHOICE, default='assets')
    is_active = models.BooleanField(default=True)
    is_add = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.header} {self.is_add}'

    class Meta:
        unique_together = ['name', 'header', 'is_add']

class AccountType(models.Model):
    name = models.CharField(max_length=255)
    HEADER_CHOICE = (
        ('assets', 'Assets'),
        ('liabilities', 'Liabilities'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
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
    due = models.FloatField(default=0)
    credit = models.FloatField(default=0)

    parent = models.ForeignKey('Account', on_delete=models.SET_NULL, blank=True, null=True, related_name='childs')

    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.opening_balance}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if (self.opening_balance < 0):
                self.due = self.opening_balance
            else:
                self.credit = self.opening_balance
        super(Account, self).save(*args, **kwargs)



class LedgerEntry(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    entry_type = models.ForeignKey(EntryType, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    date = models.DateField(default=django.utils.timezone.now)

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
        unique_together = ['account', 'entry_type', 'payment']


@receiver(models.signals.post_save, sender=LedgerEntry)
def ledger_entry_post_save(sender, instance, created, **kwargs):
    if created:
        #updating account
        if instance.entry_type.is_add:
            instance.account.credit = instance.account.credit + instance.payment.amount
        else:
            temp = instance.account.credit - instance.payment.amount
            if temp < 0:
                instance.account.due = instance.account.due - temp * -1
            else:
                instance.account.credit = temp
        instance.account.save()

        #updating monthly stats
        try:
            stat = MonthlyStats.objects.filter(date__year = instance.date.year).filter(date__year = instance.date.month)
            stat = stat[0]
        except:
            stat = MonthlyStats.objects.create(
                date = instance.date
            )
        if instance.entry_type.is_add:
            if instance.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets + instance.payment.amount
            elif instance.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities + instance.payment.amount
            elif instance.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue  + instance.payment.amount
            elif instance.entry_type.header == "expense":
                stat.total_expense = stat.total_expense + instance.payment.amount
            elif instance.entry_type.header == "draw":
                stat.total_draw = stat.total_draw + instance.payment.amount
            elif instance.entry_type.header == "equity":
                stat.total_equity = stat.total_equity + instance.payment.amount
        else: 
            if instance.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets - instance.payment.amount
            elif instance.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities - instance.payment.amount
            elif instance.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue - instance.payment.amount
            elif instance.entry_type.header == "expense":
                stat.total_expense = stat.total_expense - instance.payment.amount
            elif instance.entry_type.header == "draw":
                stat.total_draw = stat.total_draw - instance.payment.amount
            elif instance.entry_type.header == "equity":
                stat.total_equity = stat.total_equity - instance.payment.amount
        stat.save()
    


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
    to_be_paid = models.FloatField(default=0)
    to_pay = models.FloatField(default=0)
    date = models.DateTimeField(default=0)

    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=MonthlyStats)
def monthly_stats_post_save_handler(sender, instance, *args, **kwargs):
    if not instance.id:
        stat = MonthlyStats.objects.filter(date__year = instance.date.year).filter(date__year = instance.date.month)
        if len(stat) > 0:
            raise Exception("Duplicate montly stats.")
    instance.profit = instance.total_revenue - instance.total_expense



class DefaultEntryType(models.Model):
    entry_type_for_credit_purchase_order_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_credits_cr')
    entry_type_for_pre_paid_purchase_order_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_pre_paid_cr')
    entry_type_for_cash_purchase_order_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_cash_cr')
    entry_type_for_transfer_purchase_order_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_transfer_cr')
    entry_type_for_bank_purchase_order_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_banks_cr')
    
    entry_type_for_credit_invoice_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_credits_cr')
    entry_type_for_pre_paid_invoice_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_invoice_cr')
    entry_type_for_cash_invoice_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_cash_cr')
    entry_type_for_transfer_invoice_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_transfer_cr')
    entry_type_for_bank_invoice_cr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_bank_cr')
   
    entry_type_for_credit_purchase_order_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_credits_dr')
    entry_type_for_pre_paid_purchase_order_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_pre_paid_dr')
    entry_type_for_cash_purchase_order_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_cash_dr')
    entry_type_for_transfer_purchase_order_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_transfer_dr')
    entry_type_for_bank_purchase_order_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_order_banks_dr')
    
    entry_type_for_credit_invoice_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_credits_dr')
    entry_type_for_pre_paid_invoice_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_invoice_dr')
    entry_type_for_cash_invoice_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_cash_dr')
    entry_type_for_transfer_invoice_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_transfer_dr')
    entry_type_for_bank_invoice_dr = models.ForeignKey(EntryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_bank_dr')

    default_purchase_account_on_cr = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_purchases_on_cr')
    default_sales_account_on_cr = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_sales_on_cr')

    default_purchase_account_on_dr = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_purchases_on_dr')
    default_sales_account_on_dr = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='default_sales_on_dr')


    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk and DefaultEntryType.objects.exists():
            raise Exception('There is can be only one AccountingSettings instance')
        return super(DefaultEntryType, self).save(*args, **kwargs)


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
        if instance.entry_for.entry_type.is_add:
            instance.entry_for.account.credit = instance.entry_for.account.credit + instance.amount
        else:
            temp = instance.entry_for.account.credit - instance.amount
            if temp < 0:
                instance.entry_for.account.due = instance.entry_for.account.due + temp * -1
            else:
                instance.entry_for.account.credit = temp
        instance.entry_for.account.save()

        #updating monthly stats
        try:
            stat = MonthlyStats.objects.filter(date__year = instance.entry_for.date.year).filter(date__year = instance.entry_for.date.month)
            stat = stat[0]
        except:
            stat = MonthlyStats.objects.create(
                date = instance.entry_for.date
            )

        if instance.entry_type.is_add:
            if instance.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets + instance.amount
            elif instance.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities + instance.amount
            elif instance.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue  + instance.amount
            elif instance.entry_type.header == "expense":
                stat.total_expense = stat.total_expense + instance.amount
            elif instance.entry_type.header == "draw":
                stat.total_draw = stat.total_draw + instance.amount
            elif instance.entry_type.header == "equity":
                stat.total_equity = stat.total_equity + instance.amount
        else:
            if instance.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets - instance.amount
            elif instance.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities - instance.amount
            elif instance.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue - instance.amount
            elif instance.entry_type.header == "expense":
                stat.total_expense = stat.total_expense - instance.amount
            elif instance.entry_type.header == "draw":
                stat.total_draw = stat.total_draw - instance.amount
            elif instance.entry_type.header == "equity":
                stat.total_equity = stat.total_equity - instance.amount
        stat.save()
    
    


@receiver(post_save, sender=Payment)
def handle_accounting_for_payment_post_save(sender, instance, created, **kwargs):
    settings = DefaultEntryType.objects.filter(is_active=True)[0]
    if created:
        signals.post_save.disconnect(handle_accounting_for_payment_post_save, sender=Payment)
        instance.save()
        signals.post_save.connect(handle_accounting_for_payment_post_save, sender=Payment)
        if instance.purchase_order or instance.invoice:
            invoice = True
            if instance.purchase_order:
                invoice = False
                if instance.invoice:
                    raise Exception("Both invoice and purchase order cann be assigned to same payment.")
            if instance.method.header == "credit":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account_on_cr,
                        entry_type = settings.entry_type_for_credit_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account_on_dr,
                        entry_type = settings.entry_type_for_credit_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_credit_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_credit_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "pre-paid":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_pre_paid_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_pre_paid_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_pre_paid_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_pre_paid_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "cash":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_cash_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_cash_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_cash_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_cash_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "transfer":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_transfer_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_transfer_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_transfer_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_transfer_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "bank":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_bank_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_bank_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_bank_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_bank_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )   



# For payment update
# @receiver(pre_save, sender=Payment)
# def pre_save_payment_handler(sender, instance, *args, **kwargs):
#     if instance.id:
#         old = Payment.objects.get(id=instance.id)
#         if instance.amount != old.amount:
#             amount  = instance.amount - old.amount
#             for entry in LedgerEntry.objects.filter(payment = instance):
#                 free = FreeEntryLedger.objects.create(
#                     entry_for = entry,
#                     amount = amount
#                 )


# @receiver(models.signals.post_save, sender=PurchaseOrder)
# def handle_accounting_post_save(sender, instance, created, **kwargs):
#     print("ledger entry")
#     print(instance.status.is_end)
#     if instance.status.is_end:
#         settings = AccountingSettings.objects.filter(is_active=True)[0]
#         date = django.utils.timezone.now()
#         remarks = str(instance.uuid) + str(date)
#         if instance.discount_type == "percent":
#             purchase_cost = instance.total_cost - instance.total_cost*0.01*instance.discount
#         else:
#             purchase_cost = instance.total_cost - instance.discount
#         x =  LedgerEntry.objects.filter(account = settings.default_purchase_account, entry_type = settings.default_purchase_order_entry_type_on_dr, remarks=remarks)
#         y = LedgerEntry.objects.filter(account = settings.default_purchase_account, entry_type = settings.default_purchase_order_entry_type_on_cr, remarks=remarks)
#         if len(x) < 0:
#             reverse_entries(x)
#         if len(y) < 0:
#             reverse_entries(x)
#         entry = LedgerEntry.objects.create(
#             account = settings.default_purchase_account,
#             entry_type = settings.default_purchase_order_entry_type_on_dr,
#             date = datetime.datetime.today(),
#             remarks = remarks,
#             amount = purchase_cost
#         )
#         print(entry)
#         entry2 = LedgerEntry.objects.create(
#             account = settings.default_purchase_account,
#             entry_type = settings.default_purchase_order_entry_type_on_cr,
#             remarks = remarks,
#             amount = purchase_cost,
#             date = datetime.datetime.today()
#         )
#         entry.save()
#         entry2.save()

def reverse_entries(entries):
    for entry in entries:
        remarks = "reverse_minus" + entry.remarks
        x = LedgerEntry.objects.create(
            accounnt = entry.account,
            entry_type = entry.entry_type,
            remarks = remarks,
            amount = -1*entry.amount,
            date = datetime.datetime.today()
        )
        x.save()
        entry.remarks = "reverse_plus" + entry.remarks
        entry.save()

# remarks 
# normal : uuid+ date
# revered : reverse_minus uuid + date
# one being reversed : reverse_plus uuid data
