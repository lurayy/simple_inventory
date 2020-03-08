from django.urls import path
from . import views
urlpatterns = [
    path('login',views.user_login, name = 'User Login'),
    path('',views.dashboard, name = 'Dashbaord'),
    path('logout', views.user_logout, name='user logout'),
    path('user/create', views.user_creation, name='Create New User'),
    path('users', views.users, name="get user data"),
    path('user/<int:id>', views.s_user, name='get user data')
]
