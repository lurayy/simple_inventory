from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .utils import gift_card_categories_to_json, unique_cards_to_json, gift_cards_to_json, gift_card_to_json
from .models import GiftCard, GiftCardCategory, UniqueCard

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
            except:
                response_json['status'] = False
                response_json['msg'] = "Card Doesnot Exsist."
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

