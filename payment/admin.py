from django.contrib import admin
from .models import GiftCardCategory, GiftCard, UniqueCard, PaymentMethod, Payment

admin.site.register(GiftCard)

admin.site.register(UniqueCard)
admin.site.register(GiftCardCategory)

admin.site.register(Payment)

admin.site.register(PaymentMethod)