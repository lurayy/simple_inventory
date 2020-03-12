''' Searializers module for models of api '''
from rest_framework import serializers
from .models import Invoice, InvoiceItem
from user_handler.models import Customer, Tax, Discount

class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields= '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields= '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields= '__all__'

class TaxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tax
        fields= '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Discount
        fields= '__all__'
