from .views_collection.accounts import get_multiple_accounts, add_new_account, get_account_details, delete_accounts, update_account, get_transactions
from .views_collection.types_curd import get_multiple_account_types
from .views_collection.ledger_entries import get_multiple_ledger_entries, add_new_ledger_entry, get_ledger_entry_details, update_ledger_entry
from .views_collection.report_generation import generate_profit_loss_statement, generate_balance_sheet_statement


import json
from django.http import JsonResponse
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from .models import MonthlyStats
from inventory.utils import str_to_datetime
from user_handler.permission_check import bind, check_permission

@require_http_methods(['POST'])
@bind
def dashboard_report(self,request):
    response_json = {'status':False}        
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        try:
            response_json['summary'] = {
                'profit' : 0,
                'revenue' : 0,
                'expense' : 0
            }
            if data_json['action'] == "get":
                stats = MonthlyStats.objects.filter()
                if data_json['filters']['date']:
                    if data_json['filters']['date']['from']:
                        stats = stats.filter(created_at__gte = str_to_datetime(data_json['filters']['date']['from']))
                    if data_json['filters']['date']['upto']:
                        stats = stats.filter(created_at__lte = str_to_datetime(data_json['filters']['date']['upto']))
                for stat in stats:
                    response_json['summary']['profit'] = response_json['summary']['profit'] + stat.profit
                    response_json['summary']['revenue'] = response_json['summary']['revenue'] + stat.total_revenue
                    response_json['summary']['expense'] = response_json['summary']['expense'] + stat.total_expense
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

