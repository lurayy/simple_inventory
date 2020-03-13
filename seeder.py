import faker
from user_handler.models import CustomUserBase, Vendor, Customer, Tax, Discount

users = CustomUserBase.objects.filter(is_active=True)

for _ in range(50):
    vendor = Vendor.objects.create()
