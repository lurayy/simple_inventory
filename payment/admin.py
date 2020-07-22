from django.contrib import admin
from .models import GiftCardCategory, GiftCard, UniqueCard, PaymentMethod, Payment, GiftCardRedeem, Settings

admin.site.register(GiftCard)

admin.site.register(UniqueCard)
admin.site.register(GiftCardCategory)

admin.site.register(Payment)
admin.site.register(GiftCardRedeem)
admin.site.register(Settings)
admin.site.register(PaymentMethod)