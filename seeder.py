# import os, django 

# os.environ.setdefault("DJANGO_SETTING_MODULE", "simple_im.settings")
# django.setup()
import datetime

# import random
# from faker import Faker
# from user_handler.models import CustomUserBase, Vendor, Customer, Tax, Discount, CustomerCategory, Setting, NotificationSetting
# from inventory.models import PurchaseOrderStatus, PurchaseOrder, ItemCategory, Item, PurchaseItem, Place, Placement
# from sales.models import Invoice, InvoiceItem, InvoiceStatus, SalesSetting
# from payment.models import GiftCard, UniqueCard, GiftCardCategory
# from user_handler.models_permission import CustomPermission
# from payment.models import PaymentMethod
from user_handler.models import Setting, CustomPermission
# USER_COUNT = 0
# VENDOR_COUNT = 5
# CUSTOMER_COUNT = 10
# TAX_COUNT = 5
# DISCOUNT_COUNT = 5

# ITEM_CATAGORY_COUNT = 4
# ITEM_COUNT = 2

# PLACE_COUNT = 5
# GIFT_CARD_COUNT = 10
# CATEGORY = 5
#calculate placement from place and purchase_order_item

# Ledger_Count = 400

# PURCHASE_ORDER_STATUS = 3
# PURCHASE_ORDER_COUNT = 2
# PURCHASE_ORDER_ITEM_COUNT = 3

# INVOICE_COUNT = 5
# INVOICE_ITEM_COUNT = 10

# Faker.seed(22506)

permission = CustomPermission.objects.create(
    id = 1,
    name="super_role"
)
permission.save()

## craete fake users
# fake = Faker()

from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.create_superuser('admin', 'admin@myproject.com', 'pass')
admin.role = permission
admin.save()

Setting.objects.create(
    default_weight_unit = "kg",
    company = "Mandala IT",
    branch = "Pokhara",
    branch_code= "PKR",
    stock_low_notification_on = 10,
    change_fisal_year = datetime.datetime.now()
)

# print("________________________________ USER________________________")
# for _ in range(USER_COUNT):
#     username = fake.last_name()
#     email = fake.email()
#     password = "testpassword123"
#     user = CustomUserBase.objects.create_user(username, email, password)
#     user.first_name = username
#     user.last_name = fake.last_name()
#     user.role = permission
#     user.save()
# print('____________user___________________')
# users = CustomUserBase.objects.all()
# for user in users:
#     print(str(user))

# for x in range(2):
#     name = 'category_'+str(x)
#     temp = CustomerCategory(
#         name=name
#     )
#     temp.save()

# print('____________user___________________')
# x  = NotificationSetting.objects.create(
#     model = 'item'
# )
# x.roles_to_get_notified.add(user.role)

# print("--------------------------- Vendors -------------------------")
# ## Vendors 
# for _ in range(VENDOR_COUNT-1):
#     temp = Vendor.objects.create(
#         added_by = users[random.randint(0, len(users)-1)],
#         first_name = fake.first_name(),
#         last_name = fake.last_name(),
#         email = fake.email(),
#         website = "somefake@gmail.com",
#         tax_number = fake.ean8(),
#         phone1 = fake.phone_number(),
#         phone2 = fake.phone_number(),
#         address = fake.address()   
#     )
#     temp.save()
#     print (f'{temp} created.')

# print("--------------------------- Customer -------------------------")
# csutomer_category = CustomerCategory.objects.all()
# for _ in range(CUSTOMER_COUNT):
#     temp = Customer.objects.create(
#         first_name = fake.first_name(),
#         last_name = fake.last_name(),
#         email = fake.email(),
#         website = "somefake@gmail.com",
#         tax_number = fake.ean8(),
#         phone1 = fake.phone_number(),
#         phone2 = fake.phone_number(),
#         address = fake.address(),
#         category = csutomer_category[random.randint(0,1)]     
#     )
#     temp.save()
#     print (f'{temp} created.')

# print("--------------------------- Tax -------------------------")
# for _ in range(TAX_COUNT):
#     temp = Tax.objects.create(
#         name= fake.first_name(),
#         rate = random.randint(0,50),
#         tax_type = 'normal'
#     )
#     temp.save()
#     print (f'{temp} created.')

# vat = Tax.objects.create(
#     name = 'VAT',
#     rate = 13,
#     tax_type = 'percent'
# )

# print("--------------------------- Discount -------------------------")
# for _ in range(DISCOUNT_COUNT):
#     temp = Discount.objects.create(
#         name= fake.first_name(),
#         code = fake.last_name(),
#         rate = random.randint(0,50),
#         discount_type = 'percent'
#     )
#     temp.save()
#     print (f'{temp} created.')


# print("--------------------------- PurchaseOrderStatus -------------------------")
# temp = PurchaseOrderStatus.objects.create(
#     name = "Completed",
#     is_end = True
# )
# temp.save()
# temp = PurchaseOrderStatus.objects.create(
#     name = "Draft",
#     is_end = False
# )
# temp.save()
# temp = PurchaseOrderStatus.objects.create(
#     name = "Processing",
#     is_end = False
# )
# temp.save()


# print("--------------------------- ItemCategory -------------------------")
# for _ in range(ITEM_CATAGORY_COUNT):
#     temp = ItemCategory.objects.create(
#         name = fake.first_name()
#     )
#     temp.save()
#     print (f'{temp} created.')

# print("--------------------------- Item -------------------------")
# global_temp = ItemCategory.objects.all()
# for _ in range(ITEM_COUNT):
#     temp = Item.objects.create(
#         name = fake.first_name(),
#         category = global_temp[random.randint(0, len(global_temp)-1)],
#         stock = 0,
#         sold = 0,
#         barcode = random.randint(0000, 9999),
#         weight = random.randint(0000, 9999),
#         weight_unit = "kg",
#         sales_price = fake.random_number(digits=None, fix_len=False)
#     )
#     temp.save()
#     print (f'{temp} created.')

# temp = Place.objects.create(
#     name = 'Default',
#     is_default = True
# )

# name = [
#     "Draft",
#     "Done"
# ]
# for i in range(2):
#     temp = InvoiceStatus.objects.create(
#         name = name[i]
#     )
#     temp.save()

# temp.is_sold = True
# temp.save()


# temp = CustomUserBase.objects.get(id=1)
# role = CustomPermission.objects.get(id=1)
# temp.role = role
# temp.save()

# from payment.models import Payment
# methods = PaymentMethod.objects.all()

# headers = ['credit','pre-paid','cash', 'transfer','bank']
# for head in headers:
#     temp = PaymentMethod.objects.create(
#         name = head, 
#         header = head,
#     )

# methods = PaymentMethod.objects.all()
# for order in PurchaseOrder.objects.all():
#     pay = Payment.objects.create(
#         purchase_order = order,
#         amount = order.paid_amount,
#         method = methods[random.randint(0, len(methods)-1)],
#     )
#     pay.save()

# from accounting.models import Account, AccountType

# SalesSetting.objects.create(
#     default_place_to_sold_from = Place.objects.get(name='Default'),
#     default_vat_tax = vat,
#     default_customer_qk_sales = Customer.objects.get(id=2)
# )

# types = []
# headers = ['assets','expense','draw', 'liabilities','revenue', 'equity']
# for head in headers:
#     temp = AccountType.objects.create(
#         name = head, 
#         header = head,
#     )
#     types.append(temp)

# for ac in types:
#     Account.objects.create(
#         account_type = ac,
#         name = ac.header,
#         opening_date = datetime.datetime.now(),
#         opening_balance = 0,
#         current_amount = 0,
#         credit = 0
#     )

# NotificationSetting.objects.create(
#     model = 'item'
# )

# NotificationSetting.objects.create(
#     model = 'purchase_order'
# )
# NotificationSetting.objects.create(
#     model = 'invoice'
# )

from user_handler.models import Country
import json
with open('countires.json', 'r') as con_file:
    data = json.load(con_file)
    for con in data:
        print(con['alpha2'])
        Country.objects.create(
            alpha2 = con['alpha2'],
            alpha3 = con['alpha3'],
            num = int(con['num']),
            phone_code = int(con['phone_code']),
            name = (con['name']),
            continent = (con['continent'])
            
        )

