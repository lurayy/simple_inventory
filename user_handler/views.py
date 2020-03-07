from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods

from .exceptions import  EmptyValueException

from .forms import UserForm, LoginForm
from .models import CustomUserBase
import json


def check(user):
    '''Checks the user_type to grant permission to access certain function'''
    if (user.user_type == "MANAGER"):
        return True
    else:
        return False


@require_http_methods(['GET', 'POST'])
def user_login(request):
    '''user login function'''
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    response_json = {'status':False, 'error':'Username or Password is not correct.'}
                    return HttpResponse(json.dumps(response_json),content_type = 'application/json')
        else:
            form = LoginForm()
            return render (request, 'user_handler/login.html',{'form':form})


@login_required
def user_logout(request):
    '''User logout function'''
    logout(request)
    return HttpResponseRedirect('/login')


@require_http_methods(['GET'])
@login_required
def dashboard(request):
    '''Dashboard entry point fucntion'''
    return render (request, 'dashboard.html')


@require_http_methods(['GET', 'POST'])
@login_required
@user_passes_test(check)
def user_creation(request):
    '''Creates new  non-super user'''
    if request.method == 'POST':
        user_data = UserForm(request.POST)
        if user_data.is_valid():
            new_user = user_data.save(commit=False)
            new_user.save()
            print(new_user)
            return HttpResponseRedirect('/')
        else:
            print(user_data)
            return HttpResponse('Bad Data')
    user_form = UserForm()
    return render(request, 'user_handler/user_form.html',{'user_form':user_form})


def get_users_data(start, end):
    users_json = []
    active_users = CustomUserBase.objects.filter(is_staff=False, is_superuser=False)[start:end]
    for user in active_users:
        user_json = {'id':'', 'name':'', 'status':'','user_name':'', 'uuid':''}
        user_json['id'] = str(user.id)
        user_json['name'] = f'{user.first_name} {user.last_name}'
        user_json['status'] = str(user.user_type)
        user_json['user_name'] = str(user.username)
        user_json['is_active'] = user.is_active
        user_json['uuid'] = str(user.uuid)
        users_json.append(user_json)
    return users_json


@require_http_methods(['GET', 'POST'])
@login_required
@user_passes_test(check)
def user_modify(request):
    '''Deletes non-super users'''
    '''
    POST json format: 
    {
        'action':'delete'/'revive',
        'user_id':'4',
        'uuid':'c4971e44-a4d8-4675-ad27-e7b3fd24332a',
    }
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
            user = CustomUserBase.objects.get(id=int(data_json['user_id']), uuid=str(data_json['uuid']))
            if str(data_json['action']).lower() == 'delete':
                user.is_active = False
            if str(data_json['action']).lower() == 'revive':
                user.is_active = True
            user.save()
            return JsonResponse({'status':True, 'msg':f'Change is made to {user.username}'})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

    response_json = {'status':'', 'users':[]}
    response_json['users'] = get_users_data(0,10)
    response_json['status'] = True
    return render(request, 'user_handler/user_delete.html', {'response_json':response_json})
