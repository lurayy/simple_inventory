from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import EntryType, AccountType, Account, LedgerEntry, MonthlyStats
from .utils import accounts_to_json, entry_types_to_json, accounts_types_to_json, ledger_entries_to_json
from user_handler.permission_check import bind, check_permission
import json
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@require_http_methods(['POST'])
@bind
def get_multiple_accounts(self, request):
    '''
    url : api/v1/accounting/accounts/get
    {
        "action":"get",
        "start":0,
        "end":20,
        "filter":"none"
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if str(data_json['action']).lower() == "get":
                start = int(data_json["start"])
                end = int(data_json["end"])
                if data_json['filter'] == "none":
                    accounts = Account.objects.filter(is_active=True, is_closed=False).order_by('id')[start:end]
                    response_json['accounts'] = accounts_types_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "closed":
                    accounts = Account.objects.filter(is_active=True, is_closed=True).order_by('id')[start:end]
                    response_json['accounts'] = accounts_types_to_json(accounts)
                    response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_account(self, request):
    '''
    url : api/v1/accounting/account/add
    {
	"action":"add",
	"account_type":1,
	"name":"new account",
	"opening_balance":5,
	"opening_date":"2018-12-19T09:26:03.478039"
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            
            if data_json['action'] == "add":
                account = Account.objects.create(
                    account_type = AccountType.objects.get(id=data_json['account_type']),
                    name = data_json['name'],
                    opening_balance = data_json['opening_balance'],
                    opening_date = str_to_datetime(data_json['opening_date'])
                )
                response_json['accounts'] = accounts_to_json([account])
                response_json['status'] = True
                return JsonResponse( response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_account_details(self, request):
    '''
    url : api/v1/accounting/accounting/account/get
    {
        "action":"get",
        "account_id":1,
        "account_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97"
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'get':
                account = Account.objects.get(id=data_json['account_id'], uuid=data_json['account_uuid'])
                response_json['accounts'] = accounts_to_json([account])
                details =  {
                    'count_ledger_entry': len(LedgerEntry.objects.filter(account=account))
                }
                response_json['details'] = details
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_accounts(self, request):
    '''
    url : api/v1/accouting/accounts/delete
    {
        "action":"delete",
        "accounts_ids : [1],
        "accounts_uuids":["a9140902-7863-40f6-b01a-ec5045d38c97"]
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
                    
            if data_json['action'] == 'delete':
                for i in range(len(data_json['accounts_ids'])):
                    account = Account.objects.get(id=data_json['accounts_ids'][i], uuid=data_json['accounts_uuids'][i])
                    account.is_active = False
                    account.is_closed = True
                    account.save()
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_account(self, request):
    '''
    url : api/v1/accouting/accounts/delete
    {
        "action":"delete",
        "accounts_ids : [1],
        "accounts_uuids":["a9140902-7863-40f6-b01a-ec5045d38c97"]
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            account = Account.objects.get(id=data_json['account_id'], uuid=data_json['account_uuid'])
            if data_json['action'] == "update":
                account = Account.objects.get(id=data_json['account_id'], uuid=data_json['account_uuid'])
                account.name = data_json['name']
                account.opening_date = data_json['opening_date']
                account.parent = Account.objects.get(id=data_json['parent_id'], uuid=data_json['parent_uuid'])
                account.save()
            if data_json['action'] == 'close':
                account.is_closed = True
                account.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
