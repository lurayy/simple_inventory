from django.urls import path
from . import views
urlpatterns = [
    path('purchaseorders/status', views.purchase_order_statuss, name='get purchase order status'),

    path('purchaseorders/get', views.get_multiple_purchase_orders, name="GET \  purchase orders"),
    path('purchaseorder/add', views.add_new_purchase_order, name = 'add new purchase order'),
    path('purchaseorder/get', views.get_purchase_order_details, name='get single purchase order details'),
    path('purchaseorder/update', views.update_purchase_order, name='update purchase order'),
    path('purchaseorders/delete', views.delete_purchase_orders, name = "delete multiple purchase orders"),
    
    path('vendors/get', views.get_multiple_vendors, name="GET vendors"),
    path('vendor/add', views.add_new_vendor, name='add new vendor'),
    path('vendors/delete', views.delete_vendors, name="delete vendors"),
    path('vendor/update', views.update_vendor, name='update vendor'),   

    path('items/get', views.get_multiple_items, name="get multiple items"),
    path('item/add', views.add_new_item, name="add new item"),
    path('item/get', views.get_item_details, name="get item details"),
    path('item/update', views.update_item, name='update item detail'),
    path('items/delete', views.delete_items, name= "delete item"),


    path('places', views.places, name="GET and add places"),
    path('place', views.place, name='edit places '),
    path('places/delete', views.delete_places, name="delete places"),

    path('places/assign', views.assign_place, name="placement curd"),

    path('items/catagories', views.item_catagories, name = "get/add "),
    path('items/catagory', views.item_catagory, name = "get/edit "),
    path('items/catagories/delete', views.delete_item_catagories, name = "delete"),

    path('placements', views.placements, name = 'placements'),

    path('export',views.handle_export, name='Export data'),   
]