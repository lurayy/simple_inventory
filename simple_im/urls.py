from django.contrib import admin
from django.urls import path, include, re_path
from user_handler.views import entry_point

urlpatterns = [
    path('super/', admin.site.urls),
    path('apiv1/sales/', include('sales.urls')),
    path('apiv1/inventory/', include('inventory.urls')),
    path('apiv1/users/', include('user_handler.urls')),
    path('', entry_point, name = " entry point"),
    re_path(r'^(?:.*)/?$',  entry_point, name = " entry point")
]
