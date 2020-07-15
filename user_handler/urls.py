from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('auth', obtain_jwt_token),
    path('refresh', refresh_jwt_token),

    path('verify', views.csrf, name = 'get csrf token'),

    path('login',obtain_jwt_token),

    path('add', views.user_creation, name='Create New User'),
    path('list', views.get_multiple_user, name="get user data"),
    path('update', views.update_user),
    path('roles/get', views.get_multiple_roles),
    path('delete', views.delete_user),

    path('current', views.get_current_user, name='get current user data'),    
]
