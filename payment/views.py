from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .utils import gift_card_categories_to_json, unique_cards_to_json, gift_cards_to_json, gift_card_to_json, payment_methods_to_json
from .models import GiftCard, GiftCardCategory, UniqueCard, Payment, PaymentMethod
from sales.models import Invoice

@login_required
@require_http_methods(['POST'])
def gift_cards(request):
    if request.method == "POST":
        response_json = {'status':False, 'gift_cards':[]}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    start = int(data_json["start"])
                    end = int(data_json["end"])
                    response_json['status'] = True
                    response_json['gift_cards']  = gift_cards_to_json(GiftCard.objects.filter()[start:end])
                    return JsonResponse(response_json)
                if data_json['filter'] == 'name':
                    response_json['gift_cards'] = gift_cards_to_json(GiftCard.objects.filter(name__icontains=str(data_json['name']).lower())[start:end])
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'code':
                    response_json['gift_cards'] = gift_cards_to_json(GiftCard.objects.filter(code__icontains=str(data_json['name']).lower())[start:end])
                    response_json['status'] = True
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def gift_card(request):
    response_json = {}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if data_json['action'] == "get":
                if data_json['filter'] == "uuid":
                    response_json['status'] = True
                    response_json['gift_cards']  = gift_card_to_json(GiftCard.objects.get(uuid=data_json['uuid']))
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def delete_gift_cards(request):
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuids = data_json['gift_cards_uuid']
            for uuid in uuids:
                gift_cards = GiftCard.objects.get(uuid=uuid)
                gift_card.is_active = False
                gift_card.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
@require_http_methods(['POST'])
def delete_unique_cards(request):
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuids = data_json['unique_card_id']
            for uuid in uuids:
                card = UniqueCard.objects.get(uuid=uuid)
                if card.is_used:
                    raise Exception("You cannot delete gift card that's already been used.")
                else:
                    card.delete()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def validate_gift_card(request):
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            code = data_json['code']
            try:
                card = UniqueCard.objects.get(code=code)
                if card.is_used:
                    response_json['status'] = False
                    response_json['msg'] = "Card is already used."
                else:
                    response_json['status'] = True
                    response_json['msg'] = "Valid"
                    response_json['card_detail'] = {
                        'discountType':card.gift_card.discount_type,
                        'rate':card.gift_card.rate,
                        'name':card.gift_card.name,
                        'category':card.gift_card.category
                    }
            except:
                response_json['status'] = False
                response_json['msg'] = "Card Doesnot Exsist."
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

# {
#     invoice_id:,
#     payment_method:
#     amount
#     bank_name 
#     transaction_id
# }

@login_required
@require_http_methods(['POST'])
def payment_methods(request):
    response_json = {'status':'', 'payment_methods':''}
    try:  
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        if data_json['action'] == 'get':
            pay_methods = PaymentMethod.objects.filter(is_active=True)
            response_json['payment_methods'] = payment_methods_to_json(pay_methods)
            response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def apply_payment(request):
    response_json = {'status':''}
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        payment_method = PaymentMethod.objects.get(id=data_json['payment_method'])
        if (payment_method.is_gift_card):
            pass
        else:
            payment = Payment.objects.create(
                invoice = Invoice.objects.get(id=data_json['invoice_id']),
                payment_method = PaymentMethod.objects.get(id=data_json['payment_method']),
                amount = data_json['amount'],
                transaction_from = data_json['transaction_from'],
                transaction_id = data_json['transaction_id']
            )
            payment.save()
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
