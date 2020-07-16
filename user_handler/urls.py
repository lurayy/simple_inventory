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

    path('logout', views.user_logout),

    path('current', views.get_current_user, name='get current user data'),    
]
