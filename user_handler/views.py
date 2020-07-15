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
from .models import CustomUserBase, Profile
import json
from django.middleware.csrf import get_token


from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .serializers import CustomPermissionSerializer, ProfileSerializer
from .permission_check import bind, check_permission
from .models_permission import CustomPermission

def csrf(request):
    return JsonResponse({'x-csrftoken': get_token(request)})


def check(user):
    '''Checks the user_type to grant permission to access certain function'''
    if (user.user_type == "MANAGER"):
        return True
    else:
        return False

@login_required
def user_logout(request):
    '''User logout function'''
    logout(request)
    return HttpResponseRedirect('/login')


@require_http_methods(['POST'])
@bind
def user_creation(request):
    '''Creates new  non-super user'''
    response_json = {}
    new_user = None
    try:
        if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)    
            if data_json['action'] == "add":
                user =  CustomUserBase.objects.get(id=request.user.id)
                new_user = CustomUserBase.objects.create_user(str(data_json['username']), str(data_json['email']), str(data_json['password']))
                new_user.first_name = str(data_json['first_name'])
                new_user.last_name = str(data_json['last_name'])
                role = CustomPermission.objects.get(id = data_json['custom_permission_id'])
                new_user.role = role
                new_user.save()
                if data_json['profile']:
                    profile = Profile.objects.create(
                        user = new_user,
                        address = data_json['profile']['address'],
                        phone_number = data_json['profile']['phone_number'],
                        phone_number2 = data_json['profile']['phone_number2'],
                        post = data_json['profile']['post']
                    )
                    if (data_json['profile']['profile_image']):
                        data = data_json['profile']['profile_image'][0]['base64']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                        profile.profile_image = data
                        profile.save()
                response_json['status'] = True
            return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        if (new_user):
            new_user.delete()
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@require_http_methods(['POST'])
@bind
def get_multiple_user(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    users = CustomUserBase.objects.filter(is_active = True)
                    response_json['count'] = len(users)
                    users = users[data_json['start']:data_json['end']]
                    users_json = []
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                        users_json.append(user_json)
                    response_json['status'] = True
                    response_json['users'] = users_json
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


def user_data(user):
    user_json = {'id':'', 'name':'', 'status':'','username':'', 'uuid':''}
    user_json['id'] = str(user.id)
    user_json['name'] = f'{user.first_name} {user.last_name}'
    user_json['role_str'] = str(user.role)
    user_json['role'] = (user.role.id)

    user_json['username'] = str(user.username)
    user_json['is_active'] = user.is_active
    user_json['is_active_str'] = "Active" if user.is_active else "Deactivated"
    user_json['uuid'] = str(user.uuid)
    user_json['last_login'] = user.last_login
    user_json['email'] = user.email
    user_json['first_name'] = user.first_name
    user_json['last_name'] = user.last_name
    return user_json



@require_http_methods(['POST'])
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
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
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
        'action':'delete'/'revive'
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
                user = CustomUserBase.objects.get(id=data_json['user_id'])
                user_json = {'id':'', 'name':'', 'status':'','username':'', 'uuid':''}
                user_json['id'] = str(user.id)
                user_json['name'] = f'{user.first_name} {user.last_name}'
                user_json['first_name'] = user.first_name
                user_json['last_name'] = user.last_name
                user_json['username'] = str(user.username)
                user_json['is_active'] = user.is_active
                user_json['email'] = str(user.email)
                user_json['uuid'] = str(user.uuid)
                user_json['role'] = (user.role.id)
                user_json['role_str'] = str(user.role)
                user_json['roles_given'] = CustomPermissionSerializer(user.role).data
                user_json['status'] = True
                return JsonResponse(user_json)
            else:
                user = CustomUserBase.objects.get(id=int(data_json['user_id']))
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
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


def get_current_user(request):
    try:
        data = {'token':request.headers['Authorization'].split(' ')[1]}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        response_json = {
            'status':True,
            'user':{
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'role_str':str(user.role),
                'username':user.username
            }
        }
        return JsonResponse( response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})