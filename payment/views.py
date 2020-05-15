from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .utils import gift_card_categories_to_json, unique_cards_to_json, gift_cards_to_json, gift_card_to_json, payment_methods_to_json
from .models import GiftCard, GiftCardCategory, UniqueCard, Payment, PaymentMethod
from sales.models import Invoice
from user_handler.permission_check import bind, check_permission


@require_http_methods(['POST'])
@bind
def get_multiple_gift_cards(request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_gift_card_details(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_gift_cards(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def update_gift_card(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuid = data_json['gift_card_uuid']
            gift_card = GiftCard.objects.get(uuid=data_json['uuid'])
            if gift_card.count_used > 1:
                raise Exception("You cannot edit gift card that are already being used.")
            gift_card.name = data_json['name']
            gift_card.category = GiftCardCategory.objects.get(id=data_json['category']) 
            gift_card.discount_type = data_json['discount_type']
            gift_card.rate = data_json['rate']
            gift_card.count_limit = data_json['count_limit']
            gift_card.is_limited = data_json['is_limited']
            gift_card.has_unique_codes = data_json['has_unique_codes']
            gift_card.is_active = data_json['is_active']
            gift_card.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})




@require_http_methods(['POST'])
@bind
def delete_unique_cards(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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


@require_http_methods(['POST'])
@bind
def validate_gift_card(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            code = data_json['code']
            try:
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
                            'category':card.gift_card.category,
                            'isUnique':card.has_unique_codes
                        }
                except:
                    card = GiftCard.objects.get(code=code)
                    if card.is_used_out():
                        response_json['status'] = False
                        response_json['msg'] = "Card is already used."
                    else:
                        response_json['status'] = True
                        response_json['msg'] = "Valid"
                        response_json['card_detail'] = {
                            'discountType':card.discount_type,
                            'rate':card.rate,
                            'name':card.name,
                            'category':card.category,
                            'isUnique':card.has_unique_codes
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


@require_http_methods(['POST'])
@bind
def get_payment_methods(request):
    response_json = {'status':'', 'payment_methods':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def apply_payment(request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            payment_method = PaymentMethod.objects.get(id=data_json['payment_method'], is_active=True)
            if (payment_method.is_gift_card):
                if data_json['isCardUnique']:
                    unique_card = UniqueCard.objects.get(code = data_json['transaction_from'])
                    if unique_card.is_used:
                        raise Exception('The gift card is already used.')
                    card = unique_card.gift_card
                else:
                    card = GiftCard.objects.get(code = data_json['transaction_from'], is_active=True)
                    if card.is_used_out():
                        raise Exception("This gift card is used out.")
                
                invoice = Invoice.objects.get(id=data_json['invoice_id'])
                if card.discount_type == "percent":
                    amount = invoice.bill_amount * card.rate/100
                else:
                    amount = card.gift_card.rate
                payment = Payment.objects.create(
                    invoice = invoice,
                    payment_method = PaymentMethod.objects.get(id=data_json['payment_method']),
                    amount = amount,
                    transaction_from = data_json['transaction_from']
                )
                payment.save()
                if data_json['isCardUnique']:
                    unique_card.is_used = True
                    unique_card.save()
                else:
                    card.count_used = card.count_used + 1
                card.save()
                invoice.save()
            else:
                payment = Payment.objects.create(
                    invoice = Invoice.objects.get(id=data_json['invoice_id']),
                    payment_method = PaymentMethod.objects.get(id=data_json['payment_method']),
                    amount = data_json['amount'],
                    transaction_from = data_json['transaction_from'],
                    transaction_id = data_json['transaction_id'],
                    bank_name = data_json['bank_name']
                )
                payment.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
