from django.contrib import admin
from .models import LedgerEntry, Account,  MonthlyStats, AccountingSettings, AccountType, FreeEntryLedger

admin.site.register(LedgerEntry)
admin.site.register(Account)
admin.site.register(MonthlyStats)
admin.site.register(AccountType)
admin.site.register(AccountingSettings)
admin.site.register(FreeEntryLedger)