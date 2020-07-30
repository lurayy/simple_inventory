''' Searializers module for models of api '''
from rest_framework import serializers
from .models import Invoice, InvoiceItem, InvoiceStatus, SalesSetting
from user_handler.models import Customer, Tax, Discount, CustomerCategory

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


class InvoiceStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InvoiceStatus
        fields= '__all__'


class CustomerCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerCategory
        fields= '__all__'



class SalesSettingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SalesSetting
        exclude = ('id',)