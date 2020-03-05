from django.urls import path
from . import views
urlpatterns = [
    path('porders', views.purchase_orders, name="GET json of purchase orders"),
    path('porders/<int:id>', views.purchase_order, name='Get data ofa pruchase order'),
    path('vendors', views.vendors, name="GET json of purchase orders"),
    path('vendors/<int:id>', views.vendor, name='Get data ofa pruchase order'),
    path('items', views.items, name="GET json of purchase orders"),
    path('items/<int:id>', views.item, name='Get data ofa pruchase order'),
]

