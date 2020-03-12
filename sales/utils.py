from .models import Invoice, InvoiceItem 
from user_handler.models import Customer, CustomUserBase
from .serializers import InvoiceSerializer, InvoiceItemSerializer, CustomerSerializer, TaxSerializer, DiscountSerializer
from inventory.models import PurchaseItem, Place, Item

def invoices_to_json(models):
    data = []
    for model in models:
        temp = (InvoiceSerializer(model).data)
        temp['customer_name'] = str(Customer.objects.get(id=temp['customer']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
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

