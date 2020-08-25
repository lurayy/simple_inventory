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
from .models import CustomUserBase, Profile, UserActivities, PasswordResetCode, Setting, Notification, NotificationSetting, ActivityLog, UserActivities
import json
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate
import random
from django.template import Context
from django.core.files.base import ContentFile
import base64
from inventory.utils import str_to_datetime
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .serializers import CustomPermissionSerializer, ProfileSerializer, UserActivitySerializer, SettingSerializer, NotificationSerializer, NotificationSettingSerializer, ActivityLogSerializer, UserActivitiesSerializer
from .permission_check import bind, check_permission
from .models_permission import CustomPermission
import datetime
from django.db.models import Q
from rest_framework_jwt.settings import api_settings

from django.core.mail import send_mail

from django.conf import settings
from django.template.loader import get_template 

import django

from user_handler.models import log

def csrf(request):
    return JsonResponse({'x-csrftoken': get_token(request)})

def ss(request):    
    data = {'token':request.headers['Authorization'].split(' ')[1]}
    valid_data = VerifyJSONWebTokenSerializer().validate(data)
    user = valid_data['user']
    return user


def check(user):
    '''Checks the user_type to grant permission to access certain function'''
    if (user.user_type == "MANAGER"):
        return True
    else:
        return False



@require_http_methods(['POST'])
def user_token(request):
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        username = str(data_json['username'])
        password = str(data_json['password'])
        user = authenticate(username = username, password = password)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        UserActivities.objects.create(
            user = user,
            ip = get_client_ip(request),
            log_time = django.utils.timezone.now(),
            action = "LOGIN"
        )
        return JsonResponse({'token':token})
    except:
        return JsonResponse({'status':False, "error":'Wrong username or password.'})


def log_logout_time(request):
    try:
        data = {'token':request.headers['Authorization'].split(' ')[1]}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        UserActivities.objects.create(
                user = user,
                ip = get_client_ip(request),
                log_time = django.utils.timezone.now(),
                action = "LOGOUT"
            )    
        return JsonResponse({'status':True})
    except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@require_http_methods(['POST'])
@bind
def user_creation(self, request):
    '''Creates new  non-super user'''
    response_json = {}
    new_user = None
    try:
        jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
        if jwt_check:
            if not jwt_check['status']:
                return JsonResponse(jwt_check)
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)    
            if data_json['action'] == "add":
                new_user = CustomUserBase.objects.create_user(str(data_json['username']), str(data_json['email']), str(data_json['password']))
                new_user.first_name = str(data_json['first_name'])
                new_user.last_name = str(data_json['last_name'])
                role = CustomPermission.objects.get(id = data_json['role_id'])
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
                    if data_json['profile']['profile_image']:
                        data = data_json['profile']['profile_image']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='profile_img.' + ext)
                        profile.profile_image = data
                        profile.save()
                else:
                    profile = Profile.objects.create(user = new_user)
                response_json['status'] = True
                log('user', 'create', new_user.id, str(new_user), {}, ss(request))
            return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        if (new_user):
            new_user.delete()
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@require_http_methods(['POST'])
@bind
def get_multiple_user(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            users_json = []
            user_json = []
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    users = CustomUserBase.objects.filter().order_by('-id')
                    response_json['count'] = len(users)
                    users = users[data_json['start']:data_json['end']]
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                        users_json.append(user_json)
                    response_json['status'] = True
                    response_json['users'] = users_json

                if data_json['filter'] == "id":
                    users = CustomUserBase.objects.filter(id=data_json['user_id']).order_by('-id')
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                    response_json['status'] = True
                    response_json['users'] = [user_json]


                if data_json['filter'] == "name":
                    users = CustomUserBase.objects.filter(Q(username__icontains = data_json['name'])|Q(first_name__icontains = data_json['name'])|Q(last_name__icontains = data_json['name'])).order_by('-id')
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                        users_json.append(user_json)
                    response_json['status'] = True
                    response_json['users'] = users_json
                
                if data_json['filter'] == "role":
                    users = CustomUserBase.objects.filter(role__id = data_json['role_id'] ).order_by('-id')
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                        users_json.append(user_json)
                    response_json['status'] = True
                    response_json['users'] = users_json

                if data_json['filter'] == "status":
                    users = CustomUserBase.objects.filter(is_active = data_json['is_active'] ).order_by('-id')
                    for user in users:
                        user_json = user_data(user)
                        try:
                            user_json['profile'] = ProfileSerializer(Profile.objects.get(user = user)).data
                        except Exception as e:
                            user_json['profile'] = None
                        users_json.append(user_json)
                    response_json['status'] = True
                    response_json['users'] = users_json
                
                if data_json['filter'] == "multiple":
                    users = CustomUserBase.objects.all()
                    if data_json['filters']['name']:
                        users = users.filter(Q(username__icontains = data_json['filters']['name'])|Q(first_name__icontains = data_json['filters']['name'])|Q(last_name__icontains = data_json['filters']['name'])).order_by('-id')
                    if data_json['filters']['role']:
                        users = users.filter(role__id = data_json['filters']['role_id'] ).order_by('-id')
                    if data_json['filters']['status']:
                        users = CustomUserBase.objects.filter(is_active = data_json['filters']['is_active']).order_by('-id')
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
@bind
def update_user(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            user = CustomUserBase.objects.get(id = user.id)
            profile = Profile.objects.get(user = user)
            if data_json['action'] == "update":
                if data_json['first_name']:
                    user.first_name = data_json['first_name']
                if data_json['last_name']:
                    user.last_name = data_json['last_name']
                if data_json['password']:
                    user.set_password(data_json['password'])
                if data_json['profile']:
                    if data_json['profile']['address']:
                        profile.address = data_json['profile']['address']
                    if data_json['profile']['phone_number']:
                        profile.phone_number = data_json['profile']['phone_number']
                    if data_json['profile']['phone_number2']:
                        profile.phone_number2 = data_json['profile']['phone_number2']
                    if data_json['profile']['post']:
                        profile.post = data_json['profile']['post']
                    if data_json['profile']['profile_image']:
                        if data_json['profile']['profile_image'] == "remove":
                            profile.profile_image = None
                        else:
                            data = data_json['profile']['profile_image']
                            format, imgstr = data.split(';base64,') 
                            ext = format.split('/')[-1] 
                            data = ContentFile(base64.b64decode(imgstr), name='profile_img.' + ext)
                            profile.profile_image = data
                    profile.save()
                user.save()
                response_json['status'] = True    
            elif data_json['action'] == "deactivate":
                user.is_active = False
                user.save()
                log('user', 'deactivate', user.id, str(user), {}, ss(request))
                response_json['status'] = True    
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_user(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "deactivate":
                user = CustomUserBase.objects.get(id = data_json['user_id'])
                user.is_active = False
                user.save()
                log('user', 'deactivate', user.id, str(user), {}, ss(request))

                response_json['status'] = True
            elif data_json['action'] == "activate":
                user = CustomUserBase.objects.get(id = data_json['user_id'])
                user.is_active = True
                log('user', 'activate', user.id, str(user), {}, ss(request))
                user.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


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
                'username':user.username,
                'powers' : CustomPermissionSerializer(user.role).data
            }
        }
        response_json['user']['powers'].pop('id')
        response_json['user']['powers'].pop('name')
        response_json['user']['powers'].pop('description')
        return JsonResponse( response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@require_http_methods(['POST'])
@bind
def get_multiple_roles(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                roles = CustomPermission.objects.filter().order_by('-id')
                response_json['roles'] = []
                for role in roles:
                    data = CustomPermissionSerializer(role).data
                    response_json['roles'].append(
                        {
                            'id': data.pop('id'),
                            'name': data.pop('name'),
                            'discription' : data.pop('description'),
                            'powers' : data
                        }
                    )
                response_json['status'] = True
                response_json['count'] = len(roles)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def get_role_details(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                roles = CustomPermission.objects.filter(id=data_json['role_id']).order_by('-id')
                response_json['roles'] = []
                for role in roles:
                    data = CustomPermissionSerializer(role).data
                    response_json['roles'].append(
                        {
                            'id': data.pop('id'),
                            'name': data.pop('name'),
                            'discription' : data.pop('description'),
                            'powers' : data
                        }
                    )
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def valid_power(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                powers = CustomPermission._meta.get_fields()
                response_json['valid_powers'] = []
                for power in powers:
                    x = (power.name)
                    if x == "id":
                        pass
                    elif x == "role_users":
                        pass
                    elif x == "name":
                        pass
                    elif x == "description":
                        pass
                    else:
                        response_json['valid_powers'].append(x)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def add_new_role(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                with open('user_handler/temp.py','w') as f:
                    print("write")
                    f.write('from user_handler.models_permission import CustomPermission')
                    f.write('\n')
                    f.write('def tes():\n')
                    f.write('   role = CustomPermission.objects.create( name = "'+data_json['name']+'", description = "'+data_json['description']+'",\n')
                    for i in range (len(data_json['values'])):
                        f.write('      '+data_json['powers'][i]+' = '+str(data_json['values'][i])+',\n')
                    f.write('   )')
                from .temp import tes
                tes()
                response_json['status'] = True
                log('user/roles', 'create', 0, str(0), {}, ss(request))
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_role(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                with open('user_handler/temp.py','w') as f:
                    print("write")
                    f.write('from user_handler.models_permission import CustomPermission')
                    f.write('\n')
                    f.write('def tes():\n')
                    f.write('   role = CustomPermission.objects.get(id = '+str(data_json['role_id'])+')\n')
                    f.write('   role.name = "'+data_json['name']+'"\n')
                    f.write('   role.description = "'+data_json['description']+'"\n')
                    for i in range (len(data_json['values'])):
                        f.write('   role.'+data_json['powers'][i]+' = '+str(data_json['values'][i])+'\n')
                    f.write('   role.save()')
                from .temp import tes
                tes()
                response_json['status'] = True
                log('user/role', 'update', 0, str(0), {}, ss(request))
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def assign_role(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "assign":
                user = CustomUserBase.objects.get(id = data_json['user_id'])
                role = CustomPermission.objects.get(id = data_json['role_id'])
                user.role = role
                user.save()
                log('user/role/assign', 'create', user.id, str(user), {'msg' : 'given power to object id','role_id': role.id}, ss(request))
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_role(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "delete":
                role = CustomPermission.objects.get(id=data_json['role_id'])
                x = role.id
                role.delete()
                log('user/role', 'delete', x, str(x), {}, ss(request))
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_logs(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                activites = UserActivities.objects.all()
                if data_json['filter'] == "multiple":
                    if data_json['filters']['user']:
                        activites = activites.filter( user__id = data_json['filters']['user']).order_by('-id')
                    if data_json['filters']['action']:
                        activites = activites.filter( action = data_json['filters']['action']).order_by('-id')
                        if data_json['filters']['date']:
                            if data_json['filters']['start_date']:
                                start_date = str_to_datetime(str(data_json['filters']['start_date']))
                                activites = activites.filter(log_time__gte = start_date).order_by('-log_time')
                            if data_json['filters']['end_date']:
                                end_date = str_to_datetime(str(data_json['filters']['end_date']))
                                activites = activites.filter(log_time__lte = end_date).order_by('-log_time')
                else:
                    pass
                response_json['count'] = len(activites)
                activites = activites[data_json['start'] : data_json['end']]
                response_json['logs'] = []
                for activity in activites:
                    x = UserActivitySerializer(activity).data
                    x['username'] = activity.user.username
                    x['first_name'] = activity.user.first_name
                    x['last_name'] = activity.user.last_name
                    x['email'] = activity.user.email
                    response_json['logs'].append(x)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


def send_email(code, email):
    template = get_template('password_reset_email.html')
    data = {
        'code' : code
    }
    html = template.render(data)
    res = send_mail("Password Reset for Mandala ERP", " DO ", settings.EMAIL_HOST_USER, [email], html_message=html)
    if res:
        return True
    else:
        raise Exception("Email can't be sent through.")


def forget_password(request):
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        email = data_json['email']
        try:
            user = CustomUserBase.objects.get(email = email)
        except:
            return JsonResponse({'status': False, 'error': 'You are not registed. Please sign up or contact admin.'})
        try:
            code = PasswordResetCode.objects.get(email = email)
            code.delete()
        except:
            pass
        code = create_unique_code(request, email)
        send_email(code, email)
        return JsonResponse({'status': True, 'msg': 'A code has been sent to your email. Please use the code to login.'})
    except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


def create_unique_code(request, email):
    code = random.randint(0, 999999)
    code = str(code).zfill(6)
    x = PasswordResetCode.objects.filter(code = code)
    if len(x) <=0:
        PasswordResetCode.objects.create(
            code = code,
            timestamp = django.utils.timezone.now(),
            ip = get_client_ip(request),
            email = email
        )
    else:
        create_unique_code(request)
    return code


def is_code_valid(code):
    try:
        code = PasswordResetCode.objects.get(code = code)
    except:
        return {'status':False, 'error' : 'Invalid Code.'}
    if code.timestamp + datetime.timedelta(minutes = 30) < django.utils.timezone.now():
        code.delete()
        return {'status':False, 'error' : 'Time Expired, please re-issue the code.'}
    return {'status':True}

def validate_code(request):
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        return JsonResponse(is_code_valid(data_json['code']))
    except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

def reset_password(request):
    try: 
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        x = is_code_valid(data_json['code'])
        if not x['status']:
            return JsonResponse(x)
        code = PasswordResetCode.objects.get(code = data_json['code'])
        user = CustomUserBase.objects.get(email = code.email)
        user.set_password(data_json['password'])
        user.save()
        return JsonResponse({'status':True})
    except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@require_http_methods(['POST'])
@bind
def get_notifications(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                response_json['notifications'] = []
                settings = NotificationSetting.objects.filter(roles_to_get_notified = user.role)
                notifications = []
                if data_json['read']:
                    for setting in settings:
                        for x in (Notification.objects.filter(model = setting.model, read = data_json['read']).order_by('-id')):
                            notifications.append(x)
                else:
                    for setting in settings:
                        for x in (Notification.objects.filter(model = setting.model, read = False).order_by('-id')):
                            notifications.append(x)
                        for x in (Notification.objects.filter(model = setting.model, read = True).order_by('-id')):
                            notifications.append(x)
                response_json['count'] = len(notifications)
                notifications = notifications[data_json['start']:data_json['end']]
                for notification in notifications:
                    response_json['notifications'].append(NotificationSerializer(notification).data)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def read_notification(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'read':
                for n_id in data_json['notifications_id']:
                    notification = Notification.objects.get(id = n_id)
                    notification.read = True
                    notification.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['GET'])
@bind
def get_settings(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            settings = Setting.objects.filter(is_active=True)[0]
            response_json['settings'] = SettingSerializer(settings).data
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def udpate_settings(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            settings = Setting.objects.filter(is_active=True)[0]
            old = settings
            if data_json['action'] == "update":
                if data_json['default_weight_unit']:
                    settings.default_weight_unit = data_json['default_weight_unit']
                if data_json['company']:
                    settings.company = data_json['company']
                if data_json['company_address']:
                    settings.company_address = data_json['company_address']
                if data_json['branch']:
                    settings.branch = data_json['branch']
                if data_json['branch_code']:
                    settings.branch_code = data_json['branch_code']
                if data_json['manufacturer']:
                    settings.manufacturer = data_json['manufacturer']
                if data_json['distributor']:
                    settings.distributor = data_json['distributor']
                if data_json['contact']:
                    settings.contact = data_json['contact']
                if data_json['manufacturer_website']:
                    settings.manufacturer_website = data_json['manufacturer_website']
                if data_json['change_fisal_year']:
                    settings.change_fisal_year = data_json['change_fisal_year']
                if data_json['stock_low_notification_on']:
                    settings.stock_low_notification_on = data_json['stock_low_notification_on']
                if data_json['manufacturer_address']:
                    settings.manufacturer_address = data_json['manufacturer_address']
                if data_json['pan_number']:
                    settings.pan_number = data_json['pan_number']
                settings.save()
            response_json['settings'] = SettingSerializer(settings).data
            response_json['status'] = True
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            log('user/settings', 'update', old.id, str(old),  SettingSerializer(old).data, user)
        
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

def get_user_data(user):
    temp = {}
    temp['username'] = user.username
    temp['first_name'] = user.first_name
    temp['last_name'] = user.last_name
    try:
        temp['profile_picture'] = user.profile.profile_image.url
    except:
        temp['profile_picture'] = None
    return temp

def notification_to_json(models):
    data = []
    for model in models:
        temp = NotificationSettingSerializer(model).data
        temp['roles'] = []
        for x in model.roles_to_get_notified.all():
            temp['roles'].append({
                'id' : x.id,
                'name' : x.name
            })
        data.append(temp)
    return data

@require_http_methods(['GET'])
@bind
def get_notification_settings(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            response_json['settings'] = notification_to_json(NotificationSetting.objects.all())
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_notification_settings(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                x = NotificationSetting.objects.get(id = data_json['notification_setting_id'])
                old = x
                x.roles_to_get_notified.clear()
                for x in data_json['roles']:
                    x.roles_to_get_notified.add(CustomPermission.objects.get(id = x))
                x.save()
                response_json['settings'] = NotificationSettingSerializer(x).data
            response_json['status'] = True
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            log('user/notification/settings', 'update', old.id, str(old),  NotificationSettingSerializer(old).data, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})




def logs_to_json(models):
    data = []
    for model in models:
        temp = ActivityLogSerializer(model).data
        temp['user_details'] = get_user_data(model.user)
        data.append(temp)
    return data

def login_to_json(models):
    data = []
    for model in models:
        temp = UserActivitiesSerializer(model).data
        temp['user_details'] = get_user_data(model.user)
        data.append(temp)
    return data



@require_http_methods(['POST'])
@bind
def get_activities_log(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                logs = ActivityLog.objects.filter()
                if data_json['fitler'] == "none":
                    logs = logs
                if data_json['filter'] == 'multiple':
                    if data_json['filters']['model']:
                        logs = logs.filter(model = data_json['filters']['model'])
                    if data_json['filters']['action']:
                        logs = logs.filter(action = data_json['filters']['action'])
                    if data_json['filters']['object_id']:
                        logs = logs.filter(object_id = data_json['filters']['object_id'])
                    if data_json['filters']['object_str']:
                        logs = logs.filter(object_str__icontains = data_json['filters']['object_str'])
                    if data_json['filters']['user']:
                        logs = logs.filter(user__id = data_json['filters']['user'])
                    if data_json['filters']['date_range']:
                        if data_json['filters']['date_from']:
                            logs = logs.filter(date__gte = str_to_datetime(data_json['filters']['date_from']))
                        if data_json['filters']['date_upto']:
                            logs = logs.filter(date__lte = str_to_datetime(data_json['filters']['date_upto']))
                logs = logs[data_json['start']:data_json['end']]
                response_json['logs'] = logs_to_json(logs)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_user_logs(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                logs = UserActivities.objects.filter()
                if data_json['filter'] == "none":
                    logs = logs 
                if data_json['filter'] == "multiple":
                    if data_json['filters']['action']:
                        logs = logs.filter(action = data_json['filters']['action'])
                    if data_json['filters']['user']:
                        logs = logs.filter(user__id = data_json['filters']['user'])
                    if data_json['filters']['date_range']:
                        if data_json['filters']['date_from']:
                            logs = logs.filter(log_time__gte = str_to_datetime(data_json['filters']['date_from']))
                        if data_json['filters']['date_upto']:
                            logs = logs.filter(log_time__lte = str_to_datetime(data_json['filters']['date_upto']))
                logs = logs[data_json['start']:data_json['end']]
                response_json['status'] = True
                response_json['logs'] = login_to_json(logs)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
