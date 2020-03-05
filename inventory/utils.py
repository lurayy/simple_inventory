from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
from django.forms.models import model_to_dict 
from user_handler.models import Vendor, CustomUserBase
from .serializers import PurchaseOrderSerializer, PurchaseItemSerializer, VendorSerializer, ItemSerializer
import dateutil.parser

def purchase_orders_to_json(models):
    data = []
    for model in models:
        temp = (PurchaseOrderSerializer(model).data)
        temp['vendor_name'] = str(Vendor.objects.get(id=temp['vendor']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        data.append(temp)
    return data

def purchase_items_to_json(items):
    data = []
    for item in items:
        temp = PurchaseItemSerializer(item).data
        temp['item'] = str(Item.objects.get(id=temp['item']))
        data.append(temp)
    return data

# get final on the date foramting 
def str_to_datetime(datetime_str):
    return dateutil.parser.parse(datetime_str)


def vendors_to_json(vendors):
    data = []
    for vendor in vendors:
        temp = VendorSerializer(vendor).data
        data.append(temp)
    return data

def items_to_json(items):
    data = []
    for item in items:
        temp = ItemSerializer(item).data
        data.append(temp)
    return data
