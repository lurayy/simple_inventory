''' Searializers module for models of api '''
from rest_framework import serializers
from .models import GiftCard, GiftCardCategory, UniqueCard, Payment, PaymentMethod

class GiftCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftCard
        fields= '__all__'


class UniqueCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UniqueCard
        fields= '__all__'


class GiftCardCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftCardCategory
        fields= '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields= '__all__'
