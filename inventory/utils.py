from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, ItemCategory, PurchaseOrderStatus, ItemImage
from django.forms.models import model_to_dict 
from user_handler.models import Vendor, CustomUserBase, Setting
from .serializers import PurchaseOrderSerializer, PurchaseItemSerializer, VendorSerializer, ItemSerializer, PlaceSerializer,ItemCategorySerializer, PlacementSerializer, ItemImageSerializer
import dateutil.parser
from user_handler.models import ActivityLog, Country
from user_handler.serializers import CountrySerializer

def purchase_orders_to_json(models):
    data = []
    for model in models:
        temp = (PurchaseOrderSerializer(model).data)
        temp['vendor_name'] = str(Vendor.objects.get(id=temp['vendor']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        temp['status_name'] = str(PurchaseOrderStatus.objects.get(id=temp['status']))
        x = ActivityLog.objects.filter(object_id = model.id, model = 'inventory/purchase_order')
        temp['count_revision'] =  len(x)
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
        temp['country_detail'] = CountrySerializer(vendor.country).data
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
        temp['category_str'] = str(item.category)
        temp['images'] = []
        if temp['weight']:
            unit = Setting.objects.filter(is_active=True)[0].default_weight_unit
            temp['weight_unit'] = unit
            temp['weight'] = weight_conversion(temp['weight'], unit)
        for image in ItemImage.objects.filter(item = item):
            temp['images'].append(ItemImageSerializer(image).data)
        data.append(temp)
    return data


def items_to_json_with_selection(items,fields):
    data = []
    for item in items:
        final = []
        temp = ItemSerializer(item).data
        temp['category'] = str(ItemCategory.objects.get(id=temp['category']))
        for field in fields:
            final.append(temp[field])
        data.append(final)
    return data

def item_catagories_to_json(catagories, include_items = True):
    data = []
    for category in catagories:
        temp = ItemCategorySerializer(category).data
        temp['parent_str'] = str(category.parent)
        temp['count_item'] = len(Item.objects.filter(category = category))
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


def weight_conversion(mass, to):
    if to == "kg":
        return (mass/1000)
    if to == "lb":
        return (mass/454)
    if to == "g":
        return mass
    raise Exception("Default mass unit is invalid. Accepted Units. Accepted weight units g [gram], kg[kilogram] and lb[pound]")