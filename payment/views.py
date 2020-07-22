from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .utils import gift_card_categories_to_json, unique_cards_to_json, gift_cards_to_json, gift_card_to_json, payment_methods_to_json, payment_to_json
from .models import GiftCard, GiftCardCategory, UniqueCard, Payment, PaymentMethod, GiftCardRedeem, Settings
from sales.models import Invoice
from user_handler.permission_check import bind, check_permission
from inventory.models import PurchaseOrder
import uuid
from django.conf import settings
from django.utils.timezone import now
from user_handler.models import Customer

@require_http_methods(['POST'])
@bind
def add_new_gift_cards(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] =="add":
                gift_card = GiftCard.objects.create(
                    name = data_json['name'],
                    code = data_json['code'],
                    discount_type = data_json['discount_type'],
                    rate = data_json['rate'],
                    is_limited = data_json['is_limited'],
                    has_unique_codes = data_json['has_unique_codes'],
                    count_limit = data_json['count_limit']
                )
                if data_json['category']:
                    gift_card.category = GiftCardCategory.objects.get(id=data_json['category'])
                gift_card.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

                
@require_http_methods(['POST'])
@bind
def get_multiple_gift_cards(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False, 'gift_cards':[]}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            start = int(data_json["start"])
            end = int(data_json["end"])
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    response_json['status'] = True
                    x = GiftCard.objects.filter(is_active = True)
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards']  = gift_cards_to_json(x)
                    return JsonResponse(response_json)
                if data_json['filter'] == 'name':
                    x = GiftCard.objects.filter(is_active = True, name__icontains=str(data_json['name']).lower())
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards'] = gift_cards_to_json(x)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'code':
                    x = GiftCard.objects.filter(is_active = True, code__icontains=str(data_json['name']).lower())
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards'] = gift_cards_to_json(x)
                    response_json['status'] = True
                if data_json['filter'] == "multiple":
                    gift_cards = GiftCard.objects.filter(is_active= True)
                    if data_json['filters']['name']:
                        gift_cards = gift_cards.filter(name__icontains = data_json['filters']['name'])
                    if data_json['filters']['category']:
                        gift_cards = gift_cards.filter(category__id = data_json['filters']['category'])
                    if data_json['filters']['code']:
                        gift_cards = gift_cards.filter(code__icontains = data_json['filters']['code'])
                    if data_json['filters']['discount_type']:
                        gift_cards = gift_cards.filter(discount_type = data_json['filters']['discount_type'])
                    if data_json['filters']['apply_limited']:
                        gift_cards = gift_cards.filter(is_limited = data_json['filters']['is_limited'])
                    if data_json['filters']['apply_has_unique_codes']:
                        gift_cards = gift_cards.filter(has_unique_codes = data_json['filters']['has_unique_codes'])
                    if data_json['filters']['rate']:
                        if data_json['filters']['rate_from']:
                            gift_cards = gift_cards.filter(rate__gte = data_json['filters']['rate_from'])
                        if data_json['filters']['rate_upto']:
                            gift_cards = gift_cards.filter(rate__lte = data_json['filters']['rate_upto'])
                    if data_json['filters']['count_used']:
                        if data_json['filters']['count_used_from']:
                            gift_cards = gift_cards.filter(count_used__gte = data_json['filters']['count_used_from'])
                        if data_json['filters']['count_used_upto']:
                            gift_cards = gift_cards.filter(count_used__lte = data_json['filters']['count_used_upto'])
                    response_json['count'] = len(gift_cards)
                    gift_cards = gift_cards[data_json['start']: data_json['end']]
                    response_json['gift_cards']  = gift_cards_to_json(gift_cards)
                    response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_gift_card_details(self, request):
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
def delete_gift_cards(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuids = data_json['gift_cards_uuid']
            for uuid in uuids:
                gift_card = GiftCard.objects.get(uuid=uuid)
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
def update_gift_card(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                gift_card = GiftCard.objects.get(uuid= data_json['gift_card_uuid'])
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
def delete_unique_cards(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuids = data_json['uuids']
            for uuid in uuids:
                card = UniqueCard.objects.get(uuid = uuid)
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
def validate_gift_card(self, request):
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
def get_payment_methods(self, request):
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
def apply_payment(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            payment_method = PaymentMethod.objects.get(id=data_json['payment_method'], is_active=True)
            if (payment_method.header == "pre-paid"):
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
                    transaction_from = data_json['transaction_from'],
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


@require_http_methods(['POST'])
@bind
def get_gift_card_categories(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    category = GiftCardCategory.objects.filter(is_active=True)
                    response_json['gift_card_categories'] = gift_card_categories_to_json(category)
                    response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def create_payment(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            payment_models = []
            if data_json['action'] == "add":
                for payment in data_json['payments']:
                    if payment['invoice']:
                        temp = Payment.objects.create(
                            invoice = Invoice.objects.get(id=payment['invoice']),
                            amount=payment['amount'],
                            method= PaymentMethod.objects.get(id=payment['method']),
                            transaction_from = payment['transaction_from'],
                            transaction_id = payment['transaction_id'],
                            bank_name = payment['bank_name'],
                            remarks = payment['remarks'],
                        )
                        temp.save()                            
                    elif payment['purchase_order']:
                        temp = Payment.objects.create(
                            purchase_order = PurchaseOrder.objects.get(id=payment['purchase_order']),
                            amount= payment['amount'],
                            method= PaymentMethod.objects.get(id=payment['method']),
                            transaction_from = payment['transaction_from'],
                            transaction_id = payment['transaction_id'],
                            bank_name = payment['bank_name'],
                            remarks = payment['remarks']
                        )
                        temp.save()
                    else:
                        temp = Payment.objects.create(
                            amount=payment['amount'],
                            method= PaymentMethod.objects.get(id=payment['method']),
                            transaction_from = payment['transaction_from'],
                            transaction_id = payment['transaction_id'],
                            bank_name = payment['bank_name'],
                            remarks = payment['remarks']
                        )
                        temp.save()
                    if payment['invoice'] or payment['purchase_order']:
                        if "accounting" in settings.INSTALLED_APPS:
                            from accounting.models import Account, payemnt_entry_to_system
                            account = Account.objects.get(id = payment['account'])
                            payemnt_entry_to_system(account, temp)
                    try:
                        if payment['credit_payment_for']:
                            credit = Payment.objects.get(id = payment['credit_payment_for'])
                            temp.remarks = payment['remarks'] + " / credit payemnt for  "+ str(credit.id)
                            temp.save()
                            if "accounting" in settings.INSTALLED_APPS:
                                from accounting.models import handle_credit_for
                                handle_credit_for(credit, temp)
                    except:
                        pass
                    payment_models.append(temp)  

                response_json['status'] = True
                response_json['payments'] = payment_to_json(payment_models)
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_payment(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "delete":
                for pay_id in data_json['payments_ids']:
                    payment = Payment.objects.get(id=pay_id)
                    old = payment
                    payment.is_active = False
                    payment.save()
                    if old.is_active == True and payment.is_active == False: 
                        if "accounting" in settings.INSTALLED_APPS:
                            from accounting.models import handle_payment_deletetion
                            handle_payment_deletetion(payment)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_payment(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                payment = Payment.objects.get(id=data_json['payment_id'])
                # payment.amount=data_json['amount'],
                payment.transaction_from = data_json['transaction_from']
                payment.transaction_id = data_json['transaction_id']
                payment.bank_name = data_json['bank_name']
                payment.remarks = data_json['remarks']
                payment.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_payments(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "invoice":
                    payments = Payment.objects.filter(is_active=True, invoice=Invoice.objects.get(is_active=True, id=data_json['invoice']))
                    response_json['payments'] = payment_to_json(payments)
                    response_json['status'] = True
                if data_json['filter'] == "purchase_order":
                    payments = Payment.objects.filter(is_active=True, purchase_order=PurchaseOrder.objects.get(is_active=True, id=data_json['purchase_order']))
                    response_json['payments'] = payment_to_json(payments)
                    response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
   



# default payment method for gift cards 

@require_http_methods(['POST'])
@bind
def redeeme_gift_card(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "redeeme":
                code = data_json['code']
                if data_json['invoice']:
                    invoice = Invoice.objects.get(id = data_json['invoice'])
                else:
                    invoice = None
                unique = False
                try: 
                    unique = UniqueCard.objects.get(code = code)
                except:
                    unique = False
                value = unique.gift_card.rate
                if unique.gift_card.discount_type == "percentage":
                    if not invoice:
                        raise Exception("Cannot redeeme gift card with discount in percentage without a invoice.")
                    value = invoice.bill_amount*value/100
                if unique:
                    if unique.is_used:
                        raise Exception("This gift card is already redeemed.")
                    if not unique.is_active:
                        raise Exception("This gift card is not yet been activated. Please content the vendor of the gift card or the support.")
                    if invoice:
                        payment = Payment.objects.create(
                            invoice = invoice,
                            amount = value,
                            method = Settings.objects.all()[0].default_gitf_card_payment_method,
                            transaction_from = "Gift card "+str(unique.code)
                        )
                    else:
                        payment = None
                    redeeme = GiftCardRedeem.objects.create(
                        card = unique.gift_card,
                        unique_card = unique,
                        invoice = invoice,
                        value = value,
                        payment = payment,
                        customer = Customer.objects.get(id=data_json['customer'])
                    )
                    if payment:
                        payment.transaction_id = redeeme.id
                        payment.save()
                else:
                    card = GiftCard.objects.get(code = code)
                    if card.has_unique_codes:
                        raise Exception("This gift is not to be used a coupon. [has unique codes]")
                    if card.is_used_out:
                        raise Exception("This limited coupon has already reached it's limits.")
                    if not card.is_active:
                        raise Exception("This gift card is not active so cannot be redeemed.")
                    if invoice:
                        payment = Payment.objects.create(
                            invoice = invoice,
                            amount = value,
                            method = Settings.objects.filter(is_active=True)[0].default_gitf_card_payment_method,
                            transaction_from = "Gift card "+str(unique.code)
                        )
                    else:
                        payment = None
                    redeeme = GiftCardRedeem.objects.create(
                        card = card,
                        unique_card = unique,
                        invoice = invoice,
                        value = value,
                        payment = payment,
                        customer = Customer.objects.get(id=data_json['id'])
                    )
                    if payment:
                        payment.transaction_id = redeeme.id
                        payment.save()
                if payment:
                    # account = 
                    # payemnt_entry_to_system(value, payment)
                    response_json['payment'] = payment_to_json([payment])
                if invoice:
                    invoice.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



# @require_http_methods(['POST'])
# @bind
# def redeeme_history(self, request):
#     response_json = {'status':False}
#     if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
#         try:
#             json_str = request.body.decode(encoding='UTF-8')
#             data_json = json.loads(json_str)
#             if data_json['action'] == "get":
#                 history = GiftCardRedeem.objects.all()


