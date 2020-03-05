''' Searializers module for models of api '''
from rest_framework import serializers
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
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
