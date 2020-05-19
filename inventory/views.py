from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import json
import datetime
from user_handler.models import Vendor, CustomUserBase
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement, PurchaseOrderStatus, ItemCatagory
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
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import StringIO
import cgi
from user_handler.permission_check import bind, check_permission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


@require_http_methods(['POST'])
@bind
def get_multiple_purchase_orders(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if str(data_json['action']).lower() == "get":
                start = int(data_json["start"])
                end = int(data_json["end"])
                response_json = {'status':'', 'p_orders':[]}
                if str(data_json['filter']).lower() == "none":
                    orders = PurchaseOrder.objects.filter(is_active=True).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "status":
                    status = PurchaseOrderStatus.objects.get(id=data_json['status_id'])
                    orders = PurchaseOrder.objects.filter(is_active=True, status=status).order_by('-invoiced_on')[start:end]                
                # filter using date, will have to do after front-end
                if str(data_json['filter']).lower() == "date":
                    start_date = str_to_datetime(str(data_json['start_date']))
                    end_date = str_to_datetime(str(data_json['end_date']))
                    orders = PurchaseOrder.objects.filter(is_active=True, invoiced_on__range = [start_date, end_date]).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "vendor":
                    vendor_obj = Vendor.objects.get(id=int(data_json['vendor']))
                    orders = PurchaseOrder.objects.filter(is_active=True, vendor=vendor_obj).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "added_by":
                    added_by_obj = CustomUserBase.objects.get(id=int(data_json['added_by']))
                    orders = PurchaseOrder.objects.filter(is_active=True, added_by=added_by_obj).order_by('-invoiced_on')[start:end]            
                response_json['p_orders'] = purchase_orders_to_json(orders)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_purchase_order(self,request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
                    total_cost = data_json['total_cost'],
                    discount_type = data_json['discount_type'],
                    discount = data_json['discount'],
                    added_by = user,
                    vendor = Vendor.objects.get(id=int(data_json['vendor'])),
                    invoiced_on = str_to_datetime(data_json['invoiced_on']),
                    completed_on = str_to_datetime(data_json['completed_on']),
                    third_party_invoice_number = data_json['third_party_invoice_number'],
                    status = status          
                )
                purchase_order.save()
                response_json['status'] = True
                response_json['p_orders'] = purchase_orders_to_json([purchase_order])
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order_id']))
                purchase_order.total_cost = data_json['total_cost']
                purchase_order.discount_type = data_json['discount_type']
                purchase_order.discount = data_json['discount']
                purchase_order.vendor = Vendor.objects.get(id=int(data_json['vendor']))
                purchase_order.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                purchase_order.completed_on = str_to_datetime(data_json['completed_on'])
                purchase_order.status = PurchaseOrderStatus.objects.get(id=int(data_json['status']))
                purchase_order.third_party_invoice_number = data_json['third_party_invoice_number']
                purchase_order.save()
                response_json = {'status':True}
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "delete":
                ids = data_json['purchase_orders_id']
                for id in ids:
                    purchase_order = PurchaseOrder.objects.get(id=int(id))
                    purchase_order.is_active = False
                    purchase_order.status = PurchaseOrderStatus.objects.filter(is_end=False)[0]
                    purchase_order.save()
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    vendors = Vendor.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
                    added_by = user
                )
                vendor.save()
                response_json['vendors'] = vendors_to_json([vendor])
                response_json = {'status':True}
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['vendors_id']
            if ids is None:
                raise Exception('Empty Vendor list')
            for id in ids:
                vendor = Vendor.objects.get(id=int(id))
                vendor.is_active = False
                vendor.save()
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                vendor = Vendor.objects.get(id=int(data_json['vendor_id']))
                vendor.first_name = str(data_json['first_name'])
                vendor.last_name = str(data_json['last_name'])
                vendor.middle_name = str(data_json['middle_name'])
                vendor.email = str(data_json['email'])
                vendor.website = str(data_json['website'])
                vendor.tax_number = str(data_json['tax_number'])
                vendor.phone1 = str(data_json['phone1'])
                vendor.phone2 = str(data_json['phone2'])
                vendor.address = str(data_json['address'])
                vendor.is_active = (data_json['is_active'])
                vendor.save()
                response_json = {'status':True}
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "none":
                    items = Item.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == "name":
                    items = Item.objects.filter(is_active=True, name__icontains = str(data_json['name']).lower() ).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['items'] = items_to_json(items)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                if data_json['filter'] == 'multiple':
                    items = Item.objects.filter(is_active=True)
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
                    if (data_json['filters']['is_applied_catagory']):
                        items = items.filter(catagory__id = int(data_json['filters']['catagory']))
                    items = items[int(data_json['start']) : int(data_json['end'])]
                    return JsonResponse({'status':True, 'items':items_to_json(items)})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_item(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                item = Item.objects.create(
                    name = str(data_json['name']),
                    sales_price = data_json['sales_price'],
                    catagory = ItemCatagory.objects.get(id=int(data_json['catagory'])),
                    description = data_json['description'],
                    weight = data_json['weight'],
                    average_cost_price = data_json['average_cost_price']
                )
                item.save()
                try:
                    if (data_json['new_product_image']):
                        data = data_json['new_product_image'][0]['base64']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                        item.product_image = data
                except:
                    pass
                try:
                    if (data_json['new_thumbnail_image']):
                        data = data_json['new_thumbnail_image'][0]['base64']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                        item.thumbnail_image = data
                except:
                    pass
                item.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):            
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False}
            if data_json['action'] == "update":
                item = Item.objects.get(id=int(data_json['item_id']))
                item.name = str(data_json['name'])
                item.catagory = ItemCatagory.objects.get(id=int(data_json['catagory']))
                item.is_active = data_json['is_active']
                item.description = data_json['description']
                item.weight = data_json['weight']
                item.sales_price = data_json['sales_price']
                item.average_cost_price =  data_json['average_cost_price']
                try:
                    if (data_json['product_image']):
                        data = data_json['product_image'][0]['base64']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                        item.product_image = data
                except Exception as exp:
                    return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                try:
                    if (data_json['thumbnail_image']):
                        data = data_json['thumbnail_image'][0]['base64']
                        format, imgstr = data.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                        item.thumbnail_image = data
                except Exception as exp:
                    return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                item.save()
                response_json = {'status':True}
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':''}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['items_id']
            for id in ids:
                item = Item.objects.get(id=int(id))
                item.is_active = False
                item.save()
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    catagroies = ItemCatagory.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['item_catagories'] = item_catagories_to_json(catagroies)
                    response_json['status'] = True
                if data_json['filter'] == "category":
                    catagroy = ItemCatagory.objects.get(is_active=True, id=data_json['category_id'])
                    response_json['category_details'] = item_catagories_to_json([catagroy])
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]): 
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
                response_json['status'] = True
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                item_catagory = ItemCatagory.objects.get(id=int(data_json['item_category_id']))
                item_catagory.name = str(data_json['name'])
                item_catagory.is_active = data_json['is_active']
                try:
                    parent = ItemCatagory.objects.get(id=data_json['parent'])
                except:
                    parent = None
                item_catagory.parent = parent
                item_catagory.save()
                response_json = {'status':True}
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
    response_json = {'status':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['item_catagories_id']
            for id in ids:
                item_catagories = ItemCatagory.objects.get(id=int(id))
                item_catagories.is_active = False
                item_catagories.save()
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

    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'item':
                    placements = Placement.objects.filter(item__id = data_json['item_id'])
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
                    places = Place.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False,'placements':[]}
            if data_json['action'] == "add":
                place = Place.objects.create(
                    name = data_json['name']
                )
                place.save()
                response_json['status'] = True
            return response_json
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
    response_json = {'status':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            place = Place.objects.get(id=int(data_json['place_id']))
            response_json = {'status':False}
            if data_json['action'] == "update":
                place.name = str(data_json['name'])
                place.save()
                response_json = {'status':True}
            if data_json['action'] == "get":
                response_json['places'] = places_to_json([place])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



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
    response_json = {'status':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['places_id']
            for id in ids:
                place_x = Place.objects.get(id=int(id))
                place_x.is_active = False
                place_x.save()
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                place = Place.objects.get(id=int(data_json['place_id']))
                purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item']))
                placement = Placement.objects.create(
                    purchase_item = purchase_item,
                    placed_on = place,
                    stock = int(data_json["stock"])
                )
                placement.save()
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == 'delete':
                placement = Placement.objects.get(id=int(data_json['id']))
                placement.delete()
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == 'update':
                placement.stock = int(data_json['quantity'])
                placement.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})





@require_http_methods(['POST'])
@bind
def get_placements(self, request):
    request_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                start = data_json['start']
                end = data_json['end']
                if data_json['filter'] == 'none':
                    placements = Placement.objects.filter(is_active=True).order_by('-id')[start:end]
                    request_json['placements'] = placements_to_json(placements)
                if data_json['filter'] == 'item':
                    placements = Placement.objects.filter(is_active=True, item=data_json['item'])[start:end]
                    request_json['placements'] = placements_to_json(placements)
                if data_json['filter'] == 'place':
                    placements = Placement.objects.filter(is_active=True, placed_on=data_json['place'])[start:end]
                    request_json['placements'] = placements_to_json(placements)    
            request_json['status'] = True
            return JsonResponse(request_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'get':
                if data_json['filter'] == 'item_for_place':
                    default = Place.objects.get(is_default=True)
                    purchase_items= PurchaseItem.objects.filter(item__id=int(data_json['item_id']))
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
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@require_http_methods(['POST'])
@bind
def add_new_purchase_item(self, request):
    response_json = {'status':False, 'purchase_items':[]}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                purchase_item = PurchaseItem.objects.create(
                    item = Item.objects.get(id=int(data_json['item'])),
                    purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order'])),
                    quantity = int(data_json['quantity']),
                    purchase_price = data_json['purchase_price'],
                    defective = int(data_json['defective']),
                    discount_type = data_json['discount_type'],
                    discount = float(data_json['discount']),
                    status = data_json['status']
                    )                
                purchase_item.save()
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
    response_json = {'status':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)    
            if data_json['action'] == 'get':
                print(data_json)
                if data_json['filter'] == 'uuid':
                    print("here")
                    purchase_item = PurchaseItem.objects.get(uuid=data_json['uuid'])
                    return JsonResponse({'status':True, 'purchase_item':  purchase_items_to_json([purchase_item])})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_purchase_item(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        if data_json['action'] == "update":
            purchase_item = PurchaseItem.objects.get(id=data_json['id'])
            purchase_item.status = 'incomplete'
            purchase_item.save()
            purchase_item.quantity = int(data_json['quantity'])
            purchase_item.purchase_price = float(data_json['purchase_price'])
            purchase_item.defective = int(data_json['defective'])
            purchase_item.discount_type = data_json['discount_type']
            purchase_item.discount = float(data_json['discount'])
            purchase_item.status = data_json['status']    
            purchase_item.save()
            response_json = {'status':True}
        return JsonResponse(response_json)
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
    response_json = {'status':''}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['purchase_items_id']
            for id in ids:
                z = PurchaseItem.objects.get(id=int(id))
                z.is_active = False
                z.status = 'incomplete'
                z.save()
                z.delete()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@require_http_methods(['POST'])
@bind
def purchase_order_statuss(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    sensative = ['purchaseitem', 'invoiceitem', 'product_image', 'thumbnail_image', 'id', 'item_placements']
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                model = str(data_json['model']).lower()
                x = []
                if model == 'item':
                    temp = Item._meta.get_fields(include_hidden=True)
                    for t in temp:
                        if t.name not in sensative:
                            x.append(t.name)
                    return JsonResponse({'status':True,"fields":x})
            if (data_json['action'] == 'export' ):
                items = Item.objects.filter(is_active=True)
                model = str(data_json['model']).lower()
                if data_json['model'] == 'item':
                    if (data_json['filter']['is_applied_name']):
                        if(data_json['filter']['exact_name']):
                            items = items.filter(name=str(data_json['filter']['name']))
                        else:
                            items = items.filter(name__icontains=str(data_json['filter']['name']))
                
                    if(data_json['filter']['is_applied_weight_from']):
                        temp_start = data_json['filter']['weight_from']
                    else:
                        temp_start = 0
                    if (data_json['filter']['is_applied_weight_upto']):
                        temp_end = data_json['filter']['weight_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filter']['is_applied_weight_from'] == True or data_json['filter']['is_applied_weight_upto'] == True:
                        items = items.filter(weight__range = (temp_start, temp_end))
 
                    if(data_json['filter']['is_applied_average_cost_price_from']):
                        temp_start = data_json['filter']['average_cost_price_from']
                    else:
                        temp_start = 0
                    if (data_json['filter']['is_applied_average_cost_price_upto']):
                        temp_end = data_json['filter']['average_cost_price_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filter']['is_applied_average_cost_price_from'] == True or data_json['filter']['is_applied_average_cost_price_upto'] == True:
                        items = items.filter(average_cost_price__range = (temp_start, temp_end))

                    if(data_json['filter']['is_applied_stock_from']):
                        temp_start = data_json['filter']['stock_from']
                    else:
                        temp_start = 0
                    if (data_json['filter']['is_applied_stock_upto']):
                        temp_end = data_json['filter']['stock_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filter']['is_applied_stock_from'] == True or data_json['filter']['is_applied_stock_upto'] == True:
                        items = items.filter(stock__range = (temp_start, temp_end))
 

                    if(data_json['filter']['is_applied_sold_from']):
                        temp_start = data_json['filter']['sold_from']
                    else:
                        temp_start = 0
                    if (data_json['filter']['is_applied_sold_upto']):
                        temp_end = data_json['filter']['sold_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filter']['is_applied_sold_from'] == True or data_json['filter']['is_applied_stock_upto'] == True:
                        items = items.filter(sold__range = (temp_start, temp_end))
 


                    if(data_json['filter']['is_applied_sales_price_from']):
                        temp_start = data_json['filter']['sales_price_from']
                    else:
                        temp_start = 0
                    if (data_json['filter']['is_applied_sales_price_upto']):
                        temp_end = data_json['filter']['sales_price_upto']
                    else:
                        temp_end = 9999999999999
                    if data_json['filter']['is_applied_sales_price_from'] == True or data_json['filter']['is_applied_sales_price_upto'] == True:
                        items = items.filter(sales_price__range = (temp_start, temp_end))
 

                    if (data_json['filter']['is_applied_catagory']):
                        items = items.filter(catagory__id = int(data_json['filter']['catagory']))
                    
                    if (data_json['showItems']):
                        items = items[int(data_json['start']) : int(data_json['end'])]
                        return JsonResponse({'status':True, 'items':items_to_json(items)})

                    fields = (data_json['filter']['fields'])
                    selected_fields = []
                    for key in fields:
                        if key not in sensative:
                            if fields[key] == True:
                                selected_fields.append(key)
                    data = items_to_json_with_selection(items, selected_fields)
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
                    return HttpResponse("Not found")

            return JsonResponse({'status':True})
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
