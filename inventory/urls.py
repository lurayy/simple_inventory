from django.urls import path
from . import views
urlpatterns = [
    path('porders', views.purchase_orders, name="GET json of purchase orders"),
    path('porders/<int:id>', views.purchase_order, name='Get data ofa pruchase order')
]

