from django.urls import path
from . import views
urlpatterns = [
    path('staffs', views.staff_list, name = 'get staff lists'),

    path('purchaseorders', views.purchase_orders, name='get purhcase order list'),
    
    path('purchaseorders/create', views.create_purchase_order, name='create order list'),
    path('purchaseorder/<int:id>', views.edit_purchase_order, name='edit purchase order'),

    
    path('vendors', views.vendors, name = 'get vendors'),
    path('items', views.items, name = 'get items lists'),
    path('places',views.places, name='places'),
    
    path('invoices',views.invoices, name='places'),
    path('customers',views.customers, name='places'),
    
]

