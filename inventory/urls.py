from django.urls import path
from . import views
urlpatterns = [
    path('porders', views.purchase_orders, name="GET and add  purchase orders"),
    path('porders/<int:id>', views.purchase_order, name='edit  pruchase order'),
    path('porders/delete', views.delete_purchase_orders, name = "Delete purhcase orders"),

    path('vendors', views.vendors, name="GET and add vendors"),
    path('vendors/<int:id>', views.vendor, name='edit  data of a vendor'),
    path('vendors/delete', views.delete_vendors, name="delete vendors"),

    path('items', views.items, name="GET and add items "),
    path('items/<int:id>', views.item, name='edit data of item'),
    path('items/delete', views.delete_items, name="delete items "),

    path('places', views.places, name="GET and add places"),
    path('places/<int:id>', views.place, name='edit places '),
    path('places/delete', views.delete_places, name="delete places"),

    path('places/assign', views.assign_place, name="placement curd"),
]