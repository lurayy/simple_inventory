from django.contrib import admin
from .models import CustomUserBase, Vendor, PurchaseOrder, PurchaseItem, Item, Place, Placement, ItemCategory, PurchaseOrderStatus, ItemImage
# Register your models here.

admin.site.register(ItemCategory)
admin.site.register(CustomUserBase)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(Place)
admin.site.register(Placement)
admin.site.register(ItemImage)

admin.site.register(PurchaseOrder)

admin.site.register(PurchaseOrderStatus)
admin.site.register(PurchaseItem)

admin.site.site_header = "Mandala Management"