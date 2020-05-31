from django.contrib import admin
from .models import LedgerEntry, Account, EntryType, MonthlyStats, DefaultLedgerEntry, AccountingSettings, AccountType

admin.site.register(LedgerEntry)
admin.site.register(Account)
admin.site.register(EntryType)
admin.site.register(MonthlyStats)
admin.site.register(AccountType)
admin.site.register(AccountingSettings)
admin.site.register(DefaultLedgerEntry)