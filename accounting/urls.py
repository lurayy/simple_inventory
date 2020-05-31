from django.urls import path
from . import views

urlpatterns = [
   path('accounts/get', views.get_multiple_accounts),
   path('account/add', views.add_new_account),
   path('account/get', views.get_account_details),
   path('accounts/delete', views.delete_accounts),
]