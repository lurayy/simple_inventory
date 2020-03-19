from django.urls import path
from . import views
urlpatterns = [
    path('porders', views.purchase_orders, name="GET and add  purchase orders"),
    path('porders/<int:id>', views.purchase_order, name='edit  pruchase order'),
    path('porders/delete', views.delete_purchase_orders, name = "Delete purhcase orders"),

    path('vendors/get', views.vendors, name="GET and add vendors"),
    path('vendor/0', views.vendor, name='edit  data of a vendor'),
    path('vendor/create', views.vendors, name="add vendors"),
    path('vendors/delete', views.delete_vendors, name="delete vendors"),

    path('items', views.items, name="GET and add items "),
    path('items/0', views.item, name='edit data of item'),
    path('items/delete', views.delete_items, name="delete items "),

    path('places', views.places, name="GET and add places"),
    path('places/0', views.place, name='edit places '),
    path('places/delete', views.delete_places, name="delete places"),

    path('places/assign', views.assign_place, name="placement curd"),

    path('status',views.purchase_order_statuss, name="get status")
]