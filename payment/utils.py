from . models import UniqueCard, GiftCardCategory, GiftCard
from .serializers import UniqueCardSerializer, GiftCardCategorySerializer, GiftCardSerializer, PaymentMethodSerializer, PaymentSerializer

from accounting.models import FreeEntryLedger, LedgerEntry

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
        free_entry = FreeEntryLedger.objects.filter(entry_for__payment__id=method.id)
        if len(free_entry):
            temp['amount_correction_on_ledger'] = free_entry[0].amount
        data.append(temp)
    return data