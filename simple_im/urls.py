from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os 
import json
from simple_im.views import index
from django.conf.urls.static import static


urlpatterns = [
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/user/', include('user_handler.urls')),
    path('api/v1/payment/', include('payment.urls')),
    path('api/v1/accounting/', include('accounting.urls')),
    path('api/v2/sales/', include('v2.urls')),
    path('super/', admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns.append(
    re_path(r'^(?:.*)/?$',  index, name = " entry point"))  