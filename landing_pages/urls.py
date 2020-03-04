from django.urls import path
from . import views
urlpatterns = [
    path('inventory/orders', views.purchase_orders, name = "purchase order Landing page"),
]

