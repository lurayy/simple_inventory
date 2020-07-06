from django.contrib import admin
from .models import LedgerEntry, Account,  MonthlyStats, AccountingSettings, AccountType

admin.site.register(LedgerEntry)
admin.site.register(Account)
admin.site.register(MonthlyStats)
admin.site.register(AccountType)
admin.site.register(AccountingSettings)