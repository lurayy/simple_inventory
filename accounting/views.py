from .views_collection.accounts import get_multiple_accounts, add_new_account, get_account_details, delete_accounts, update_account, get_transactions
from .views_collection.types_curd import get_multiple_account_types
from .views_collection.ledger_entries import get_multiple_ledger_entries, add_new_ledger_entry, get_ledger_entry_details, update_ledger_entry
from .views_collection.report_generation import generate_profit_loss_statement, generate_balance_sheet_statement


import json
from django.http import JsonResponse
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods



# @require_http_methods(['POST'])
# @bind
# def dashboard_report(self,request):
#     response_json = {'status':False}
#     if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
#         response_json = {'status':False}
#         pass
