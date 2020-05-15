from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('auth', obtain_jwt_token),
    path('refresh', refresh_jwt_token),

    path('verify', views.csrf, name = 'get csrf token'),

    path('login',obtain_jwt_token),
    # path('logout', views.user_logout, name='user logout'),
    path('create', views.user_creation, name='Create New User'),
    path('get', views.users, name="get user data"),
    path('get/0', views.s_user, name='get user data'),
    path('current', views.get_current_user, name='get current user data'),    
]
