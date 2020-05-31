import os, django 

os.environ.setdefault("DJANGO_SETTING_MODULE", "simple_im.settings")
django.setup()
import datetime

import random
from faker import Faker
from user_handler.models import CustomUserBase, Vendor, Customer, Tax, Discount, CustomerCategory
from inventory.models import PurchaseOrderStatus, PurchaseOrder, ItemCatagory, Item, PurchaseItem, Place, Placement
from sales.models import Invoice, InvoiceItem
from payment.models import GiftCard, UniqueCard, GiftCardCategory
from user_handler.models_permission import CustomPermission
from accounting.models import EntryType, LedgerEntry, Account
USER_COUNT = 2
VENDOR_COUNT = 5
CUSTOMER_COUNT = 10
TAX_COUNT = 5
DISCOUNT_COUNT = 5

ITEM_CATAGORY_COUNT = 4
ITEM_COUNT = 8

PLACE_COUNT = 5
GIFT_CARD_COUNT = 10
CATEGORY = 5
#calculate placement from place and purchase_order_item

Ledger_Count = 400

PURCHASE_ORDER_STATUS = 3
PURCHASE_ORDER_COUNT = 5
PURCHASE_ORDER_ITEM_COUNT = 25

INVOICE_COUNT = 5
INVOICE_ITEM_COUNT = 10

Faker.seed(22506)

permission = CustomPermission.objects.create(
    name="super_role"
)
permission.save()

## craete fake users
fake = Faker()

for _ in range(USER_COUNT):
    username = fake.last_name()
    email = fake.email()
    password = "testpassword123"
    user = CustomUserBase.objects.create_user(username, email, password)
    user.first_name = username
    user.last_name = fake.last_name()
    user.role = permission
    user.save()

users = CustomUserBase.objects.all()
for user in users:
    print(str(user))

for x in range(2):
    name = 'category_'+str(x)
    temp = CustomerCategory(
        name=name
    )
    temp.save()


print("--------------------------- Vendors -------------------------")
## Vendors 
for _ in range(VENDOR_COUNT-1):
    temp = Vendor.objects.create(
        added_by = users[random.randint(0, len(users)-1)],
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        email = fake.email(),
        website = "somefake@gmail.com",
        tax_number = fake.ean8(),
        phone1 = fake.phone_number(),
        phone2 = fake.phone_number(),
        address = fake.address()   
    )
    temp.save()
    print (f'{temp} created.')

print("--------------------------- Customer -------------------------")
csutomer_category = CustomerCategory.objects.all()
for _ in range(CUSTOMER_COUNT):
    temp = Customer.objects.create(
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        email = fake.email(),
        website = "somefake@gmail.com",
        tax_number = fake.ean8(),
        phone1 = fake.phone_number(),
        phone2 = fake.phone_number(),
        address = fake.address(),
        category = csutomer_category[random.randint(0,1)]     
    )
    temp.save()
    print (f'{temp} created.')

print("--------------------------- Tax -------------------------")
for _ in range(TAX_COUNT):
    temp = Tax.objects.create(
        name= fake.first_name(),
        rate = random.randint(0,50),
        tax_type = 'normal'
    )
    temp.save()
    print (f'{temp} created.')


print("--------------------------- Discount -------------------------")
for _ in range(DISCOUNT_COUNT):
    temp = Discount.objects.create(
        name= fake.first_name(),
        code = fake.last_name(),
        rate = random.randint(0,50),
        discount_type = 'percent'
    )
    temp.save()
    print (f'{temp} created.')

print("--------------------------- PurchaseOrderStatus -------------------------")
temp = PurchaseOrderStatus.objects.create(
    name = "Completed",
    is_end = True
)
temp.save()
temp = PurchaseOrderStatus.objects.create(
    name = "Draft",
    is_end = False
)
temp.save()
temp = PurchaseOrderStatus.objects.create(
    name = "Processing",
    is_end = False
)
temp.save()


print("--------------------------- ItemCatagory -------------------------")
for _ in range(ITEM_CATAGORY_COUNT):
    temp = ItemCatagory.objects.create(
        name = fake.first_name()
    )
    temp.save()
    print (f'{temp} created.')

print("--------------------------- Item -------------------------")
global_temp = ItemCatagory.objects.all()
for _ in range(ITEM_COUNT):
    temp = Item.objects.create(
        name = fake.first_name(),
        catagory = global_temp[random.randint(0, len(global_temp)-1)],
        stock = 0,
        sold = 0,
        sales_price = fake.random_number(digits=None, fix_len=False)
    )
    temp.save()
    print (f'{temp} created.')

print("--------------------------- Purchase Order -------------------------")
global_temp2 = PurchaseOrderStatus.objects.all()
global_temp = Vendor.objects.all()
for i in range(PURCHASE_ORDER_COUNT):
    temp = PurchaseOrder.objects.create(
        added_by = users[random.randint(0,len(users)-1)],
        vendor = global_temp[random.randint(0, len(global_temp)-1)],
        invoiced_on = fake.date_time(tzinfo=None, end_datetime=None),
        completed_on = fake.date_time(tzinfo=None, end_datetime=None),
        status = global_temp2[random.randint(0, len(global_temp2)-1)],
        total_cost = 0
    )
    temp.save()
    print (f'{i} of {PURCHASE_ORDER_COUNT}')

print("--------------------------- Purchase Order Item -------------------------")
global_temp = Item.objects.all()
STATUS_S = ['delivered', 'incomplete', 'addedtocirculation']
global_temp2 = PurchaseOrder.objects.all()
for i in range(PURCHASE_ORDER_COUNT-1):
    purchase_order = global_temp2[i]
    item_number = random.randint(0,10)
    for _ in range(item_number):
        temp = PurchaseItem.objects.create(
            item = global_temp[random.randint(0, len(global_temp)-1)],
            purchase_order = purchase_order,
            quantity = random.randint(100, 400),
            sold = 0,
            purchase_price = random.randint(500, 50000),
            defective = random.randint(0, 100),
            status = STATUS_S[random.randint(0, len(STATUS_S)-1)]
        )
        temp.save()
        temp.save()
    purchase_order.save()


for order in PurchaseOrder.objects.all():
    temp = PurchaseOrderStatus.objects.get(is_end=True)
    order.status = temp
    order.save()
    order.save()
    print(f'{order} changed to {order.status}')




# print("--------------------------- Invoice -------------------------")
# global_temp = Customer.objects.all()
# STATUS_S = ['sent', 'due', 'paid', 'completed', 'shiped']
# for _ in range(INVOICE_COUNT):
#     temp = Invoice.objects.create(
#         added_by = users[random.randint(0,len(users)-1)],
#         customer = global_temp[random.randint(0, len(global_temp)-1)],
#         invoiced_on = fake.date_time(tzinfo=None, end_datetime=None),
#         due_on = fake.date_time(tzinfo=None, end_datetime=None),
#         paid_amount = 0,
#         tax_total = 0,
#         order_number = fake.ean8(),
#         status = STATUS_S[random.randint(0,4)]
#     )
#     temp.save()
#     print (f'{temp} created.')



# print("--------------------------- Invoice Items -------------------------")
# invoices = Invoice.objects.all()
# purchase_items = PurchaseItem.objects.all()
# discounts = Discount.objects.all()
# taxes = Tax.objects.all()
# STATUS_S = ['sent', 'due', 'paid', 'completed', 'shiped']
# for x in range(INVOICE_COUNT-1):
#     invoice = invoices[x]
#     purchase_item = purchase_items[random.randint(0, len(purchase_items)-1)]
#     print(purchase_item.stock)
#     sold_from = Placement.objects.get(purchase_item=purchase_item).placed_on
#     temp = InvoiceItem.objects.create(
#         purchase_item = purchase_item,
#         item = purchase_item.item,
#         sold_from = sold_from,
#         invoice = invoice,
#         quantity = random.randint(5,10),
#         price = random.randint(0,25000),
#         tax_total = 0,
#         sub_total = 0,
#         discount_amount = 0,
#         total_without_discount = 0,
#         total = 0,
#     )
#     for dis in discounts:
#         if bool(random.getrandbits(1)):
#             temp.discount.add(dis)
#     for tax in taxes:
#         if bool(random.getrandbits(1)):
#             temp.taxes.add(tax)
#     temp.save()
#     temp.save()
#     print("added  ",x)
#     invoice.status = STATUS_S[random.randint(0, len(STATUS_S)-1)]
#     invoice.save()

# for i in range (CATEGORY):
#     name = "category_"+str(i)
#     temp = GiftCardCategory.objects.create(
#         name= name
#     )
#     print(str(temp))
#     temp.save()

# category = GiftCardCategory.objects.all()

# for _ in range (GIFT_CARD_COUNT):
#     temp = GiftCard.objects.create(
#         name = fake.last_name(),
#         category = category[random.randint(0,len(category)-1)],
#         code = fake.first_name(),
#         rate = random.randint(0,50),
#         count_limit = random.randint(5,100),
#         is_limited = True,
#         has_unique_codes = True,
#         is_active = True
#     )
#     temp.save()
#     print (temp.name)


headers = [
        'assets','liabilities','revenue','expense','draw','equity'
    ]

headers_obj = []
for header in headers:
    temp = EntryType.objects.create(
        name = header,
        header = header,
    )
    temp.save()
    headers_obj.append(temp)

# for i in range(Ledger_Count):
#     temp = LedgerEntry.objects.create(
#         entry_type = headers_obj[random.randint(0, len(headers_obj)-1)],
#         date = datetime.datetime.now(),
#         amount = random.randint(10, 100000)
#     )
#     temp.save()
#     print('entry: ',i)

temp = CustomUserBase.objects.get(id=1)
role = CustomPermission.objects.get(id=1)
temp.role = role
temp.save()
