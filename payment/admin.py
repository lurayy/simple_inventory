from django.contrib import admin
from .models import GiftCardCategory, GiftCard, UniqueCard

admin.site.register(GiftCard)

admin.site.register(UniqueCard)
admin.site.register(GiftCardCategory)