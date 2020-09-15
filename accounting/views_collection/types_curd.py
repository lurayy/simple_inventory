from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user_handler.permission_check import bind, check_permission
import json
from inventory.utils import  str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from accounting.models import AccountType, Account, LedgerEntry, MonthlyStats
from accounting.utils import accounts_to_json, accounts_types_to_json, ledger_entries_to_json
from user_handler.models import log

@require_http_methods(['POST'])
@bind
def get_multiple_account_types(self, request):
    '''
    url : api/v1/accounting/accounts/get
    {
        "action":"get",
    }s
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] =="get":
                if data_json['filter'] == "none":
                    x = AccountType.objects.filter(is_active=True)
                    response_json['count'] = len(x)
                    x = x[data_json['start']:data_json['end']]
                    response_json['account_types'] = accounts_types_to_json(x)
                if data_json['filter'] == "id":
                    x = AccountType.objects.filter(is_active=True, id= data_json['id'])
                    response_json['count'] = len(x)
                    response_json['account_types'] = accounts_types_to_json(x)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_account_types(self, request):
    '''
    url : api/v1/accounting/accounts/get
    {
        "action":"get",
    }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']        
            
            if data_json['action'] =="add":
                x = AccountType.objects.create(
                    header = data_json['header'],
                    name = data_json['name']
                )
                response_json['account_types'] = accounts_types_to_json([x])
                response_json['status'] = True
                log('accounting/account_type', 'create', x.id, str(x), {}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def udpate_account_types(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']        
            
            if data_json['action'] =="update":
                x = AccountType.objects.get(id = data_json['account_type_id'])
                changes = {}
                if data_json['name']:
                    changes['account_type_name'] = x.name
                    print("hanasdf")
                    x.name = data_json['name']
                if data_json['status']:
                    changes['account_type_is_active'] = x.is_active
                    x.is_active = data_json['status']['is_active']
                if data_json['header']:         
                    changes['account_type_header'] = x.header           
                    x.header = data_json['header']
                x.save()
                response_json['account_types'] = accounts_types_to_json([x])
                response_json['status'] = True
                log('accounting/account_type', 'update', x.id, str(x), changes, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_account_types(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']        
            
            if data_json['action'] =="delete":
                for id in data_json['account_type_ids']:
                    x = AccountType.objects.get(id = id)
                    log('accounting/account_type', 'soft-delete', x.id, str(x), {}, user)
                    x.is_active = False
                    x.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

