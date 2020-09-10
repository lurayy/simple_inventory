from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import json
import datetime
from user_handler.models import Vendor, CustomUserBase, Country
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, PurchaseOrderStatus, ItemCatagory, ItemImage
from .utils import purchase_orders_to_json, purchase_items_to_json, str_to_datetime, vendors_to_json, items_to_json, item_catagories_to_json, places_to_json, placements_to_json,items_to_json_with_selection
from .exceptions import  EmptyValueException
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .serializers import StatusSerializer
from django.template.loader import get_template 
import base64
from django.utils import timezone
from django.core.files.base import ContentFile
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from django.template import Context
from io import StringIO
import cgi
from user_handler.permission_check import bind, check_permission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from barcode import generate
import xlwt
from django.utils import timezone

from user_handler.models import log

from django.db.models import Sum

from barcode import Code128
from barcode.writer import ImageWriter

from django.conf import settings
if 'sales' in settings.INSTALLED_APPS:
    from sales.models import SalesSetting 

@require_http_methods(['POST'])
@bind
def get_multiple_purchase_orders(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            start = 0
            end = 25
            if str(data_json['action']).lower() == "get":
                orders = []
                response_json = {'status':'', 'purchase_orders':[]}
                if str(data_json['filter']).lower() == "none":
                    start = int(data_json["start"])
                    end = int(data_json["end"])
                    orders = PurchaseOrder.objects.filter(is_active=True).order_by('-id')
                if str(data_json['filter']).lower() == "added_by":
                    start = int(data_json["start"])
                    end = int(data_json["end"])
                    added_by_obj = CustomUserBase.objects.get(id=int(data_json['added_by']))
                    orders = PurchaseOrder.objects.filter(is_active=True, added_by=added_by_obj).order_by('-id')
                if data_json['filter'] == "third_party_invoice_number":
                    order = PurchaseOrder.objects.filter(is_active=True, third_party_invoice_number = data_json['third_party_invoice_number'])
                if data_json['filter'] == "multiple":
                    start = int(data_json["start"])
                    end = int(data_json["end"])
                    orders = PurchaseOrder.objects.filter(is_active=True)
                    if data_json['filters']['date']:
                        if data_json['filters']['start_date']:
                            start_date = str_to_datetime(str(data_json['filters']['start_date']))
                            orders = orders.filter(invoiced_on__gte = start_date).order_by('-id')
                        if data_json['filters']['end_date']:
                            end_date = str_to_datetime(str(data_json['filters']['end_date']))
                            orders = orders.filter(invoiced_on__lte = end_date).order_by('-id')
                    if data_json['filters']['vendor']:
                        vendor_obj = Vendor.objects.get(id=int(data_json['filters']['vendor_id']))
                        orders = orders.filter(vendor=vendor_obj).order_by('-id')
                    if data_json['filters']['status']:
                        status = PurchaseOrderStatus.objects.get(id=data_json['filters']['status_id'])
                        orders = orders.filter(is_active=True, status=status).order_by('-id')
                
                response_json['count'] = len(orders)
                orders = orders[start:end]
                
                response_json['purchase_orders'] = purchase_orders_to_json(orders)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_purchase_order(self,request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'add':
                try:
                    status = PurchaseOrderStatus.objects.get(id = int(data_json['status']))
                except:
                    status =  PurchaseOrderStatus.objects.filter(is_end=False)[0]
                if (status.is_end):
                    status =  PurchaseOrderStatus.objects.filter(is_end=False)[0]
                valid_data = VerifyJSONWebTokenSerializer().validate({'token':request.headers['Authorization'].split(' ')[1]})
                user = valid_data['user']
                purchase_order = PurchaseOrder.objects.create(
                    discount_type = data_json['discount_type'],
                    discount = data_json['discount'],
                    added_by = user,
                    vendor = Vendor.objects.get(id=int(data_json['vendor'])),
                    invoiced_on = str_to_datetime(data_json['invoiced_on']),
                    completed_on = str_to_datetime(data_json['completed_on']),
                    third_party_invoice_number = data_json['third_party_invoice_number'],
                    status = status,
                    bill_received=data_json['bill_received']
                )
                purchase_order.save()
                response_json['status'] = True
                response_json['purchase_orders'] = purchase_orders_to_json([purchase_order])
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']        
                log('inventory/purchase_order', 'create', purchase_order.id, str(purchase_order), {}, user)

            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_purchase_order_details(self, request):
    ''' To get data about single purchase order
    To get info about a single purchase_order, trigger /apiv1/inventory/porders/<purchase_order_id>/
    To update the data, you can POST on the same link: 
    POST format:
    {
        'action':'update',
        'id':1,
        'invoiced_on': "2019-11-16T08:15:00.000",
        'completed_on: "2019-11-16T08:15:00.000",
        'total_cost': 2500,
        'discount_type': 'fixed',    <- can be fixed or percent
        'discount': 25,
        'added_by':1,                <- added_by id
        'vendor':1,                  <- vendor id 
        'status':'paid',
    }
    '''
    response_json = {'status':False, 'p_order':{}, 'p_items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'get':   
                order = PurchaseOrder.objects.get(id=int(data_json['purchase_order_id']))
                response_json['p_order'] = purchase_orders_to_json([order])
                response_json['p_items'] = purchase_items_to_json(PurchaseItem.objects.filter(purchase_order=order))        
                response_json['status'] = True
            return JsonResponse(response_json)
        except(ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_purchase_order(self, request):
    response_json = {'status':False, 'p_order':{}, 'p_items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order_id']))
                change = {}
                if data_json['discount_type']:
                    change['discount_type'] = purchase_order.discount_type
                    purchase_order.discount_type = data_json['discount_type']
                if data_json['discount']:
                    change['discount'] = purchase_order.discount
                    purchase_order.discount = data_json['discount']
                if data_json['vendor']:
                    change['vendor'] = purchase_order.vendor
                    purchase_order.vendor = Vendor.objects.get(id=int(data_json['vendor']))
                if data_json['invoiced_on']:
                    change['invoiced_on'] = str(purchase_order.invoiced_on)
                    purchase_order.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                if data_json['completed_on']:
                    change['completed_on'] = str(purchase_order.completed_on)
                    purchase_order.completed_on = str_to_datetime(data_json['completed_on'])
                if data_json['status']:
                    change['status'] = purchase_order.status
                    purchase_order.status = PurchaseOrderStatus.objects.get(id=int(data_json['status']))
                if data_json['third_party_invoice_number']:
                    change['third_party_invoice_number'] = purchase_order.third_party_invoice_number
                    purchase_order.third_party_invoice_number = data_json['third_party_invoice_number']
                if data_json['bill_received']:
                    change['bill_received'] = purchase_order.bill_received
                    purchase_order.bill_received = data_json['bill_received']
                purchase_order.save()
                response_json['status'] = True
                response_json['purchase_order'] = purchase_orders_to_json([purchase_order])
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user'] 
                log('inventory/purchase_order', 'update', purchase_order.id, str(purchase_order), change, user)   
                return JsonResponse(response_json)
        except(ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def delete_purchase_orders(self, request):
    '''
    {
        "purchase_orders_id":[
            1,2
        ]
    }
    '''
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
                ids = data_json['purchase_orders_id']
                for id in ids:
                    purchase_order = PurchaseOrder.objects.get(id=int(id))
                    purchase_order.is_active = False
                    purchase_order.status = PurchaseOrderStatus.objects.filter(is_end=False)[0]
                    purchase_order.save()
                    log('inventory/purchase_order', 'delete', purchase_order.id, str(purchase_order), {}, user)   
                    for p_item in PurchaseItem.objects.filter(purchase_order = purchase_order):
                        p_item.is_active = False
                        p_item.status = "incomplete"
                        p_item.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



######################################## Vendor  ########################################


@require_http_methods(['POST'])
@bind
def get_multiple_vendors(self, request):
    '''
    Fucntion to get and add vendors data
    POST Format:
    {
        'action':"get",
        'start':0,
        'end':20
    } 
    add format : 
    {
        "action":"add",
        "first_name": "Raven2",
        "middle_name": "Ulric2 Davenport",
        "last_name": "Solomon2",
        "email": "qadeg@maili2nator.net",
        "website": "https://www.dogotime.org.uk",
        "tax_number": "974",
        "phone1": "+1 (149) 119-4092",
        "phone2": "+1 (381) 765-8778",
        "address": "Qui in at culpa unde"
    }
    '''
    response_json = {'status':False, 'vendors':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    vendors = Vendor.objects.filter(is_active=True).order_by('-id')
                    response_json['count'] = len(vendors)
                    vendors = vendors[int(data_json['start']):int(data_json['end'])]
                    response_json['vendors'] = vendors_to_json(vendors)
                    response_json['status'] = True
                if data_json['filter'] == 'name':
                    vendors = Vendor.objects.filter(is_active=True, first_name__icontains=str(data_json['first_name']).lower())
                    response_json['vendors'] = vendors_to_json(vendors)
                    if response_json['vendors']:
                        response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def add_new_vendor(self, request):
    response_json = {'status':False, 'vendors':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False}
            if data_json['action'] == "add":
                valid_data = VerifyJSONWebTokenSerializer().validate({'token':request.headers['Authorization'].split(' ')[1]})
                user = valid_data['user']
                vendor = Vendor.objects.create(
                    first_name = str(data_json['first_name']),
                    last_name = str(data_json['last_name']),
                    middle_name = str(data_json['middle_name']),
                    email = str(data_json['email']),
                    website = str(data_json['website']),
                    tax_number = str(data_json['tax_number']),
                    phone1 = str(data_json['phone1']),
                    phone2 = str(data_json['phone2']),
                    address = str(data_json['address']),
                    company = data_json['company'],
                    added_by = user,
                )
                vendor.save()
                if data_json['country']:
                    vendor.country = Country.objects.get(id=data_json['country'])
                vendor.save()
                
                log('inventory/vendor', 'create', vendor.id, str(vendor), {}, user)
                response_json['vendors'] = vendors_to_json([vendor])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_vendors(self, request):
    '''
    {
        "vendors_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['vendors_id']
            valid_data = VerifyJSONWebTokenSerializer().validate({'token':request.headers['Authorization'].split(' ')[1]})
            user = valid_data['user']    
            if ids is None:
                raise Exception('Empty Vendor list')
            for id in ids:
                vendor = Vendor.objects.get(id=int(id))
                vendor.is_active = False
                vendor.save()
                log('inventory/vendor', 'soft-delete', vendor.id, str(vendor), {}, user)
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_vendor_details(self, request):
    '''
    
    '''
    response_json = {'status':'', 'vendors':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] =="get":
                vendor = Vendor.objects.get(id=int(data_json['vendor_id']))
                response_json['vendors'] = vendors_to_json([vendor])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def update_vendor(self, request):
    response_json = {'status':False, 'vendors':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            valid_data = VerifyJSONWebTokenSerializer().validate({'token':request.headers['Authorization'].split(' ')[1]})
            user = valid_data['user']
                
            if data_json['action'] == "update":
                vendor = Vendor.objects.get(id = data_json['vendor_id'])
                changes = {}
                if data_json['first_name']:
                    changes['first_name'] = vendor.first_name
                    vendor.first_name = str(data_json['first_name'])
                if data_json['last_name']:
                    changes['last_name'] = vendor.last_name
                    vendor.last_name = str(data_json['last_name'])
                if data_json['middle_name']:
                    changes['first_middle_namename'] = vendor.middle_name
                    vendor.middle_name = str(data_json['middle_name'])
                if data_json['email']:
                    changes['email'] = vendor.email
                    vendor.email = str(data_json['email'])
                if data_json['website']:
                    changes['website'] = vendor.website
                    vendor.website = str(data_json['website'])
                if data_json['tax_number']:
                    changes['tax_number'] = vendor.tax_number
                    vendor.tax_number = str(data_json['tax_number'])
                if data_json['phone1']:
                    changes['phone1'] = vendor.phone1
                    vendor.phone1 = str(data_json['phone1'])
                if data_json['phone2']:
                    changes['phone2'] = vendor.phone2
                    vendor.phone2 = str(data_json['phone2'])
                if data_json['address']:
                    changes['address'] = vendor.address
                    vendor.address = str(data_json['address'])
                if data_json['country']:
                    changes['country'] = str(vendor.country)
                    vendor.country = Country.objects.get(id=data_json['country'])
                if data_json['company']:
                    changes['company'] = vendor.company
                    vendor.tax_number = str(data_json['company'])
                vendor.save()
                log('inventory/vendor', 'update', vendor.id, str(vendor), changes, user)
                response_json['vendors'] = vendors_to_json([vendor])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



######################################## Items ########################################


@require_http_methods(['POST'])
@bind
def get_multiple_items(self, request):
    '''
    get data about the items
    POST 
    {
        'action':'get',
        'start':0,
        'end':10,
    }
    Add format 
    {
        'action':'add',
        name: "klj"
        sales_price: 50000
        catagory: 1             <- catagory id
    }
    '''
    response_json = {'status':False, 'items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    items = Item.objects.filter(is_active=True).order_by('-id')
                    response_json['count'] = len(items)
                    items = items[int(data_json['start']):int(data_json['end'])]
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'category':
                    items = items = Item.objects.filter(is_active=True, catagory = ItemCatagory.objects.get(id=data_json['category_id'])).order_by('-id')
                    response_json['count'] = len(items)
                    items = items[int(data_json['start']):int(data_json['end'])]
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == "name":
                    items = Item.objects.filter(is_active=True, name__icontains = str(data_json['name']).lower() ).order_by('-id')
                    response_json['count'] = len(items)
                    items = items[int(data_json['start']):int(data_json['end'])]
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == "barcode":
                    items = Item.objects.filter(is_active=True, barcode__icontains=data_json['barcode'])
                    response_json['count'] = len(items)
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'multiple':
                    items = Item.objects.filter(is_active=True).order_by('-id')
                    if (data_json['filters']['is_applied_name']):
                        if(data_json['filters']['exact_name']):
                            items = items.filter(name=str(data_json['filters']['name']))
                        else:
                            items = items.filter(name__icontains=str(data_json['filters']['name']))
                    if(data_json['filters']['is_applied_weight_from']):
                        temp_start = data_json['filters']['weight_from']
                    else:
                        temp_start = 0
                    if (data_json['filters']['is_applied_weight_upto']):
                        temp_end = data_json['filters']['weight_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filters']['is_applied_weight_from'] == True or data_json['filters']['is_applied_weight_upto'] == True:
                        items = items.filter(weight__range = (temp_start, temp_end))

                    if(data_json['filters']['is_applied_average_cost_price_from']):
                        temp_start = data_json['filters']['average_cost_price_from']
                    else:
                        temp_start = 0
                    if (data_json['filters']['is_applied_average_cost_price_upto']):
                        temp_end = data_json['filters']['average_cost_price_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filters']['is_applied_average_cost_price_from'] == True or data_json['filters']['is_applied_average_cost_price_upto'] == True:
                        items = items.filter(average_cost_price__range = (temp_start, temp_end))

                    if(data_json['filters']['is_applied_stock_from']):
                        temp_start = data_json['filters']['stock_from']
                    else:
                        temp_start = 0
                    if (data_json['filters']['is_applied_stock_upto']):
                        temp_end = data_json['filters']['stock_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filters']['is_applied_stock_from'] == True or data_json['filters']['is_applied_stock_upto'] == True:
                        items = items.filter(stock__range = (temp_start, temp_end))


                    if(data_json['filters']['is_applied_sold_from']):
                        temp_start = data_json['filters']['sold_from']
                    else:
                        temp_start = 0
                    if (data_json['filters']['is_applied_sold_upto']):
                        temp_end = data_json['filters']['sold_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filters']['is_applied_sold_from'] == True or data_json['filters']['is_applied_stock_upto'] == True:
                        items = items.filter(sold__range = (temp_start, temp_end))

                    if(data_json['filters']['is_applied_sales_price_from']):
                        temp_start = data_json['filters']['sales_price_from']
                    else:
                        temp_start = 0
                    if (data_json['filters']['is_applied_sales_price_upto']):
                        temp_end = data_json['filters']['sales_price_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filters']['is_applied_sales_price_from'] == True or data_json['filters']['is_applied_sales_price_upto'] == True:
                        items = items.filter(sales_price__range = (temp_start, temp_end))
                    if (data_json['filters']['is_applied_category']):
                        items = items.filter(catagory__id = int(data_json['filters']['category']))
                    count = len(items)
                    items = items[int(data_json['start']) : int(data_json['end'])]
                    return JsonResponse({'status':True, 'items':items_to_json(items), 'count' : count })
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_item(self, request):
    response_json = {'status':False}
    item = False
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']        
                item = Item.objects.create(
                    name = str(data_json['name']),
                    sales_price = data_json['sales_price'],
                    catagory = ItemCatagory.objects.get(id=int(data_json['catagory'])),
                    description = data_json['description'],
                    weight = data_json['weight'],
                    average_cost_price = data_json['average_cost_price'],
                    barcode = data_json['barcode'],
                    vat_enabled = data_json['vat_enabled'],
                    weight_unit = data_json['weight_unit']
                )
                item.save()
                log('inventory/item', 'create', item.id, str(item), {}, user)
                try:
                    if (data_json['product_images']):
                        for image_data in data_json['product_images']:
                            data = image_data['base64']
                            format, imgstr = data.split(';base64,') 
                            ext = format.split('/')[-1] 
                            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
                            x = ItemImage.objects.create(
                                category = image_data['category'],
                                item = item,
                            )
                            x.image = data
                            x.save()
                except Exception as exp:
                    return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                item.save()
                response_json['item'] = items_to_json([item])
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            if item:
                item.delete()
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_item_details(self, request):
    '''
    use only get to get data 

    POST For editing
    {
        'action':'update',
        id: 1
        name: "klj"
        is_active:True,
        catagory: 1
    }
    '''
    response_json = {'status':'', 'items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False}
            if data_json['action'] == "get":
                try:
                    if data_json['filter'] == 'purchase_item':
                        purchase_item = PurchaseItem.objects.get(uuid=data_json['uuid'])
                        item = purchase_item.item
                except Exception as ex:
                    item = Item.objects.get(id=int(data_json['item_id']), is_active=True )
                response_json['items'] = items_to_json([item])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@require_http_methods(['POST'])
@bind
def update_item(self, request):
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
            
            response_json = {'status':False}
            if data_json['action'] == "update":
                changes = {}
                item = Item.objects.get(id=int(data_json['item_id']))
                if data_json['name']:
                    changes['name'] : item.name
                    item.name = str(data_json['name'])
                if data_json['description']:
                    changes['description'] : item.description
                    item.description = (data_json['description'])
                if data_json['weight']:
                    changes['weight'] : item.weight
                    item.weight = (data_json['weight'])
                
                if data_json['sales_price']:
                    changes['sales_price'] : item.sales_price
                    item.sales_price = (data_json['sales_price'])
                if data_json['average_cost_price']:
                    changes['average_cost_price'] : item.average_cost_price
                    item.average_cost_price = (data_json['average_cost_price'])
                if data_json['barcode']:
                    changes['barcode'] : item.barcode
                    item.barcode = (data_json['barcode'])
                if data_json['vat_enabled']:
                    changes['vat_enabled'] : item.vat_enabled
                    item.vat_enabled = (data_json['vat_enabled'])
                if data_json['weight_unit']:
                    changes['weight_unit'] : item.weight_unit
                    item.weight_unit = (data_json['weight_unit'])
                if data_json['category']:
                    changes['category'] : item.category
                    category = ItemCatagory.objects.get(id=int(data_json['category']))
                    item.category = category
                try:
                    if (data_json['product_images']):
                        for image_data in data_json['product_images']:
                            data = image_data['base64']
                            format, imgstr = data.split(';base64,') 
                            ext = format.split('/')[-1] 
                            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
                            x = ItemImage.objects.create(
                                category = image_data['category'],
                                item = item,
                            )
                            x.image = data
                            x.save()
                            changes['product_image'] = 'changed'
                except Exception as exp:
                    return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                if data_json['remove_image']:
                    for id in data_json['remove_image']:
                        x = ItemImage.objects.get(id = id)
                        x.delete()
                        changes['product_image'] = 'removed'
                item.save()
                response_json = {'status':True}
                log('inventory/item', 'update', item.id, str(item), changes, user)

            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_items(self, request):
    '''
    {
        "items_id":[
            1,2
        ]
    }
    '''
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
            ids = data_json['items_id']
            for id in ids:
                item = Item.objects.get(id=int(id))
                item.is_active = False
                item.save()
                log('inventory/item', 'soft-delete', item.id, str(item), {}, user)
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



######################################## itemCatagory ########################################


@require_http_methods(['POST'])
@bind
def get_multiple_item_catagories(self, request):
    '''
    get data about the items
    POST to get data
    {
        'action':'get',
        'start':0,
        'end':10,
    }
    Add format 
    {
        action:add
        name: "klj"             
    }
    '''
    response_json = {'status':'False'}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    catagroies = ItemCatagory.objects.filter(is_active=True).order_by('-id')
                    response_json['count'] = len(catagroies)
                    catagroies = catagroies[int(data_json['start']):int(data_json['end'])]
                    response_json['item_catagories'] = item_catagories_to_json(catagroies, False)
                    response_json['status'] = True
                if data_json['filter'] == 'parent':
                    catagroies = ItemCatagory.objects.filter(is_active=True, parent=None).order_by('-id')
                    response_json['count'] = len(catagroies)
                    catagroies = catagroies[int(data_json['start']):int(data_json['end'])]
                    response_json['item_catagories'] = item_catagories_to_json(catagroies, False)
                    response_json['status'] = True
                if data_json['filter'] == "category":
                    catagroy = ItemCatagory.objects.get(is_active=True, id=data_json['category_id'])
                    response_json['category_details'] = item_catagories_to_json([catagroy], False)
                    categories = ItemCatagory.objects.filter(is_active=True, parent =catagroy)
                    response_json['sub_categories'] = item_catagories_to_json(categories)
                    response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_item_catagory(self, request):
    response_json = {'status':'False'}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check) 
        try:   
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                try:
                    parent = ItemCatagory.objects.get(id=data_json['parent'])
                except:
                    parent = None
                catagory = ItemCatagory.objects.create(
                    name = data_json['name'],
                    parent = parent
                )
                catagory.save()
                response_json['item_category'] = item_catagories_to_json([catagory])
                response_json['status'] = True
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']        
                log('inventory/item_category', 'create', catagory.id, str(catagory), {}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


def get_parent_categories(category):
    current = category
    loop = True
    sub  = {}
    data = {}
    while loop:
        if current.parent:
            details = item_catagories_to_json([current],False)
            data = {'details':details, 'sub_categories': data}
            current = current.parent
        else:
            details = item_catagories_to_json([current], False)
            data = {'details':details, 'sub_categories': data}
            loop = False
    return data


@require_http_methods(['POST'])
@bind
def get_item_catagory_details(self, request):
    '''
    POST For editing
    {
        'action':'update',
        is_active :True
        item_catagory_id: 1
        name: "klj"
    }
    '''
    response_json = {'status':'', 'items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            item_catagory = ItemCatagory.objects.get(id=int(data_json['item_category_id']))
            response_json = {'status':False}
            if data_json['action'] == "get":
                response_json['item_category'] = item_catagories_to_json([item_catagory])
                sub_categories = ItemCatagory.objects.filter(is_active=True, parent = item_catagory)
                response_json['sub_categories'] = item_catagories_to_json(sub_categories)
                response_json['parent_tree'] = get_parent_categories(item_catagory)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_item_category(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                item_catagory = ItemCatagory.objects.get(id=int(data_json['item_category_id']))
                old = item_catagory.name
                item_catagory.name = str(data_json['name'])
                try:
                    parent = ItemCatagory.objects.get(id=data_json['parent'])
                except:
                    parent = None
                item_catagory.parent = parent
                item_catagory.save()
                response_json = {'status':True}
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']        
                log('inventory/item_category', 'update', item_catagory.id, str(item_catagory), {'item_category.name':old}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_item_catagories(self, request):
    '''
    {
        "item_catagories_id":[
            1,2
        ]
    }
    '''
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
            ids = data_json['item_catagories_id']
            for id in ids:
                item_catagories = ItemCatagory.objects.get(id=int(id))
                item_catagories.is_active = False
                item_catagories.save()
                log('inventory/item_category', 'soft-delete', item_catagories.id, str(item_catagories), {}, user)
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


######################################## Place ########################################


@require_http_methods(['POST'])
@bind
def get_multiple_places(self, request):
    '''
    get data about the items
    POST to get data
    {
        'action':'get',
        'start':0,
        'end':10,
    }
    Add format 
    {
        action:add
        name: "klj"             
    }
    '''
    response_json = {'status':'False','placements':[]}

    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'item':
                    placements = Placement.objects.filter(item__id = data_json['item_id']).order_by('-id')
                    for p in placements:
                        if p.stock>0:
                            temp = {}
                            temp['id'] = p.id
                            temp['purchase_item'] = p.purchase_item.id
                            temp['purchase_item_details'] = {
                                'quantity':p.purchase_item.stock,
                                'purchase_price': p.purchase_item.purchase_price,
                                'vendor': p.purchase_item.purchase_order.vendor.first_name +  ' ' + p.purchase_item.purchase_order.vendor.last_name
                            }
                            temp['placed_on'] = p.placed_on.id
                            temp['sales_price'] = p.item.sales_price
                            temp['str_placed_on'] = p.placed_on.name
                            temp['stock'] = p.stock
                            response_json['placements'].append(temp)
                        else:
                            pass
                    response_json['status'] = True
                else:
                    response_json= {'places':[]}
                    places = Place.objects.filter(is_active=True).order_by('-id')
                    response_json['count'] = len(places)
                    places = places[int(data_json['start']):int(data_json['end'])]
                    for place in places:
                        response_json['places'].append({
                            'id':place.id,
                            'name':place.name,
                            'count_assignment':len(place.placements.filter(is_active=True))
                        })
                    response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_place(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False,'placements':[]}
            if data_json['action'] == "add":
                place = Place.objects.create(
                    name = data_json['name']
                )
                place.save()
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']        
                log('inventory/place', 'create', place.id, str(place), {}, user)
                response_json['status'] = True
            return JsonResponse( response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_place(self, request):
    '''
    POST For editing
    {
        'action':'update',
        place_id: 1
        name: "klj"
    }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            place = Place.objects.get(id=int(data_json['place_id']))
            response_json = {'status':False}
            if data_json['action'] == "update":
                data = {'token':request.headers['Authorization'].split(' ')[1]}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                log('inventory/place', 'update', place.id, str(place), {'name': place.name}, user)
                place.name = str(data_json['name'])
                place.save()
                response_json = {'status':True}
            if data_json['action'] == "get":
                response_json['places'] = places_to_json([place])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_single_place(self,request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                place = Place.objects.get(is_active=True, id=data_json['place_id'])
                response_json['place'] = {
                    'id':place.id,
                    'name':place.name,
                    'is_active':place.is_active,
                    'count_assignment':len(place.placements.filter(is_active=True))
                }
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def delete_places(self, request):
    '''
    {
        "places_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['places_id']
            
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            for id in ids:
                place_x = Place.objects.get(id=int(id))
                place_x.is_active = False
                place_x.save()
                log('inventory/place', 'soft-delete', place.id, str(place), {}, user)

            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

######################################## Placement ########################################


@require_http_methods(['POST'])
@bind
def assign_place(self, request):
    '''
    To increase quntity, there must be objects unassigned on the related purchase_item

    assign placement foramt : 
    {
        'action':'add',
        'place_id':1,
        'purchase_item':2,
        'stock':3        
    }
    Delete placement:
    {
        'action':'delete',
        'id':2
        'place_id':1,
        'purchase_item':3,
    }
    '''    
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
                place = Place.objects.get(id=int(data_json['place_id']))
                purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item_id']))
                if Placement.objects.filter(purchase_item=purchase_item, placed_on=place):
                    raise Exception('Item already exists in this place.')
                placement = Placement.objects.create(
                    purchase_item = purchase_item,
                    placed_on = place,
                    stock = int(data_json["quantity"])
                )
                placement.save()
                changes = {'items moved from default place to':place.name, ' quantity':placement.stock, ' purchase item':purchase_item.id}
                log('inventory/placement', 'create', place.id, str(place), changes, user)
                response_json['status'] = True

            if data_json['action'] == 'delete':
                placement = Placement.objects.get(id=int(data_json['placement_id']))
                placement_id = placement.id
                str_placement = str(placement)
                placement.delete()
                log('inventory/placement', 'delete', placement_id, str(str_placement), {}, user)
                response_json['status'] = True
            if data_json['action'] == 'update':
                placement = Placement.objects.get(id=int(data_json['placement_id']))
                placement.stock = int(data_json['quantity'])
                placement.save()
                response_json['status'] = True
                log('inventory/placement', 'update', placement.id, str(placement), {'quantity':placement.stock}, user)
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_placements(self, request):
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                start = data_json['start']
                end = data_json['end']
                if data_json['filter'] == 'none':
                    placements = Placement.objects.filter(is_active=True).order_by('-id')
                    response_json['count'] = len(placements)
                    placements = placements[start:end]
                    response_json['placements'] = placements_to_json(placements)
                if data_json['filter'] == 'item':
                    placements = Placement.objects.filter(is_active=True, item=data_json['item'])
                    response_json['count'] = len(placements)
                    placements = placements[start:end]
                    response_json['placements'] = placements_to_json(placements)
                if data_json['filter'] == 'place':
                    placements = Placement.objects.filter(is_active=True, placed_on=data_json['place'])
                    response_json['count'] = len(placements)
                    placements = placements[start:end]
                    response_json['placements'] = placements_to_json(placements)    
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})




# --------------------------------------------------------------------------------------------------------------------------------------------
@require_http_methods(['POST'])
@bind
def get_mulitple_purchase_items(self, request):
    '''
    function to add purchase item 
    {
        'action':'add',
        'item': 1,
        'purchase_order':5,
        'quantity':3,
        'non_discount_price': 234,
        'purchase_price':34234,
        'defective':55,
        'discount_type':'fixed',
        'discount':1351,
        'status':'addedtocirculation',

    }
    '''
    response_json = {'status':False, 'purchase_items':[]}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'get':
                if data_json['filter'] == 'item_on_default':
                    default = Place.objects.get(is_default=True)
                    purchase_items= PurchaseItem.objects.filter(item__id=int(data_json['item_id'])).order_by('-id')
                    response_json['count'] = len(purchase_items)
                    purchase_items = purchase_items[data_json['start']:data_json['end']]
                    for purchase_item in purchase_items:
                        temp = {}
                        try:
                            x = Placement.objects.get(placed_on=default, purchase_item=purchase_item)
                            if (x.stock>0):
                                temp = {
                                    'purchase_order_id': purchase_item.purchase_order.uuid,
                                    'id':purchase_item.id,
                                    'price':purchase_item.purchase_price,
                                    'vendor':str(purchase_item.purchase_order.vendor),
                                    'stock':purchase_item.stock,
                                    'on_default':x.stock
                                }
                                response_json['purchase_items'].append(temp)
                        except:
                            pass
                    response_json['status'] = True
                if data_json['filter'] == "barcode":
                    item = Item.objects.get(barcode = data_json['barcode'])
                    purchase_items = PurchaseItem.objects.filter(item__id = item.id).order_by('-id')
                    default = SalesSetting.objects.all()
                    default = default[0].default_place_to_sold_from
                    purchase_items= PurchaseItem.objects.filter(item__id= item.id).order_by('-id')
                    for purchase_item in purchase_items:
                        temp = {}
                        try:
                            x = Placement.objects.get(placed_on=default, purchase_item=purchase_item)
                            if (x.stock>0):
                                temp = {
                                    'item': items_to_json([item]),
                                    'purchase_order_id': purchase_item.purchase_order.uuid,
                                    'purchase_item_id':purchase_item.id,
                                    'price_from_purchase_item':purchase_item.purchase_price,
                                    'vendor':str(purchase_item.purchase_order.vendor),
                                    'stock':purchase_item.stock,
                                    'on_default':x.stock,
                                    'place_str': default.name,
                                    'place_id':default.id 
                                }
                                response_json['purchase_items'].append(temp)
                        except:
                            pass
                    response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@require_http_methods(['POST'])
@bind
def add_new_purchase_item(self, request):
    response_json = {'status':False, 'purchase_items':[]}
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
                purchase_item = PurchaseItem.objects.create(
                    item = Item.objects.get(id=int(data_json['item'])),
                    purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order'])),
                    quantity = int(data_json['quantity']),
                    non_discount_price = data_json['non_discount_price'],
                    defective = int(data_json['defective']),
                    discount_type = data_json['discount_type'],
                    discount = float(data_json['discount']),
                    status = data_json['status']
                    )                
                purchase_item.save()
                purchase_item.purchase_order.save()
                log('inventory/purchase_item', 'create', purchase_item.id, str(purchase_item), {'purchase_order':purchase_item.purchase_order.id}, user)
                response_json = {'status':True}
            if data_json['action'] == "add_multiple":
                for purchase_items_json in data_json['purchase_items']:
                    purchase_item = PurchaseItem.objects.create(
                        item = Item.objects.get(id=int(purchase_items_json['item'])),
                        purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order'])),
                        quantity = int(purchase_items_json['quantity']),
                        non_discount_price = purchase_items_json['non_discount_price'],
                        defective = int(purchase_items_json['defective']),
                        discount_type = purchase_items_json['discount_type'],
                        discount = float(purchase_items_json['discount']),
                        status = purchase_items_json['status']
                        )                
                    purchase_item.save()
                    purchase_item.purchase_order.save()
                    log('inventory/purchase_item', 'create', purchase_item.id, str(purchase_item), {'purchase_order':purchase_item.purchase_order.id}, user)
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


    


@require_http_methods(['POST'])
@bind
def get_purchase_item_details(self, request):
    '''
    function to update purchase item 
    {
        'action':'update',
        'item': 1,
        'purchase_order':5,
        'quantity':3,
        'non_discount_price': 234,
        'purchase_price':34234,
        'defective':55,
        'discount_type':'fixed',
        'discount':1351,
        'status':'addedtocirculation',
        'id':1,
    }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)    
            if data_json['action'] == 'get':
                if data_json['filter'] == 'uuid':
                    purchase_item = PurchaseItem.objects.get(uuid=data_json['uuid'])
                    return JsonResponse({'status':True, 'purchase_item':  purchase_items_to_json([purchase_item])})
                if data_json['filter'] == 'id':
                    purchase_item = PurchaseItem.objects.get(id=data_json['id'])
                    return JsonResponse({'status':True, 'purchase_item':  purchase_items_to_json([purchase_item])})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_purchase_item(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        data = {'token':request.headers['Authorization'].split(' ')[1]}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']    
        try:
            if data_json['action'] == "update":
                purchase_item = PurchaseItem.objects.get(id=data_json['id'])
                old_purchase_item = purchase_item
                purchase_item.status = 'incomplete'
                purchase_item.save()
                purchase_item.quantity = int(data_json['quantity'])
                purchase_item.non_discount_price = float(data_json['non_discount_price'])
                purchase_item.defective = int(data_json['defective'])
                purchase_item.discount_type = data_json['discount_type']
                purchase_item.discount = float(data_json['discount'])
                purchase_item.status = data_json['status']    
                purchase_item.save()
                purchase_item.purchase_order.save()
                log('inventory/purchase_item', 'update', purchase_item.id, str(purchase_item), {'purchase_order':purchase_item.purchase_order.id, 'old_purchase_item':purchase_items_to_json([old_purchase_item])}, user)
                response_json = {'status':True}
            if data_json['action'] == 'update_multiple':
                for purchase_item_json in data_json['purchase_items']:
                    purchase_item = PurchaseItem.objects.get(id=purchase_item_json['id'])
                    old_purchase_item = purchase_item
                    purchase_item.status = 'incomplete'
                    purchase_item.save()
                    purchase_item.quantity = int(purchase_item_json['quantity'])
                    purchase_item.non_discount_price = float(purchase_item_json['non_discount_price'])
                    purchase_item.defective = int(purchase_item_json['defective'])
                    purchase_item.discount_type = purchase_item_json['discount_type']
                    purchase_item.discount = float(purchase_item_json['discount'])
                    purchase_item.status = purchase_item_json['status']    
                    purchase_item.save()
                    purchase_item.purchase_order.save()
                    log('inventory/purchase_item', 'update', purchase_item.id, str(purchase_item), {'purchase_order':purchase_item.purchase_order.id, 'old_purchase_item':purchase_items_to_json([old_purchase_item])}, user)
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_purchase_items(self, request):
    '''
        {
            "purchase_items_id":[
                1,2
            ]
        }
    '''
    response_json = {'status':False}
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['purchase_items_id']
            orders = []
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
        
            for id in ids:
                z = PurchaseItem.objects.get(id=int(id))
                if z.purchase_order not in orders:
                    orders.append(z.purchase_order) 
                z.is_active = False
                z.status = 'incomplete'
                z.save()
                log('inventory/purchase_item', 'delete', z.id, str(z), {}, user)
                z.delete()
            for order in orders:
                order.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@require_http_methods(['POST'])
@bind
def purchase_order_statuss(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            statuss = PurchaseOrderStatus.objects.all()
            data = []
            for status in statuss:
                temp =  StatusSerializer(status).data
                data.append(temp)
            return JsonResponse({'status':True, 'data':data})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})





@require_http_methods(['POST'])
@bind
def export_inventory(self, request):
    sensative = ['purchaseitem', 'invoiceitem', 'product_image', 'thumbnail_image', 'id', 'item_placements', 'is_active']
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)    
        try:
            response_json = {'status':False}
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                x = []
                temp = Item._meta.get_fields(include_hidden=True)
                for t in temp:
                    if t.name not in sensative:
                        x.append(t.name)
                return JsonResponse({'status':True,"fields":x})
            if (data_json['action'] == 'export' ):
                items = Item.objects.filter(is_active=True).order_by('-id')

                if (data_json['filters']['name']):
                    items = items.filter(name__icontains=str(data_json['filters']['name']))

                if data_json['filters']['weight']:
                    if data_json['filters']['weight']['from']:
                        items = items.filter(weight__gte = data_json['filters']['weight']['from'])
                    if data_json['filters']['weight']['upto']:
                        items = items.filter(weight__lte = data_json['filters']['weight']['upto'])
                    
                if data_json['filters']['average_cost_price']:
                    if data_json['filters']['average_cost_price']['from']:
                        items = items.filter(average_cost_price__gte = data_json['filters']['average_cost_price']['from'])
                    if data_json['filters']['average_cost_price']['upto']:
                        items = items.filter(average_cost_price__lte = data_json['filters']['average_cost_price']['upto'])

    
                if data_json['filters']['stock']:
                    if data_json['filters']['stock']['from']:
                        items = items.filter(stock__gte = data_json['filters']['stock']['from'])
                    if data_json['filters']['stock']['upto']:
                        items = items.filter(stock__lte = data_json['filters']['stock']['upto'])

                if data_json['filters']['sold']:
                    if data_json['filters']['sold']['from']:
                        items = items.filter(sold__gte = data_json['filters']['sold']['from'])
                    if data_json['filters']['sold']['upto']:
                        items = items.filter(sold__lte = data_json['filters']['sold']['upto'])

                if data_json['filters']['sales_price']:
                    if data_json['filters']['sales_price']['from']:
                        items = items.filter(sales_price__gte = data_json['filters']['sales_price']['from'])
                    if data_json['filters']['sales_price']['upto']:
                        items = items.filter(sales_price__lte = data_json['filters']['sold']['upto'])
              
                if (data_json['filters']['category']):
                    items = items.filter(catagory__id = int(data_json['filters']['category']))
                
                response_json['count'] = len(items)
                items = items[int(data_json['start']) : int(data_json['end'])]
                response_json['items'] = items_to_json(items)



                fields = (data_json['selected_fields'])
                selected_fields = []
                for key in fields:
                    if key not in sensative:
                        selected_fields.append(key)
                data = items_to_json_with_selection(items, selected_fields)

                if data_json['export'] == "pdf":
                    pdf = export_data(data,selected_fields)
                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "export_data"
                        content = "inline; filename='%s'" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                
                if data_json['export'] == "excel":
                    response = HttpResponse(content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="items_data.xls"'

                    wb = xlwt.Workbook(encoding='utf-8')
                    ws = wb.add_sheet('Items')

                    # Sheet header, first row
                    row_num = 0

                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True

                    columns = selected_fields

                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    font_style = xlwt.XFStyle()

                    rows = data
                    for row in rows:
                        row_num += 1
                        for col_num in range(len(row)):
                            ws.write(row_num, col_num, row[col_num], font_style)

                    wb.save(response)
                    return response

            return JsonResponse({'status':False})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


def render_to_pdf(template_src, context_dict={}):
    template = get_template('export_items_data.html')
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def export_data(data, fields):
    template = get_template('export_items_data.html')
    data = {
    'today': datetime.date.today(), 
    'items':data,
    'headers':fields
    }
    html = template.render(data)
    pdf = render_to_pdf('export_items_data', data)
    return pdf


@require_http_methods(['POST'])
@bind
def dashboard_report(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        try:
            response_json['summary'] = {
                'active_items' : 0,
                'sold' : 0
            }
            if data_json['action'] == "get":
                items = Item.objects.filter(is_active = True).order_by('-id')
                response_json['summary']['active_items'] = len(items)
                response_json['summary']['sold'] = items.aggregate(Sum('sold'))['sold__sum']
                temp = items.filter().order_by('stock')
                response_json['summary']['low_stock_items'] = {
                    'items' : items_to_json(temp[data_json['filters']['low_items']['start']:data_json['filters']['low_items']['end']]),
                    'count' : len(temp)
                }
                temp = items.filter().order_by('-sold')
                response_json['summary']['most_sold_items'] = {
                    'items' : items_to_json(temp[data_json['filters']['most_sold_items']['start']:data_json['filters']['most_sold_items']['end']]),
                    'count' : len(temp)
                }
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

import uuid

@require_http_methods(['POST'])
@bind
def create_bar_code(self,request):
    response_json = {'status':False}        
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            code = 0
            response_json['barcode_images'] = []
            if data_json['action'] == 'create':
                if data_json['type'] == "barcode":
                    count = data_json['count']
                    for _ in range(count):
                        code = generate_code()
                        with open('temp.jpeg', 'wb') as image:
                            Code128(str(code), writer=ImageWriter()).write(image)
                        with open('temp.jpeg', 'rb') as image:
                            response_json['barcode_images'].append(
                                {
                                    'barcode': code,
                                    'image':base64.b64encode(image.read()).decode('utf-8')
                                }
                            )
                            response_json['status'] = True
                            response_json['count'] = len(response_json['barcode_images'])
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

def generate_code():
    code = uuid.uuid4()
    code = str(code).replace('-','')[:12].upper()
    if Item.objects.filter(barcode = code):
        code()
    else:
        return code

import pandas as pd

@require_http_methods(['POST'])
@bind
def import_data(self,request):
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
            if data_json['action'] == "import":
                csv = base64.b64decode(data_json['csv_file']).decode('utf-8')
                csv = csv.splitlines()
                column = csv[0].split(',')
                if len(csv) <= 1:
                    raise Exception("No data to import.")
                data_raw = csv[1:len(csv)]
                data = []
                for x in data_raw:
                    data.append( x.split(','))
                df = pd.DataFrame(data, columns=column)
                data = df.to_dict()
                try:
                    vendor = Vendor.objects.get(first_name = 'Old', last_name = 'Inventory')
                except:
                    vendor = Vendor.objects.create(
                        first_name= 'Old',
                        last_name= 'Inventory',
                        middle_name = '',
                        company = "Yes",
                        email = 'generic@dumb.com',
                        website= '',
                        tax_number = '00',
                        phone1 = '0',
                        phone2 = '0',
                        address = ' '
                    )
                try:
                    purchase_order = PurchaseOrder.objects.get(vendor = vendor, third_party_invoice_number = '0000001')
                except:
                    purchase_order = PurchaseOrder.objects.create(
                    third_party_invoice_number = '0000001',
                    added_by = user,
                    vendor = vendor,
                    invoiced_on = timezone.now(),
                    completed_on = timezone.now(),
                    total_cost = 0,
                    bill_amount = 0,
                    paid_amount = 0,
                    status = PurchaseOrderStatus.objects.filter(is_end = False)[0]
                    )
                purchase_items_data = []
                for i in range(len(data['name'])):
                    try:
                        category = ItemCatagory.objects.get(name = data['category'][i])
                    except:
                        category = ItemCatagory.objects.create(name = data['category'][i])
                    try:
                        item = Item.objects.get(name = data['name'][i], catagory = category, sales_price = data['sales_price'][i])
                    except:
                        if data['vat_enabled'][i] == 0:
                            x = False
                        else:
                            x = True
                        item = Item.objects.create(
                            name = data['name'][i],
                            description = data['description'][i],
                            catagory = category,
                            weight = data['weight'][i],
                            average_cost_price = data['purchase_price'][i],
                            sales_price = data['sales_price'][i],
                            weight_unit = 'g',
                            barcode = data['barcode'][i],
                            vat_enabled = x
                        )
                    print("here")
                    try:
                        purchase_item = PurchaseItem.objects.get(
                            item = item,
                            purchase_order = purchase_order, 
                            purchase_price = data['purchase_price'][i]
                        )
                        purchase_item.quantity = purchase_item.quantity + int(data['stock'][i])
                    except:
                        purchase_item = PurchaseItem.objects.create(
                            item = item,
                            purchase_order = purchase_order,
                            quantity = int(data['stock'][i]),
                            non_discount_price = float (data['purchase_price'][i]),
                            sold = 0,
                            defective = 0,
                            status = 'addedtocirculation'
                        )
                    purchase_items_data.append(purchase_item)
                    purchase_order.save()
                purchase_order.status = PurchaseOrderStatus.objects.get(is_end=True)
                purchase_order.save()
                response_json['purchase_order'] = purchase_orders_to_json([purchase_order])
                response_json['purchase_items'] = purchase_items_to_json(purchase_items_data)
                log('inventory/import', 'create', 0, str('data import'), {}, user)

                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})