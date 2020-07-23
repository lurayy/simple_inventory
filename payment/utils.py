from . models import UniqueCard, GiftCardCategory, GiftCard, GiftCardRedeem
from .serializers import UniqueCardSerializer, GiftCardCategorySerializer, GiftCardSerializer, PaymentMethodSerializer, PaymentSerializer, GiftCardRedeemSerializer
from sales.serializers import InvoiceSerializer
from django.conf import settings
from django.utils.timezone import now

def gift_cards_to_json(cards):
    data = []
    for card in cards:
        temp = GiftCardSerializer(card).data
        temp['category_str'] = str(card.category)
        data.append(temp)
    return data

def unique_cards_to_json(cards):
    data = []
    for card in cards:
        temp = UniqueCardSerializer(card).data
        data.append(temp)
    return data

def gift_card_categories_to_json(cards):
    data = []
    for card in cards:
        temp = GiftCardCategorySerializer(card).data
        data.append(temp)
    return data

def gift_card_to_json(card):
    data = gift_cards_to_json([card])
    temp = []
    for unique_card in card.unique_codes.all():
        temp.append(UniqueCardSerializer(unique_card).data)
    data[0]['unique_cards'] = temp
    return data



def payment_methods_to_json(methods):
    data = []
    for method in methods:
        data.append(PaymentMethodSerializer(method).data)
    return data


def payment_to_json(methods):
    data = []
    for method in methods:
        temp = (PaymentSerializer(method).data)
        temp['payment_method'] = payment_methods_to_json([method.method])
        data.append(temp)
    return data



def gift_card_redeeme_to_json(methods):
    data = []
    for method in methods:
        temp = (GiftCardRedeemSerializer(method).data)
        temp['gift_card'] = GiftCardSerializer(method.card).data
        if method.card:
            temp['unique_card'] = UniqueCardSerializer(method.unique_card).data
        if method.invoice:
            temp['invoice_data'] = InvoiceSerializer(method.invoice).data
        if method.payment:
            temp['payment_data'] = PaymentSerializer(method.payment).data
        data.append(temp)
    return data
