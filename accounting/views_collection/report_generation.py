from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user_handler.permission_check import bind, check_permission
import json
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from accounting.models import EntryType, AccountType, Account, LedgerEntry, MonthlyStats, FreeEntryLedger
from accounting.utils import accounts_to_json, entry_types_to_json, accounts_types_to_json, ledger_entries_to_json
import datetime
from django.core import serializers

# didn't use aggregate sum coz Using cProfile profiler, I find that in my development environment, 
# it is more efficient (faster) to sum the values of a list than to aggregate using Sum()
# from django.db.models import Sum

@require_http_methods(['POST'])
@bind
def generate_profit_loss_statement(self, request):
    response_json = {'status':False}
    # if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
    #     try:
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    if data_json['action'] == "get":
        if data_json['filter'] == "none":
            monthly_stats = MonthlyStats.objects.filter(is_active=True).order_by('-date')
            today =datetime.datetime.now()
            
            if today.year > monthly_stats[0].date.year:
                print("run monthly status scripts")

            tmp = {
                'total_assets':0,
                'total_liabilities':0,
                'total_revenue':0,
                'total_expense':0,
                'total_draw':0,
                'total_equity':0,
                'profit':0,
                'to_be_paid':0,
                'to_pay':0
            }
            fields =  [
                'total_assets',
                'total_liabilities',
                'total_revenue',
                'total_expense',
                'total_draw',
                'total_equity',
                'profit',
                'to_be_paid',
                'to_pay'
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
            new_entries = LedgerEntry.objects.filter(is_active=True, created_at__range=[monthly_stats[0].date, today])
            response_json['this_month'] = sum_from_legder_entries(new_entries, fields)
    return JsonResponse(response_json)


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
        for entry in entries.filter( entry_type__header = header ):
            corrections = FreeEntryLedger.objects.filter(entry_for = entry)
            total[header] = total[header] + entry.payment.amount + sum(e.amount for e in corrections)
    total['profit'] = total['revenue'] - total['expense']
    return total
    # for account in Account.objects.filter(is_active = True, is_closed=False)
