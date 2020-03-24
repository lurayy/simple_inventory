import os, django 

os.environ.setdefault("DJANGO_SETTING_MODULE", "simple_im.settings")
django.setup()

import random
from faker import Faker
from user_handler.models import CustomUserBase, Vendor, Customer, Tax, Discount
from inventory.models import PurchaseOrderStatus, PurchaseOrder, ItemCatagory, Item, PurchaseItem, Place, Placement
from sales.models import Invoice, InvoiceItem

USER_COUNT = 20
VENDOR_COUNT = 50
CUSTOMER_COUNT = 100
TAX_COUNT = 50
DISCOUNT_COUNT = 50

ITEM_CATAGORY_COUNT = 20
ITEM_COUNT = 30

PLACE_COUNT = 50
#calculate placement from place and purchase_order_item


PURCHASE_ORDER_STATUS = 30
PURCHASE_ORDER_COUNT = 80
PURCHASE_ORDER_ITEM_COUNT = 240

INVOICE_COUNT = 50
INVOICE_ITEM_COUNT = 100

Faker.seed(22506)


## craete fake users
fake = Faker()

for _ in range(USER_COUNT):
    username = fake.last_name()
    email = fake.email()
    password = "testpassword123"
    user = CustomUserBase.objects.create_user(username, email, password)
    user.first_name = username
    user.last_name = fake.last_name()
    user.save()

users = CustomUserBase.objects.all()
for user in users:
    print(str(user))


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
for _ in range(CUSTOMER_COUNT):
    temp = Customer.objects.create(
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
