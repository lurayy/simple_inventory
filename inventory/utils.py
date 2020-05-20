from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, ItemCatagory, PurchaseOrderStatus
from django.forms.models import model_to_dict 
from user_handler.models import Vendor, CustomUserBase
from .serializers import PurchaseOrderSerializer, PurchaseItemSerializer, VendorSerializer, ItemSerializer, PlaceSerializer,ItemCatagorySerializer, PlacementSerializer
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
        temp['sales_price'] = item.item.sales_price
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
        if (temp['middle_name']):
            pass
        else:
            temp['middle_name'] = ""
        data.append(temp)
    return data

def items_to_json(items):
    data = []
    for item in items:
        temp = ItemSerializer(item).data
        temp['catagory_str'] = str(ItemCatagory.objects.get(id=temp['catagory']))
        # temp['product_image'] = item.product_image.url()
        # print(item.product_thumbnail_image.url())
        # print(item.product_image.__url)
        data.append(temp)
    return data


def items_to_json_with_selection(items,fields):
    data = []
    for item in items:
        final = []
        temp = ItemSerializer(item).data
        temp['catagory'] = str(ItemCatagory.objects.get(id=temp['catagory']))
        for field in fields:
            final.append(temp[field])
        data.append(final)
    return data

def item_catagories_to_json(catagories, include_items = True):
    data = []
    for catagory in catagories:
        temp = ItemCatagorySerializer(catagory).data
        if include_items:
            pass
        data.append(temp)
    return data

def places_to_json(places):
    data = []
    for place in places:
        temp = PlaceSerializer(place).data
        data.append(temp)
    return data

def placements_to_json(placements):
    data=[]
    for placement in placements:
        if( placement.stock != 0):
            temp = PlacementSerializer(placement).data
            temp['purchase_order_uuid'] = str(placement.purchase_item.purchase_order.uuid) 
            temp['purchase_order_id'] = str(placement.purchase_item.purchase_order.id)
            temp['item_name'] = str(placement.item.name)
            temp['sales_price'] = placement.item.sales_price
            temp['placed_on_str'] = str(placement.placed_on.name)
            temp['qr_code_image'] = str(placement.purchase_item.qr_code_image.url)
            data.append(temp)
    return data