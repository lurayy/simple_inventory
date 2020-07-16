from django.contrib import admin
from .models import Tax, Discount
# Register your models here.
from .models_permission import CustomPermission
from .models import Profile,  UserActivities

admin.site.register(Tax)
admin.site.register(Discount)

admin.site.register(Profile)

admin.site.register(UserActivities)

admin.site.register(CustomPermission)
