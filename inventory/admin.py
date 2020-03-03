from django.contrib import admin
from .models import CustomUserBase, Vendor, PurchaseOrder, PurchaseItem, Item, Place, Placement
# Register your models here.

admin.site.register(CustomUserBase)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(Place)
admin.site.register(Placement)

admin.site.register(PurchaseOrder)
admin.site.register(PurchaseItem)