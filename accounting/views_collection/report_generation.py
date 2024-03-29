from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user_handler.permission_check import bind, check_permission
import json
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from accounting.models import  AccountType, Account, LedgerEntry, MonthlyStats
from accounting.utils import accounts_to_json, accounts_types_to_json, ledger_entries_to_json
import datetime
from django.core import serializers
import dateutil
from django.db.models import Sum

# didn't use aggregate sum coz Using cProfile profiler, I find that in my development environment, 
# it is more efficient (faster) to sum the values of a list than to aggregate using Sum()
# from django.db.models import Sum

@require_http_methods(['POST'])
@bind
def generate_profit_loss_statement(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    data = {'token':request.headers['Authorization'].split(' ')[1]}
                    valid_data = VerifyJSONWebTokenSerializer().validate(data)
                    user = valid_data['user']        
                
                    monthly_stats = MonthlyStats.objects.filter(is_active=True).order_by('-date')
                    today =datetime.datetime.now()
                    if len(monthly_stats) >= 0 :
                        latest_calulcation_date = today - dateutil.relativedelta.relativedelta(months=1)
                    else:
                        latest_calulcation_date = monthly_stats[0].date

                    if today.year > latest_calulcation_date.year:
                        print("run monthly status scripts")

                    tmp = {
                        'total_assets':0,
                        'total_liabilities':0,
                        'total_revenue':0,
                        'total_expense':0,
                        'total_draw':0,
                        'total_equity':0,
                        'profit':0
                    }
                    fields =  [
                        'total_assets',
                        'total_liabilities',
                        'total_revenue',
                        'total_expense',
                        'total_draw',
                        'total_equity',
                        'profit',
                    ]
                    stats = serializers.serialize('json', monthly_stats)
                    stats = json.loads(stats)
                    for stat in stats:
                        for field in fields:
                            tmp[field] = tmp[field] + stat['fields'][field]
                    response_json = {
                        'status':True,
                        'monthly_stats':stats,
                        'past_months':tmp,
                        'this_month':{},
                        'total':{} 
                    }
                    new_entries = LedgerEntry.objects.filter(is_active=True, created_at__range=[latest_calulcation_date, today])
                    response_json['this_month'] = sum_from_legder_entries(new_entries, fields)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

# show credits that are not paid 


def sum_from_legder_entries(entries, fields):
    entry_type_headers = [
            'assets','liabilities','revenue','expense','draw','equity'
        ]
    account_headers =  [
        'assets','liabilities','revenue','expense'
    ]
    total = {
        'assets':0,
        'liabilites':0,
        'revenue':0,
        'expense':0,
        'draw':0,
        'equity':0,
    }
    for header in entry_type_headers:
        for entry in entries.filter( account__account_type__header = header ):
            total[header] = total[header] + entry.payment.amount
    total['profit'] = total['revenue'] - total['expense']
    return total
    # for account in Account.objects.filter(is_active = True, is_closed=False)



@require_http_methods(['POST'])
@bind
def generate_balance_sheet_statement(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    accounts = Account.objects.filter(is_active=True, is_closed=False)
                    headers = []
                    balance_sheet = {}
                    for header in AccountType.HEADER_CHOICE:
                        headers.append(header[0])
                        balance_sheet[header[0]] = {
                                'header':header[0],
                                'sub_headers':[],
                                'meta_data':{}
                            }
                    for account_type in AccountType.objects.filter(is_active=True):
                        temp = accounts.filter(account_type=account_type)
                        x = temp.aggregate(Sum('current_amount'))['current_amount__sum']
                        balance_sheet[account_type.header]['sub_headers'].append(
                                {
                                    'name':account_type.name,
                                    'header':account_type.header,
                                    'accounts':accounts_to_json(temp),
                                    'meta_data':{
                                        'count':len(temp),
                                        'sum_current_amount': x if x else 0,
                                    }
                                }
                            )
                    for header in headers:
                        balance_sheet[header]['meta_data'] = {
                            'count': len(balance_sheet[header]['sub_headers']),
                            'sum_current_amount': sum( d['meta_data']['sum_current_amount'] for d in balance_sheet[header]['sub_headers']),
                        }
                    balance_sheet['liabilities']['net_profit'] = balance_sheet['revenue']['meta_data']['sum_current_amount']*-1-balance_sheet['expense']['meta_data']['sum_current_amount']
                    print(balance_sheet['liabilities']['net_profit'])
                # elif data_json['filter']== "date":
                    balance_sheet['status'] = True
                    return JsonResponse(balance_sheet)
            return JsonResponse(response_json)        
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
