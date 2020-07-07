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
from user_handler.models import Vendor, Customer
from inventory.utils import vendors_to_json
from sales.utils import customers_to_json
import django


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
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "closed":
                    accounts = Account.objects.filter(is_active=True, is_closed=True).order_by('id')[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "name":
                    accounts = Account.objects.filter(is_active=True, name__contains=data_json['name']).order_by('id')[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "parent":
                    accounts = Account.objects.filter(is_active=True, parent=None).order_by('id')[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "account":
                    account=Account.objects.get(id=data_json['account_id'])
                    childs = account.childs.all().filter(is_active=True)[start:end]
                    response_json['accounts'] = accounts_to_json(childs)
                    response_json['status'] = True
                    # else:
                    #     raise Exception("This account has no child.")
                if  data_json['filter'] == "vendor":
                    accounts = Account.objects.filter(vendor__id = data_json['vendor'])[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if  data_json['filter'] == "customer":
                    accounts = Account.objects.filter(customer__id = data_json['customer'])[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
                    response_json['status'] = True
                if data_json['filter'] == "multiple":
                    accounts = Account.objects.filter(is_active=True)
                    if data_json['filters']['status']:
                        accounts = accounts.filter(is_active=True, is_closed=data_json['closed']).order_by('id')
                    if data_json['filters']['name']:
                        accounts = accounts.filter(is_active=True, name__contains=data_json['name']).order_by('id')
                    if data_json['filters']['vendor']:
                        accounts = accounts.filter(vendor__id = data_json['vendor']).order_by('id')
                    if data_json['filters']['customer']:
                        accounts = accounts.filter(customer__id = data_json['customer']).order_by('id')
                    if data_json['filters']['current_amount']:
                        if data_json['filters']['current_amount_from']:
                            accounts = accounts.filter(current_amount__gte = data_json['filters']['current_amount_from']).order_by('id')
                        if data_json['filters']['current_amount_upto']:
                            accounts = accounts.filter(current_amount__lte = data_json['filters']['current_amount_upto']).order_by('id')
                    if data_json['filters']['credits']:
                        if data_json['filters']['credits_from']:
                            accounts = accounts.filter(credits__gte = data_json['filters']['credits_from']).order_by('id')
                        if data_json['filters']['credits_upto']:
                            accounts = accounts.filter(credits__lte = data_json['filters']['credits_upto']).order_by('id')                            
                    if data_json['filters']['parent']:
                        accounts = accounts.filter(is_active=True, parent=None).order_by('id')
                    if data_json['filters']['account_type']:
                        accounts = accounts.filter(account_type__id = data_json['account_type'])
                    if data_json['filters']['header']:
                        accounts = account.filter(account_type__header = data_json['header'])
                    accounts = accounts[start:end]
                    response_json['accounts'] = accounts_to_json(accounts)
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
                    opening_date = str_to_datetime(data_json['opening_date']),
                )
                if data_json['parent']:
                    account.parent = Account.objects.get(id=data_json['parent_id'], uuid=data_json['parent_uuid'])
                if data_json['customer'] and data_json['vendor']:
                    raise Exception('Account cannot have both vendor and customer as reference')
                if data_json['customer']:
                    customer = Customer.objects.get(id=data_json['customer'])
                    account.customer = customer
                if data_json['vendor']:
                    vendor = Vendor.objects.get(id=data_json['vendor'])
                    account.vendor = vendor
                account.save()
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
                account = Account.objects.get(uuid=data_json['account_uuid'])
                response_json['accounts'] = accounts_to_json([account])
                details =  {
                    'count_ledger_entry': len(LedgerEntry.objects.filter(account=account))
                }
                response_json['details'] = details
                if account.customer:
                    response_json['customer'] = customers_to_json([account.customer])
                if account.vendor:
                    response_json['vendor'] = vendors_to_json([account.vendor])
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
                    if len(account.childs.all().filter(is_active=True)):
                        raise Exception("The account you are trying to delete has a dependent(child) account.")
                    account.is_active = False
                    account.is_closed = True
                    account.save()
                response_json['status'] = True
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
        "action":"update/delete/close",
        "accounts_id" : 1,
        "accounts_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97",
        "name": "temp",
        "opening_date":"2018-12-19T09:26:03.478039",
        "new_parent":True/False
        "parent_id":2,
        "parent_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97"
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            account = Account.objects.get(id=data_json['account_id'], uuid=data_json['account_uuid'], is_active =True)
            if data_json['action'] == "update":
                account = Account.objects.get(id=data_json['account_id'], uuid=data_json['account_uuid'])
                account.name = data_json['name']
                account.opening_date = data_json['opening_date']
                if data_json['new_parent']:
                    account.parent = Account.objects.get(id=data_json['parent_id'], uuid=data_json['parent_uuid'])
                account.save()
                if data_json['customer']:
                    customer = Customer.objects.get(id=data_json['customer'])
                    account.customer = customer
                if data_json['vendor']:
                    vendor = Vendor.objects.get(id=data_json['vendor'])
                    account.vendor = vendor
                account.save()
            if data_json['action'] == 'close':
                account.is_closed = True
                account.closing_balance = account.current_amount
                account.closing_date = django.utils.timezone.now()
                account.save()
            if data_json['action'] == 'open':
                account.is_closed = False
                account.closing_balance = 0
                account.closing_date = None
                account.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})