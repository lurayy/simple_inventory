from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user_handler.permission_check import bind, check_permission
import json
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from accounting.models import AccountType, Account, LedgerEntry, MonthlyStats, update_ledger
from accounting.utils import accounts_to_json, accounts_types_to_json, ledger_entries_to_json
from payment.models import Payment, PaymentMethod
import uuid

@require_http_methods(['POST'])
@bind
def get_multiple_ledger_entries(self, request):
    '''
    url : api/v1/accouting/ledger/entries/get
    {
        "action":"get",
        "filter":"none",
        "start":0,
        "end":5
    }
    {
        "action":"get",
        "filter":"account",
        "start":0,
        "end":5,
        "account_id":1
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    response_json['ledger_entries'] = ledger_entries_to_json(LedgerEntry.objects.filter(is_active=True).order_by('date')[data_json['start']:data_json['end']])
                    response_json['status'] = True
                if data_json['filter'] == "account":
                    entries =  LedgerEntry.objects.filter(is_active=True, account=Account.objects.get(id=data_json['account_id'])).order_by('date')[data_json['start']:data_json['end']]
                    response_json['ledger_entries'] = ledger_entries_to_json(entries)
                    response_json['status'] = True
                if data_json['filter'] == "multiple":
                    start = data_json['start']
                    end = data_json['end']
                    entries = LedgerEntry.objects.filter(is_active = True)
                    if data_json['filters']['account']:
                        entries = entries.filter(account__id = data_json['account']).order_by('date')
                    if data_json['filters']['date']:
                        if data_json['filters']['start_date']:
                            start_date = str_to_datetime(str(data_json['filters']['start_date']))
                            entries = entries.filter(date__gte = start_date).order_by('date')
                        if data_json['filters']['end_date']:
                            end_date = str_to_datetime(str(data_json['filters']['end_date']))
                            entries = entries.filter(date__lte = end_date).order_by('date')
                    if data_json['filters']['bundle_id']:
                        entries = entries.filter(bundle_id__contains = data_json['bundle_id']).order_by('date')
                    if data_json['filters']['apply_is_add']:
                        entries = entries.filter(is_add = data['filters']['is_add']).order_by('date')
                    if data_json['filters']['amount']:
                        if data_json['filters']['amount_from']:
                            entries = entries.filter(payment__amount__gte = data_json['amount_from']).order_by('date')
                        if data_json['filters']['amount_upto']:
                            entries = entries.filter(payment__amount__lte = data_json['amount_upto']).order_by('date')
                    if data_json['filters']['payment_method']:
                        entries = entries.filter(payment__method__id = data_json['payment_method']).order_by('date')
                    entries = entries[start:end]
                    response_json['ledger_entries'] = ledger_entries_to_json(entries)
                    response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_ledger_entry(self, request):
    '''
    url : api/v1/accounting/ledger/entry/add
    {
        "action":"add",
        "account_id":1,
        "ledger_entry_type_id":2,
        "remarks":"some sassy remarks",
        "date":"2018-12-19T09:26:03.478039",
        "amount":25.2153
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            print(data_json)
            if data_json['action'] == "add":
                if data_json['bundle_id']:
                    bundle_id = data_json['bundle_id']
                else:
                    bundle_id = uuid.uuid4()
                for entry in data_json['entries']:
                    entry_model = LedgerEntry.objects.create(
                        account = Account.objects.get(id=entry['account_id']),
                        is_add = entry['is_add'],
                        remarks = entry['remarks'],
                        date = str_to_datetime(entry['date']),
                        payment = Payment.objects.get(id=entry['payment_id']),
                        bundle_id = bundle_id
                    )
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_ledger_entry_details(self, request):
    '''
    url : api/v1/accouting/ledger/entry/get
    {
        "action":"get",
        "ledger_entry_id":2
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                entry = LedgerEntry.objects.get(id=data_json['ledger_entry_id'])
                response_json['ledger_entries'] = ledger_entries_to_json([entry])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_ledger_entry(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                entry = LedgerEntry.objects.get(id = data_json['ledger_entry_id'])
                new_entry = update_ledger(entry, data_json['amount'])
                response_json['entries'] = ledger_entries_to_json([entry, new_entry])
                response_json['status'] = True
            return response_json
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
     


                



# @require_http_methods(['POST'])
# @bind
# def create_free_entry(self, request):
#     '''
#     url : api/v1/accouting/ledger/entry/get
#     {
#         "action":"get",
#         "ledger_entry_id":2
#     }
#     '''
#     response_json = {'status':False}
#     # if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
#     #     try:
#     json_str = request.body.decode(encoding='UTF-8')
#     data_json = json.loads(json_str)
#     if data_json['action'] == "add":
#         free_entry = FreeEntryLedger.objects.create(
#             entry_for=LedgerEntry.objects.get(is_active=True, id=data_json['ledger_entry']),
#             amount = data_json['amount'],
#             remarks = data_json['remarks']
#         )
#         response_json['status']=True
#     return JsonResponse(response_json)
#     #     except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
#     #         return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
#     # else:
#     #     return JsonResponse({'status':False, "error":'You are not authorized.'})


