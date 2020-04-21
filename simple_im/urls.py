from django.contrib import admin
from django.urls import path, include, re_path
from user_handler.views import entry_point

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super/', admin.site.urls),
    path('apiv1/sales/', include('sales.urls')),
    path('apiv1/inventory/', include('inventory.urls')),
    path('apiv1/users/', include('user_handler.urls')),
    path('', entry_point, name = " entry point"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(
    re_path(r'^(?:.*)/?$',  entry_point, name = " entry point"))