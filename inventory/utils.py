from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, ItemCatagory, PurchaseOrderStatus
from django.forms.models import model_to_dict 
from user_handler.models import Vendor, CustomUserBase
from .serializers import PurchaseOrderSerializer, PurchaseItemSerializer, VendorSerializer, ItemSerializer, PlaceSerializer,ItemCatagorySerializer
import dateutil.parser

def purchase_orders_to_json(models):
    data = []
    for model in models:
        temp = (PurchaseOrderSerializer(model).data)
        temp['vendor_name'] = str(Vendor.objects.get(id=temp['vendor']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        temp['status_name'] = str(PurchaseOrderStatus.objects.get(id=temp['status']))
        temp['items'] = ''
        for item in model.items.filter(is_active=True):
            temp['items'] = f'{item.item}, {temp["items"]}'
        data.append(temp)
    return data

def purchase_items_to_json(items):
    data = []
    for item in items:
        temp = PurchaseItemSerializer(item).data
        temp['item_name'] = str(Item.objects.get(id=temp['item']))
        data.append(temp)
    return data

# get final on the date foramting 
def str_to_datetime(datetime_str):
    return dateutil.parser.parse(datetime_str)


def vendors_to_json(vendors):
    data = []
    for vendor in vendors:
        temp = VendorSerializer(vendor).data
        temp['name'] = str(temp['first_name']) + " " + str(temp['middle_name'] )+ str(temp['last_name'])
        data.append(temp)
    return data

def items_to_json(items):
    data = []
    for item in items:
        temp = ItemSerializer(item).data
        temp['catagory_str'] = str(ItemCatagory.objects.get(id=temp['catagory']))
        data.append(temp)
    return data

def item_catagories_to_json(catagories):
    data = []
    for catagory in catagories:
        temp = ItemCatagorySerializer(catagory).data
        data.append(temp)
    return data

def places_to_json(places):
    data = []
    for place in places:
        temp = PlaceSerializer(place).data
        data.append(temp)
    return data

