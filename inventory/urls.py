from django.urls import path
from . import views
urlpatterns = [
    path('status/porders', views.purchase_order_statuss, name='get purchase order status'),

    path('porders', views.purchase_orders, name="GET and add  purchase orders"),
    path('porder', views.purchase_order, name='edit  pruchase order'),
    path('porders/delete', views.delete_purchase_orders, name = "Delete purhcase orders"),

    path('pitems', views.purchase_items, name='add a purchase item'),
    path('pitem', views.purchase_item, name='update/ get pitem'),
    path('pitems/delete', views.delete_purchase_items, name="delete purchase item"),

    path('vendors', views.vendors, name="GET and add vendors"),
    path('vendor', views.vendor, name='edit and get  data of a vendor'),
    path('vendors/delete', views.delete_vendors, name="delete vendors"),

    path('items', views.items, name="GET and add items "),
    path('item', views.item, name='edit data of item'),
    path('items/delete', views.delete_items, name="delete items "),

    path('places', views.places, name="GET and add places"),
    path('place', views.place, name='edit places '),
    path('places/delete', views.delete_places, name="delete places"),

    path('places/assign', views.assign_place, name="placement curd"),

    path('items/catagories', views.item_catagories, name = "get/add "),
    path('items/catagory', views.item_catagory, name = "get/edit "),
    path('items/catagories/delete', views.delete_item_catagories, name = "delete"),
    
    
]