from django.urls import path
from . import views
urlpatterns = [
    path('verify', views.csrf, name = 'get things'),
    path('login',views.user_login, name = 'User Login'),
    path('logout', views.user_logout, name='user logout'),
    path('create', views.user_creation, name='Create New User'),
    path('get', views.users, name="get user data"),
    path('get/0', views.s_user, name='get user data'),
    path('current', views.get_current_user, name='get current user data'),    
]
