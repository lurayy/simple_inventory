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
    path('vendor/get', views.get_vendor_details, name="get single vendor"),
    
    path('items/get', views.get_multiple_items, name="get multiple items"),
    path('item/add', views.add_new_item, name="add new item"),
    path('item/get', views.get_item_details, name="get item details"),
    path('item/update', views.update_item, name='update item detail'),
    path('items/delete', views.delete_items, name= "delete item"),

    path('items/categories/get', views.get_multiple_item_catagories, name='item categories'),
    path('items/category/add', views.add_new_item_catagory, name=" item category add"),
    path('items/category/get', views.get_item_catagory_details, name="get item category single"),
    path('items/categories/delete', views.delete_item_catagories, name="dlete "),
    path('items/category/update', views.update_item_category, name="update "),

    path('places/get',views.get_multiple_places, name=" "),
    path('place/add',views.add_new_place, name=" "),
    path('place/update',views.update_place, name=" "),
    path('places/delete',views.delete_places, name=" "),

    path('placements/assign', views.assign_place, name="placement curd"),


    path('placements/get', views.get_placements, name = 'placements'),

    path('export',views.export_inventory, name='Export data'),   

    path('purchaseitems/get',views.get_mulitple_purchase_items, name="purchae items"),
    path('purchaseitem/add',views.add_new_purchase_item, name="purchae items"),
    path('purchaseitems/delete',views.delete_purchase_items, name="purchae items"),
    path('purchaseitem/get',views.get_purchase_item_details, name="purchae items"),
    path('purchaseitem/update',views.update_purchase_item, name="purchae items"),
]