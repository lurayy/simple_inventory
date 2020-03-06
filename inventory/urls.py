from django.urls import path
from . import views
urlpatterns = [
    path('porders', views.purchase_orders, name="GET json of purchase orders"),
    path('porders/<int:id>', views.purchase_order, name='Get data ofa pruchase order'),

    path('vendors', views.vendors, name="GET json of purchase orders"),
    path('vendors/<int:id>', views.vendor, name='Get data ofa pruchase order'),
    path('vendors/delete', views.delete_vendors, name="delete vendor"),

    path('items', views.items, name="GET json of purchase orders"),
    path('items/<int:id>', views.item, name='Get data ofa pruchase order'),
    path('items/delete', views.delete_items, name="delete item"),

    path('places', views.places, name="GET json of purchase orders"),
    path('places/<int:id>', views.place, name='Get data ofa pruchase order'),
    path('places/delete', views.delete_places, name="delete vendor"),

    path('places/assign', views.assign_place, name="placement curd"),
]