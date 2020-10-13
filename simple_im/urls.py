from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os 
import json
from simple_im.views import index

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

urlpatterns.append(
    re_path(r'^(?:.*)/?$',  index, name = " entry point"))

# x = False
# with open('settings.json') as extra_settings_file:
#     x = json.load(extra_settings_file)['run_migrations']
#     print("asdadsf ",x)
# if x:
#     with open('settings.json','r') as ex:
#         data = {
#             'run_migrations' : False
#         }
#         json.dump(data, ex)
        
    #  os.system('./seeder.sh')

# from sales.models import Invoice, sync_with_ird
# invoices = Invoice.objects.filter(status__is_sold = True, is_synced_with_ird = False)
# print("Syncing , ",len(invoices))
# for invoice in  invoices:
#     sync_with_ird(invoice)
