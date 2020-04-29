from .models import Invoice, InvoiceItem 
from user_handler.models import Customer, CustomUserBase
from .serializers import InvoiceSerializer, InvoiceItemSerializer, CustomerSerializer, TaxSerializer, DiscountSerializer, CustomerCategorySerializer
from inventory.models import PurchaseItem, Place, Item

def invoices_to_json(models):
    data = []
    for model in models:
        temp = (InvoiceSerializer(model).data)
        temp['customer_name'] = str(Customer.objects.get(id=temp['customer']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        temp['status_name'] = str(model.status.name)
        data.append(temp)
    return data

def invoice_items_to_json(items):
    data = []
    for item in items:
        temp = InvoiceItemSerializer(item).data
        temp['item_name'] = str(Item.objects.get(id=temp['item']))
        temp['sold_from_name'] = str(Place.objects.get(id=temp['sold_from']))
        temp['applied_tax'] = []
        temp['applied_discount'] = []
        for tax in item.taxes.all().filter(is_active=True):
            temp['applied_tax'].append(TaxSerializer(tax).data)
        for discount in item.discount.all().filter(is_active=True):
            temp['applied_discount'].append(DiscountSerializer(discount).data)
        data.append(temp)
    return data
    
def discounts_to_json(discounts):
    data = []
    for discount in discounts:
        temp = DiscountSerializer(discount).data
        data.append(temp)
    return data

def taxes_to_json(taxes):
    data = []
    for tax in taxes:
        temp = TaxSerializer(tax).data
        data.append(temp)
    return data


def customers_to_json(customers):
    data = []
    for customer in customers:
        temp = CustomerSerializer(customer).data
        if(temp['middle_name']):
            temp['name'] = str(temp['first_name']) + " " + str(temp['middle_name'] ) + " "+ str(temp['last_name'])
        else:
            temp['name'] = str(temp['first_name']) + " "+str(temp['last_name'])
        temp['category_str'] = str(customer.category)
        data.append(temp)
    return data

def categories_to_json(categories):
    data = []
    for category in categories:
        temp = CustomerCategorySerializer(category).data
        data.append(temp)
    return data