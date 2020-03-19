from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('super/', admin.site.urls),
    path('apiv1/sales/', include('sales.urls')),
    path('apiv1/inventory/', include('inventory.urls')),
    path('apiv1/users/', include('user_handler.urls')),
    path('', TemplateView.as_view(template_name='build/index.html')),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='build/index.html'))
]
