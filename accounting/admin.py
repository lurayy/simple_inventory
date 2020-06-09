from django.contrib import admin
from .models import LedgerEntry, Account, EntryType, MonthlyStats, DefaultEntryType, AccountType, FreeEntryLedger

admin.site.register(LedgerEntry)
admin.site.register(Account)
admin.site.register(EntryType)
admin.site.register(MonthlyStats)
admin.site.register(AccountType)
admin.site.register(DefaultEntryType)
admin.site.register(FreeEntryLedger)