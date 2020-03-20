from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import  EmptyValueException
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import UserForm, LoginForm
from .models import CustomUserBase
import json
from django.middleware.csrf import get_token



def csrf(request):
    return JsonResponse({'x-csrftoken': get_token(request)})


def check(user):
    '''Checks the user_type to grant permission to access certain function'''
    if (user.user_type == "MANAGER"):
        return True
    else:
        return False

@ensure_csrf_cookie
@require_http_methods(['GET'])
def entry_point(request):
    return render (request, 'build/index.html')



@ensure_csrf_cookie
@require_http_methods(['POST'])
def user_login(request):
    '''user login function'''
    response_json = {}
    try:    
        if request.user.is_authenticated:
            response_json['status'] = True
            return JsonResponse(response_json)
        else:
            if request.method == 'POST':
                json_str = request.body.decode(encoding='UTF-8')
                data_json = json.loads(json_str)
                username = data_json['username']
                password = data_json['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request,user)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                else:
                    response_json = {'status':False, 'msg':'Username or Password is not correct.'}
                    return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
def user_logout(request):
    '''User logout function'''
    logout(request)
    return HttpResponseRedirect('/login')


@ensure_csrf_cookie
@require_http_methods(['GET'])
@login_required
def dashboard(request):
    '''Dashboard entry point fucntion'''
    return render (request, 'build/index.html')


@require_http_methods(['POST'])
@login_required
@user_passes_test(check)
def user_creation(request):
    '''Creates new  non-super user'''
    response_json = {}
    try:
        if request.method == 'POST':
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)    
            user =  CustomUserBase.objects.get(id=request.user.id)
            if (user.user_type == "MANAGER"):
                new_user = CustomUserBase.objects.create_user(str(data_json['username']), str(data_json['email']), str(data_json['password']))
                new_user.first_name = str(data_json['first_name'])
                new_user.last_name = str(data_json['last_name'])
                new_user.user_type = str(data_json['user_type'])
                new_user.save()
                response_json['status'] = True
                return JsonResponse(response_json)
            else:
                response_json = {'status':False, 'error': 'Permission Denied'}
                return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


def get_users_data(start, end):
    users_json = []
    active_users = CustomUserBase.objects.filter(is_staff=False, is_superuser=False)[start:end]
    for user in active_users:
        user_json = {'id':'', 'name':'', 'status':'','username':'', 'uuid':''}
        user_json['id'] = str(user.id)
        user_json['name'] = f'{user.first_name} {user.last_name}'
        user_json['status'] = str(user.user_type)
        user_json['username'] = str(user.username)
        user_json['is_active'] = user.is_active
        user_json['uuid'] = str(user.uuid)
        users_json.append(user_json)
    return users_json


@require_http_methods(['POST'])
@login_required
@user_passes_test(check)
def users(request):
    '''Deletes non-super users'''
    '''
    futher query : 
    {
        'action':'get',
        'start':11,
        'end':20
    }
    '''
    if request.method == 'POST':
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if str(data_json['action']).lower() == "get":
                response_json = {'status':'', 'users':[]}
                response_json['users'] = get_users_data(int(data_json['start']), int(data_json['end']))
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    response_json = {'status':'', 'users':[]}
    response_json['users'] = get_users_data(0,10)
    response_json['status'] = True
    return JsonResponse(response_json)


# for geting single user details and modify
@login_required
def s_user(request):
    '''POST json format: 
    {
        'action':'delete'/'revive','modify'
        'user_id':'4',
        'uuid':'c4971e44-a4d8-4675-ad27-e7b3fd24332a',
    }
    for modify:
    {
        'action':'edit',
        'user_id':'4',
        'uuid':'c4971e44-a4d8-4675-ad27-e7b3fd24332a',
        'first_name'
        'last_name'
        'email'
        'username'
        'user_type'
    }
    '''
    users_json = []
    if request.method == 'POST':
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)   
        try:
            if data_json['action'] == "get":
                user = CustomUserBase.objects.get(id=data_json['user_id'], uuid=data_json['uuid'])
                user_json = {'id':'', 'name':'', 'status':'','username':'', 'uuid':''}
                user_json['id'] = str(user.id)
                user_json['name'] = f'{user.first_name} {user.last_name}'
                user_json['first_name'] = user.first_name
                user_json['last_name'] = user.last_name
                user_json['status'] = str(user.user_type)
                user_json['username'] = str(user.username)
                user_json['is_active'] = user.is_active
                user_json['email'] = str(user.email)
                user_json['uuid'] = str(user.uuid)
                user_json['status'] = True
                return JsonResponse(user_json)
            else:
                user = CustomUserBase.objects.get(id=int(data_json['user_id']), uuid=str(data_json['uuid']))
                if str(data_json['action']).lower() == 'delete':
                    user.is_active = False
                if str(data_json['action']).lower() == 'revive':
                    user.is_active = True
                if str(data_json['action']) == "edit":
                    user.first_name = data_json['first_name']
                    user.last_name = data_json['last_name']
                    user.email = data_json['email']
                    user.username = data_json['username']
                    user.user_type = data_json['user_type']
                user.save()
                return JsonResponse({'status':True, 'msg':f'Change is made to {user.username}. Change Type: {data_json["action"]}'})
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@require_http_methods(['POST'])
def get_current_user(request):
    users_json = []
    try:
        if (request.user.uuid):
            if request.method == 'POST':
                user = CustomUserBase.objects.get(id=int(request.user.id), uuid=request.user.uuid)
                user_json = {'first_name':user.first_name,
                    'last_name':user.last_name,
                    'user_type':user.user_type,
                    'username':user.username
                    }
                response_json = {'status':True, 'user_data':user_json}
                return JsonResponse(response_json)
        else:
            response_json = {'status':False, 'user_data':{}}
            return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

