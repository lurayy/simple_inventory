from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super/', admin.site.urls),
    path('', admin.site.urls),
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/user/', include('user_handler.urls')),
    path('api/v1/payment/', include('payment.urls')),
    path('api/v1/accounting/', include('accounting.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
