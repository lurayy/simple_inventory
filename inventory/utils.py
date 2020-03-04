from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
from django.forms.models import model_to_dict 
from user_handler.models import Vendor, CustomUserBase
from .serializers import PurchaseOrderSerializer, PurchaseItemSerializer

def get_data_from_purchase_orders(models):
    data = []
    for model in models:
        temp = (PurchaseOrderSerializer(model).data)
        temp['vendor'] = str(Vendor.objects.get(id=temp['vendor']))
        temp['added_by'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        data.append(temp)
    return data

def get_data_from_purchase_items(items):
    data = []
    for item in items:
        temp = PurchaseItemSerializer(item).data
        temp['item'] = str(Item.objects.get(id=temp['item']))
        data.append(temp)
    return data