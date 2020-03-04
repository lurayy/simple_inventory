''' Searializers module for models of api '''
from rest_framework import serializers
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement

class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields= '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseItem
        fields= '__all__'