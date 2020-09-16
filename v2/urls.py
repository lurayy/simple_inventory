from . import views

from django.urls import path

urlpatterns = [
    path('invoice/new', views.create_invoice_all),
]