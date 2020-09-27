from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .utils import gift_card_categories_to_json, unique_cards_to_json, gift_cards_to_json, gift_card_to_json, payment_methods_to_json, payment_to_json, gift_card_redeeme_to_json
from .models import GiftCard, GiftCardCategory, UniqueCard, Payment, PaymentMethod, GiftCardRedeem, Settings
from sales.models import Invoice
from user_handler.permission_check import bind, check_permission
from inventory.models import PurchaseOrder
import uuid
from django.conf import settings
from django.utils.timezone import now
from user_handler.models import Customer
from inventory.utils import  str_to_datetime
from user_handler.models import log
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

@require_http_methods(['POST'])
@bind
def add_new_gift_cards(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
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
                log('payment/gift_card', 'create', gift_card.id, str(gift_card), {}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

                
@require_http_methods(['POST'])
@bind
def get_multiple_gift_cards(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
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
                    x = GiftCard.objects.filter(is_active = True).order_by('-id')
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards']  = gift_cards_to_json(x)
                    return JsonResponse(response_json)
                if data_json['filter'] == 'name':
                    x = GiftCard.objects.filter(is_active = True, name__icontains=str(data_json['name']).lower()).order_by('-id')
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards'] = gift_cards_to_json(x)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'code':
                    x = GiftCard.objects.filter(is_active = True, code__icontains=str(data_json['code']).lower()).order_by('-id')
                    response_json['count'] = len(x)
                    x = x[start:end]
                    response_json['gift_cards'] = gift_cards_to_json(x)
                    response_json['status'] = True
                if data_json['filter'] == "multiple":
                    gift_cards = GiftCard.objects.filter(is_active= True).order_by('-id')
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            uuids = data_json['gift_cards_uuid']
            for uuid in uuids:
                gift_card = GiftCard.objects.get(uuid=uuid)
                x = gift_card.id
                gift_card.delete()
                log('payment/gift_card', 'delete', x, str(x), {}, user)
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
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
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                log('payment/gift_card', 'update', gift_card.id, str(gift_card), {}, user)

            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_unique_cards(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            uuids = data_json['uuids']
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            for uuid in uuids:
                card = UniqueCard.objects.get(uuid = uuid)
                if card.is_used:
                    raise Exception("You cannot delete gift card that's already been used.")
                else:
                    log('payment/gift_card', 'delete', card.id, str(card), {}, user)
                    card.delete()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@require_http_methods(['POST'])
@bind
def validate_gift_card(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
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

@require_http_methods(['POST'])
@bind
def get_payment_methods(self, request):
    response_json = {'status':'', 'payment_methods':''}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            category = []
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    category = GiftCardCategory.objects.filter(is_active=True).order_by('-id')
                if data_json['filter'] == "multiple":
                    category = GiftCardCategory.objects.filter().order_by('-id')
                    if data_json['filters']['name']:
                        category = category.filter(name__icontains = data_json['filters']['name'])
                    if data_json['filters']['status']:
                        category = category.filter(is_active = data_json['filters']['status']['is_active'])
                response_json['count'] = len(category)
                category = category[data_json['start']:data_json['end']]
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            payment_models = []
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']           
            temp = False
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
                    payment_models.append(temp)
                    if payment['invoice']:
                        temp.invoice.save()
                    elif payment['purchase_order']:
                        temp.purchase_order.save()
                    log('payment/payment', 'create', temp.id, str(temp), {}, user)
                response_json['status'] = True
                response_json['payments'] = payment_to_json(payment_models)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            if temp:
                temp.delete()
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def credit_payment(self, request):
    response_json = {'status':False}
    payment = False
    new_credit = False
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            new_credit = False
            if data_json['action'] == "credit_payment":
                credit = Payment.objects.get(id= data_json['credit_id'])
                print(credit.amount,  data_json['amount'])
                if credit.amount != data_json['amount']:
                    amount = credit.amount - data_json['amount']
                    if amount < 0:
                        raise Exception("Payment must be less than or equal to the credit amount.")
                    new_credit = Payment.objects.create(
                        invoice = credit.invoice,
                        purchase_order = credit.purchase_order,
                        amount = amount,
                        method = credit.method,
                        transaction_from = credit.transaction_from,
                        transaction_id = credit.transaction_id,
                        bank_name = credit.bank_name,
                        remarks = credit.remarks,
                        is_paid_credit = False
                    )
                payment = Payment.objects.create(
                    invoice = credit.invoice,
                    purchase_order = credit.purchase_order,
                    amount = data_json['amount'],
                    method = PaymentMethod.objects.get(id=data_json['method']),
                    transaction_from = data_json['transaction_from'],
                    transaction_id = data_json['transaction_id'],
                    bank_name = data_json['bank_name'],
                    remarks = data_json['remarks'],
                    is_paid_credit = False
                )
                if "accounting" in settings.INSTALLED_APPS:
                    from accounting.models import Account, LedgerEntry, AccountingSettings
                    account = Account.objects.get(id = data_json['credited_account'])
                    bid = str( uuid.uuid4())
                    if credit.invoice:
                        entry = LedgerEntry.objects.create(
                            payment = payment,
                            account = account,
                            remarks = "automated entry for credit payment",
                            date = now(),
                            is_add = False,
                            bundle_id = bid,
                        )
                        account = Account.objects.get(id = data_json['choosen_account'])
                        entry = LedgerEntry.objects.create(
                            payment = payment,
                            account = account,
                            remarks = "automated entry for credit payment",
                            date = now(),
                            is_add = True,
                            bundle_id = bid
                        )
                    elif credit.purchase_order:
                        entry = LedgerEntry.objects.create(
                            payment = payment,
                            account = account,
                            remarks = "automated entry for credit payment",
                            date = now(),
                            is_add = True,
                            bundle_id = bid
                        )
                        account = Account.objects.get(id = data_json['choosen_account'])
                        entry = LedgerEntry.objects.create(
                            payment = payment,
                            account = account,
                            remarks = "automated entry for credit payment",
                            date = now(),
                            is_add = False,
                            bundle_id = bid
                        )
                response_json['status'] = True
                credit.is_paid_credit = True
                credit.save()
                if credit.invoice:
                    credit.invoice.save()
                elif credit.purchase_order:
                    credit.purchase_order.save()
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                log('payment/credit_payment', 'create', payment.id, str(payment), {}, user)   
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            if payment:
                payment.delete()
            if new_credit:
                new_credit.delete()
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_payment(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
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
                    log('payment/payment', 'soft-delete', payment.id, str(payment), {}, user)
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            if data_json['action'] == "update":
                payment = Payment.objects.get(id=data_json['payment_id'])
                old_payment = payment
                # payment.amount=data_json['amount'],
                payment.transaction_from = data_json['transaction_from']
                payment.transaction_id = data_json['transaction_id']
                payment.bank_name = data_json['bank_name']
                payment.remarks = data_json['remarks']
                payment.save()
                log('payment/payment', 'update', payment.id, str(payment), {'old_data': payment_to_json([old_payment])}, user)
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "invoice":
                    payments = Payment.objects.filter(is_active=True, invoice=Invoice.objects.get(id=data_json['invoice']))
                    response_json['payments'] = payment_to_json(payments)
                    response_json['status'] = True
                if data_json['filter'] == "purchase_order":
                    payments = Payment.objects.filter(is_active=True, purchase_order=PurchaseOrder.objects.get( id=data_json['purchase_order']))
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
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            redeeme = None
            payment = None
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "redeem":
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
                try:
                    default_method = Settings.objects.filter()[0].default_gitf_card_payment_method
                except:
                    raise Exception("Default payment method for gift card is not defined. Please setup the payment settings properly.")
                if unique:
                    value = unique.gift_card.rate
                    if unique.gift_card.discount_type == "percentage":
                        if not invoice:
                            raise Exception("Cannot redeeme gift card with discount in percentage without a invoice.")
                        value = invoice.bill_amount*value/100
                    if unique.is_used:
                        raise Exception("This gift card is already redeemed.")
                    if not unique.is_active:
                        raise Exception("This gift card is not yet been activated. Please content the vendor of the gift card or the support.")
                    if invoice:
                        payment = Payment.objects.create(
                            invoice = invoice,
                            amount = value,
                            method = default_method,
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
                    unique.is_used = True
                    unique.save()
                    if payment:
                        payment.transaction_id = redeeme.id
                        payment.save()
                else:
                    card = GiftCard.objects.get(code = code)
                    value = card.rate
                    if card.discount_type == "percentage":
                        if not invoice:
                            raise Exception("Cannot redeeme gift card with discount in percentage without a invoice.")
                        value = invoice.bill_amount*value/100
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
                            method = default_method,
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
                    card.count_used = card.count_used + 1
                    card.save()
                if payment:
                    if data_json['account']:
                        from simple_im.settings import INSTALLED_APPS
                        if 'accounting' in INSTALLED_APPS:
                            from accounting.models import Account, payemnt_entry_to_system
                            account = Account.objects.get(id = data_json['account'])
                            payemnt_entry_to_system(account, payment)
                        else:
                            raise Exception('You need to install and setup the accounting module to use the accounting features.')
                    response_json['payment'] = payment_to_json([payment])
                if invoice:
                    invoice.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            if payment:
                payment.delete()
            if redeeme:
                redeeme.delete()
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def redeeme_history(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            history = []
            if data_json['action'] == "get":
                history = GiftCardRedeem.objects.filter()
                if data_json['filter'] == "multiple":
                    if data_json['filters']['gift_card']:
                        history = history.filter(card__id =  data_json['filters']['gift_card'])
                    if data_json['filters']['unique_card']:
                        history = history.filter(unique_card__id = data_json['filters']['unique_card'])
                    if data_json['filters']['value']:
                        if data_json['filters']['value']['from']:
                            history = history.filter(value__gte = data_json['filters']['value']['from'])
                        if data_json['filters']['value']['upto']:
                            history = history.filter(value__lte = data_json['filters']['value']['upto'])
                    if data_json['filters']['invoice']:
                        history = history.filter(invoice__id = data_json['filters']['invoice'])
                    if data_json['filters']['customer']:
                        history = history.filter(customer__id = data_json['filters']['customer'])
                    if data_json['filters']['date']:
                        if data_json['filters']['date']['from']:
                            history = history.filter(date__gte = str_to_datetime(data_json['filters']['date']['from']))
                        if data_json['filters']['date']['upto']:
                            history = history.filter(date__lte = str_to_datetime(data_json['filters']['date']['upto']))
                response_json['count'] = len(history)
                history = history[data_json['start']:data_json['end']]
                response_json['redeeme_history'] = gift_card_redeeme_to_json(history)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def add_new_gift_card_category(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            if data_json['action'] == "add":
                category = GiftCardCategory.objects.create(
                    name = data_json['name']
                )
                data_json['category'] = gift_card_categories_to_json([category])
                response_json['status'] = True
                log('payment/gift_card_category', 'create', category.id, str(category), {}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_gift_card_category(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            if data_json['action'] == "update":
                category = GiftCardCategory.objects.get(id = data_json['gift_card_category'])
                if data_json['name']:
                    category.name = data_json['name']
                if data_json['is_active']:
                    category.is_active = data_json['is_active']
                category.save()
                data_json['category'] = gift_card_categories_to_json([category])
                response_json['status'] = True
                log('payment/gift_card_category', 'update', category.id, str(category), {}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
       

@require_http_methods(['POST'])
@bind
def delete_gift_card_category(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            if data_json['action'] == "delete":
                for category in data_json['gift_card_categories']:
                    x = GiftCardCategory.objects.get(id = category)
                    y = x.id
                    x.delete()
                    log('payment/gift_card_category', 'delete', y, str(y), {}, user)

                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
       

@require_http_methods(['POST'])
@bind
def get_gift_card_category(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                category = GiftCardCategory.objects.get(id = data_json['gift_card_category'])
                response_json['category'] = gift_card_categories_to_json([category])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['GET'])
@bind
def get_payment_settings(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            setting = Settings.objects.filter(is_active = True)[0]
            response_json['settings'] = {
                'default_gitf_card_payment_method' : setting.default_gitf_card_payment_method.id,
                'default_payment_method_qk_sales' : setting.default_payment_method_qk_sales.id
            }
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def update_payment_settings(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            setting = Settings.objects.filter(is_active = True)[0]
            old = setting
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                if data_json['default_gitf_card_payment_method']:
                    setting.default_gitf_card_payment_method = PaymentMethod.objects.get(id = data_json['default_gitf_card_payment_method'])
                if data_json['default_payment_method_qk_sales']:
                    setting.default_payment_method_qk_sales = PaymentMethod.objects.get(id = data_json['default_payment_method_qk_sales'])
                setting.save()
                response_json['settings'] = {
                    'default_gitf_card_payment_method' : setting.default_gitf_card_payment_method.id,
                    'default_payment_method_qk_sales' : setting.default_payment_method_qk_sales.id
                }
                c = {
                    'default_gitf_card_payment_method' : old.default_gitf_card_payment_method.id,
                    'default_payment_method_qk_sales' : old.default_payment_method_qk_sales.id
                }
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                log('payment/settings', 'update', old.id, str(old),  c , user)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
