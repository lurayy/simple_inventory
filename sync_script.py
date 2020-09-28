import os, django 

os.environ.setdefault("DJANGO_SETTING_MODULE", "simple_im.settings")
django.setup()
from sales.models import Invoice, sync_with_ird

invoices = Invoice.objects.filter(status__is_sold = True, is_synced_with_ird = False)
print("Syncing , ",len(invoices))
for invoice in  invoices:
    sync_with_ird(invoice)

