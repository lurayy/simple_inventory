from .views_collection.accounts import get_multiple_accounts, add_new_account, get_account_details, delete_accounts, update_account, get_transactions
from .views_collection.types_curd import get_multiple_account_types, add_account_types, delete_account_types, udpate_account_types
from .views_collection.ledger_entries import get_multiple_ledger_entries, add_new_ledger_entry, get_ledger_entry_details, update_ledger_entry
from .views_collection.report_generation import generate_profit_loss_statement, generate_balance_sheet_statement

import json
from django.http import JsonResponse
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from .models import MonthlyStats, AccountingSettings, Account
from inventory.utils import str_to_datetime
from user_handler.permission_check import bind, check_permission
import datetime
import dateutil.relativedelta
from .serializers import AccountingSettingsSerializer
from user_handler.models import log

@require_http_methods(['POST'])
@bind
def dashboard_report(self,request):
    response_json = {'status':False}        
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        try:
            if data_json['filters']['date']['start'] == None or data_json['filters']['date']['end'] == None:
                raise Exception("Both start and end date is requried.")
            response_json['summary'] = {
                'total_profit' : 0,
                'total_revenue' : 0,
                'total_expense' : 0,
                'data' : {}
            }
            if data_json['action'] == "get":
                stats = MonthlyStats.objects.filter()
                if data_json['filters']['date']:
                    if data_json['filters']['date']['start']:
                        stats = stats.filter(date__gte = str_to_datetime(data_json['filters']['date']['start']))
                    if data_json['filters']['date']['end']:
                        stats = stats.filter(date__lte = str_to_datetime(data_json['filters']['date']['end']))
                for stat in stats:
                    try:
                        old = stat.date - dateutil.relativedelta.relativedelta(months=1)
                        old_stat = MonthlyStats.objects.get( date__month = old.month, date__year = old.year)
                        old_profit = old_stat.profit
                        old_revenue = old_stat.total_revenue
                        old_expense = old_stat.total_expense
                    except:
                        old_profit = 0
                        old_revenue = 0
                        old_expense = 0
                    response_json['summary']['data'][str(stat.date.date())] = {
                        'profit' : stat.profit,
                        'revenue' : stat.total_revenue,
                        'expense' : stat.total_expense,
                    }
                    if stat.profit != 0 and old_profit != 0:
                        response_json['summary']['data'][str(stat.date.date())]['profit_increase'] = (stat.profit - old_profit) /old_profit * 100
                    elif stat.profit == 0:
                        response_json['summary']['data'][str(stat.date.date())]['profit_increase'] = 0
                    elif old_profit == 0:
                        response_json['summary']['data'][str(stat.date.date())]['profit_increase'] = stat.profit
                    
                    if stat.total_revenue != 0 and old_revenue != 0:
                        response_json['summary']['data'][str(stat.date.date())]['revenue_increase'] = (stat.total_revenue - old_revenue) /old_revenue * 100
                    elif stat.total_revenue == 0:
                        response_json['summary']['data'][str(stat.date.date())]['revenue_increase'] = 0
                    elif old_revenue == 0:
                        response_json['summary']['data'][str(stat.date.date())]['revenue_increase'] = stat.total_revenue
                    
                    if stat.total_expense != 0 and old_expense != 0:
                        response_json['summary']['data'][str(stat.date.date())]['expense_increase'] = (stat.total_expense - old_expense) /old_expense * 100
                    elif stat.total_expense == 0:
                        response_json['summary']['data'][str(stat.date.date())]['expense_increase'] = 0
                    elif old_expense == 0:
                        response_json['summary']['data'][str(stat.date.date())]['expense_increase'] = stat.total_expense
                    
                    response_json['summary']['total_profit'] = response_json['summary']['total_profit'] + stat.profit
                    response_json['summary']['total_revenue'] = response_json['summary']['total_revenue'] + stat.total_revenue
                    response_json['summary']['total_expense'] = response_json['summary']['total_expense'] + stat.total_expense
                
                start  = str_to_datetime(data_json['filters']['date']['start'])
                end = str_to_datetime(data_json['filters']['date']['end'])
                start = start.replace(day = 1)
                end = end.replace(day = 1)
                loop = True
                while loop:
                    if not str(start.date()) in response_json['summary']['data']:
                        response_json['summary']['data'][str(start.date())] = {
                            'profit' : 0,
                            'revenue' : 0,
                            'expense' : 0,
                            'profit_increase' : 0,
                            'revenue_increase' : 0,
                            'expense_increase' : 0
                        }
                    if start.date() >= end.date():
                        loop = False
                    else:
                        start = start + dateutil.relativedelta.relativedelta(months=1)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['GET'])
@bind
def get_accounting_settings(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            setting = AccountingSettings.objects.filter(is_active = True)[0]
            response_json['settings'] = AccountingSettingsSerializer(setting).data
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_accounting_settings(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                setting = AccountingSettings.objects.filter(is_active = True)[0]
                old_setting = setting
                if data_json['default_purchase_account_on_cash']:
                    setting.default_purchase_account_on_cash = Account.objects.get(id = data_json['default_purchase_account_on_cash'])
                if data_json['default_purchase_account_on_credit']:
                    setting.default_purchase_account_on_credit = Account.objects.get(id = data_json['default_purchase_account_on_credit'])
                if data_json['default_purchase_account_on_bank']:
                    setting.default_purchase_account_on_bank = Account.objects.get(id = data_json['default_purchase_account_on_bank'])
                if data_json['default_purchase_account_on_transfer']:
                    setting.default_purchase_account_on_transfer = Account.objects.get(id = data_json['default_purchase_account_on_transfer'])
                if data_json['default_purchase_account_on_pre_paid']:
                    setting.default_purchase_account_on_pre_paid = Account.objects.get(id = data_json['default_purchase_account_on_pre_paid'])
                if data_json['default_invoice_account_on_cash']:
                    setting.default_invoice_account_on_cash = Account.objects.get(id = data_json['default_invoice_account_on_cash'])
                if data_json['default_invoice_account_on_credit']:
                    setting.default_invoice_account_on_credit = Account.objects.get(id = data_json['default_invoice_account_on_credit'])
                if data_json['default_invoice_account_on_bank']:
                    setting.default_invoice_account_on_bank = Account.objects.get(id = data_json['default_invoice_account_on_bank'])
                if data_json['default_invoice_account_on_transfer']:
                    setting.default_invoice_account_on_transfer = Account.objects.get(id = data_json['default_invoice_account_on_transfer'])
                if data_json['default_invoice_account_on_pre_paid']:
                    setting.default_invoice_account_on_pre_paid = Account.objects.get(id = data_json['default_invoice_account_on_pre_paid'])
                if data_json['default_purchase_action_on_cash_is_add']:
                    setting.default_purchase_action_on_cash_is_add = data_json['default_purchase_action_on_cash_is_add']['state']
                if data_json['default_purchase_action_on_credit_is_add']:
                    setting.default_purchase_action_on_credit_is_add = data_json['default_purchase_action_on_credit_is_add']['state']
                if data_json['default_purchase_action_on_bank_is_add']:
                    setting.default_purchase_action_on_bank_is_add = data_json['default_purchase_action_on_bank_is_add']['state']
                if data_json['default_purchase_action_on_transfer_is_add']:
                    setting.default_purchase_action_on_transfer_is_add = data_json['default_purchase_action_on_transfer_is_add']['state']
                if data_json['default_purchase_action_on_pre_paid_is_add']:
                    setting.default_purchase_action_on_pre_paid_is_add = data_json['default_purchase_action_on_pre_paid_is_add']['state']
                if data_json['default_invoice_action_on_credit_is_add']:
                    setting.default_invoice_action_on_credit_is_add = data_json['default_invoice_action_on_credit_is_add']['state']
                if data_json['default_invoice_action_on_bank_is_add']:
                    setting.default_invoice_action_on_bank_is_add = data_json['default_invoice_action_on_bank_is_add']['state']
                if data_json['default_invoice_action_on_transfer_is_add']:
                    setting.default_invoice_action_on_transfer_is_add = data_json['default_invoice_action_on_transfer_is_add']['state']
                if data_json['default_invoice_action_on_pre_paid_is_add']:
                    setting.default_invoice_action_on_pre_paid_is_add = data_json['default_invoice_action_on_pre_paid_is_add']['state']
                if data_json['default_invoice_action_on_cash_is_add']:
                    setting.default_invoice_action_on_cash_is_add = data_json['default_invoice_action_on_cash_is_add']['state']
                
                if data_json['default_invoice_action_on_selected_account']:
                    setting.default_invoice_action_on_selected_account = data_json['default_invoice_action_on_selected_account']['state']
                if data_json['default_purchase_action_on_selected_account']:
                    setting.default_purchase_action_on_selected_account = data_json['default_purchase_action_on_selected_account']['state']
                setting.save()
                response_json['settings'] = AccountingSettingsSerializer(setting).data
                response_json['status'] = True
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                
                log('accounting/settings', 'update', setting.id, str(setting),  AccountingSettingsSerializer(old_setting).data, user)

            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
