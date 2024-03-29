''' Searializers module for models of api '''
from rest_framework import serializers
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, PurchaseOrderStatus,  ItemCategory, ItemImage
from user_handler.models import Vendor

class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields= '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseItem
        fields= '__all__'

class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields= '__all__'

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields= '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemCategory
        fields= '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Place
        fields= '__all__'


class StatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrderStatus
        fields= '__all__'




class PlacementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Placement
        fields= '__all__'

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        exclude = ('item',)