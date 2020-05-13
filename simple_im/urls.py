from django.contrib import admin
from django.urls import path, include, re_path
from user_handler.views import entry_point
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super/', admin.site.urls),
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/user/', include('user_handler.urls')),
    path('api/v1/payment/', include('payment.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns.append(
#     re_path(r'^(?:.*)/?$',  entry_point, name = " entry point"))