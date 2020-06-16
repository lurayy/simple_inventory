from django.urls import path
from . import views

urlpatterns = [
   path('accounts/get', views.get_multiple_accounts),
   path('account/add', views.add_new_account),
   path('account/get', views.get_account_details),
   path('accounts/delete', views.delete_accounts),
   path('account/update', views.update_account),

   path('accounts/types/get', views.get_multiple_account_types),
   path('ledger/types/get', views.get_multiple_ledger_entry_types),
   path('ledger/entries/get', views.get_multiple_ledger_entries),
   path('ledger/entry/add', views.add_new_ledger_entry),
   path('ledger/entry/get', views.get_ledger_entry_details),

   path('reports/profitloss', views.generate_profit_loss_statement),
   path('reports/balancesheet', views.generate_balance_sheet_statement),
]