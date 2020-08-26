from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('auth', views.user_token),
    path('refresh', refresh_jwt_token),

    path('verify', views.csrf, name = 'get csrf token'),

    path('add', views.user_creation, name='Create New User'),
    path('list', views.get_multiple_user, name="get user data"),
    path('update', views.update_user),
    path('delete', views.delete_user),

    path('roles/get', views.get_multiple_roles),
    path('role/get', views.get_role_details),
    path('role/valid', views.valid_power),
    path('role/add',views.add_new_role),
    path('role/assign', views.assign_role),
    path('role/delete', views.delete_role),
    path('role/update', views.update_role),

    path('logtime', views.log_logout_time),

    path('logs/get', views.get_logs),

    path('password/forget', views.forget_password),
    path('password/code/validate', views.validate_code),
    path('password/reset', views.reset_password ),

    path('current', views.get_current_user, name='get current user data'),    
    
    path('settings/get', views.get_settings),
    path('settings/update', views.udpate_settings),
    path('notifications/get', views.get_notifications),
    path('notification/read', views.read_notification),
    path('notification/settings/get', views.get_notification_settings),
    path('notification/settings/update', views.update_notification_settings),

    path('activities/logs', views.get_activities_log),
    
    path('auth/logs', views.get_user_logs),

    path('backup/create', views.make_backup),
    path('backups/get',views.get_backup_list),
    path('backup/download', views.download_backup)
]
