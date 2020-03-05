from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import json
import datetime
from user_handler.models import Vendor, CustomUserBase
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
from .utils import purchase_orders_to_json, purchase_items_to_json, str_to_datetime, vendors_to_json, items_to_json
from .exceptions import  EmptyValueException
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@login_required
@require_http_methods(['POST'])
def purchase_orders(request):
    '''
    View for handling operations related to Purchase orders
    fomats : 
    GET: 
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'none',/'date',/'vendor',/'added_by',
    }
    filter by date :
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'date',
        'start_date': "2019-11-16T08:15:00.000",
        'end_date': "2019-11-16T08:15:00.000",
    }
    filter by vendor :
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'vendor',
        'vendor_id':1
    }
    filter by status: 
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'status',
        'status':'draft'
    }
    filter by multiple:
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'multiple',
        'status':'draft',
        'vendor_id':1,
        ...... 
        # need more work after colaborating with front end
    }
    '''
    # This serach method can be optimized futher more
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if str(data_json['action']).lower() == "get":
                start = int(data_json["start"])
                end = int(data_json["end"])
                response_json = {'status':'', 'p_orders':[]}
                if str(data_json['filter']).lower() == "none":
                    orders = PurchaseOrder.objects.filter().order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "status":
                    orders = PurchaseOrder.objects.filter(status=str(data_json['status']).upper()).order_by('-invoiced_on')[start:end]                
                # filter using date, will have to do after front-end
                if str(data_json['filter']).lower() == "date":
                    start_date = str_to_datetime(str(data_json['start_date']))
                    end_date = str_to_datetime(str(data_json['end_date']))
                    orders = PurchaseOrder.objects.filter(invoiced_on__range = [start_date, end_date]).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "vendor":
                    vendor_obj = Vendor.objects.get(id=int(data_json['vendor']))
                    orders = PurchaseOrder.objects.filter(vendor=vendor_obj).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "added_by":
                    added_by_obj = CustomUserBase.objects.get(id=int(data_json['added_by']))
                    orders = PurchaseOrder.objects.filter(added_by=added_by_obj).order_by('-invoiced_on')[start:end]    
                response_json['p_orders'] = purchase_orders_to_json(orders)
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@login_required
@require_http_methods(['GET', 'POST'])
def purchase_order(request,id):
    ''' To get data about single purchase order
    To get info about a single purchase_order, trigger /apiv1/inventory/porders/<purchase_order_id>/
    To edit the data, you can POST on the same link: 
    POST format:
    {
        'action':'post',
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
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            purchase_order = PurchaseOrder.objects.get(id=int(data_json['id']))
            purchase_order.total_cost = data_json['total_cost']
            purchase_order.discount_type = data_json['discount_type']
            purchase_order.discount = data_json['discount']
            purchase_order.added_by = CustomUserBase.objects.get(id=int(data_json["added_by"])) 
            purchase_order.vendor = Vendor.objects.get(id=int(data_json['vendor']))
            ### change data after being final about date format 
            purchase_order.invoiced_on = str_to_datetime(data_json['invoiced_on'])
            purchase_order.completed_on = str_to_datetime(data_json['completed_on'])
            purchase_order.status = str(data_json['status']).upper()
            purchase_order.save()
            response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    response_json = {'status':'', 'p_order':{}, 'p_items':[]}
    try:
        order = PurchaseOrder.objects.get(id=int(id))
        response_json['p_order'] = purchase_orders_to_json([order])
        response_json['p_items'] = purchase_items_to_json(PurchaseItem.objects.filter(purchase_order=order))        
        response_json['status'] = True
        return JsonResponse(response_json)
    except(ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@login_required
@require_http_methods(['POST'])
def vendors(request):
    '''
    Fucntion to get vendors data
    POST Format:
    {
        'action':"get",
        'start':0,
        'end':20
    } 
    '''
    response_json = {'status':'', 'vendors':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            vendors = Vendor.objects.filter().order_by('id')[int(data_json['start']):int(data_json['end'])]
            response_json['vendors'] = vendors_to_json(vendors)
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
def vendor(request, id):
    '''
    TO get data [GET] to the url : /apiv1/inventory/vendors/<vendor id>
    To edit [POST] 
    Format : 
    {
        id: 1
        first_name: "kj"
        middle_name: "lkj"
        last_name: "lkj"
        email: "kj@l.com"
        website: "lkj"
        tax_number: "lkj"
        phone1: "lkj"
        phone2: "lkj"
        address: "lkj"
        is_active: true
        added_by: 1
    }
    '''

    response_json = {'status':'', 'vendors':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            vendor = Vendor.objects.get(id=int(data_json['id']))
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
            vendor.added_by = CustomUserBase.objects.get(id=int(data_json['added_by']))
            vendor.save()
            response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

    try:
        vendor = Vendor.objects.get(id=int(id))
        response_json['vendors'] = vendors_to_json([vendor])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
def items(request):
    '''
    get data about the items
    POST 
    {
        'action':'get',
        'start':0,
        'end':10,
    }
    '''
    response_json = {'status':'', 'items':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            items = Item.objects.filter().order_by('id')[int(data_json['start']):int(data_json['end'])]
            response_json['items'] = items_to_json(items)
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
def item(request, id):
    response_json = {'status':'', 'items':[]}
    try:
        item = Item.objects.get(id=int(id))
        response_json['items'] = items_to_json([item])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
