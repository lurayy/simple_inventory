from .models import Invoice, InvoiceItem 
from user_handler.models import Customer, CustomUserBase
from .serializers import InvoiceSerializer, InvoiceItemSerializer, CustomerSerializer
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
        temp['sold_from_name'] = str(Place.objects.get(id=id=temp['sold_from']))
        data.append(temp)
    return data

