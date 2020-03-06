from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import json
import datetime
from user_handler.models import Vendor, CustomUserBase
from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
from .utils import purchase_orders_to_json, purchase_items_to_json, str_to_datetime, vendors_to_json, items_to_json, item_catagories_to_json, places_to_json
from .exceptions import  EmptyValueException
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@login_required
@require_http_methods(['POST'])
# get/serach or add purchase orders
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
        "action":"get",
        "start":0,
        "end":5,
        "filter":"date",
        "start_date": "2020-02-06T11:03:03",
        "end_date": "2020-03-06T11:05:03"
    }
    filter by vendor :
    {
        "action":"get",
        "start":0,
        "end":5,
        "filter":"vendor",
        "vendor":1
    }
    filter by status: 
    {
        "action":"get",
        "start":0,
        "end":5,
        "filter":"status",
        "status":"sent"
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
    add : 
    {
        'action':'add',
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
                    orders = PurchaseOrder.objects.filter(is_active=True).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "status":
                    orders = PurchaseOrder.objects.filter(is_active=True, status=str(data_json['status']).upper()).order_by('-invoiced_on')[start:end]                
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
            if str(data_json['action'] == "add"):
                purchase_order = PurchaseOrder.objects.create(
                    total_cost = data_json['total_cost'],
                    discount_type = data_json['discount_type'],
                    discount = data_json['discount'],
                    added_by = CustomUserBase.objects.get(id=int(data_json["added_by"])),
                    vendor = Vendor.objects.get(id=int(data_json['vendor'])),
                    invoiced_on = str_to_datetime(data_json['invoiced_on']),
                    completed_on = str_to_datetime(data_json['completed_on']),
                    status = str(data_json['status']).upper()                    
                )
                purchase_order.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@login_required
#edit purchase order 

@require_http_methods(['POST', 'GET'])
def purchase_order(request,id):
    ''' To get data about single purchase order
    To get info about a single purchase_order, trigger /apiv1/inventory/porders/<purchase_order_id>/
    To edit the data, you can POST on the same link: 
    POST format:
    {
        'action':'edit',
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
            if data_json['action'] == "edit":
                purchase_order = PurchaseOrder.objects.get(id=int(data_json['id']))
                purchase_order.total_cost = data_json['total_cost']
                purchase_order.discount_type = data_json['discount_type']
                purchase_order.discount = data_json['discount']
                purchase_order.added_by = CustomUserBase.objects.get(id=int(data_json["added_by"])) 
                purchase_order.vendor = Vendor.objects.get(id=int(data_json['vendor']))
                purchase_order.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                purchase_order.completed_on = str_to_datetime(data_json['completed_on'])
                purchase_order.status = str(data_json['status']).upper()
                purchase_order.save()
                response_json = {'status':True}
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
        return JsonResponse(response_json)
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
def delete_purchase_orders(request):
    '''
    {
        "purchase_orders_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['purchase_orders_id']
            for id in ids:
                purchase_order = PurchaseOrder.objects.get(id=int(id))
                purchase_order.is_active = False
                purchase_order.save()
                for p_item in PurchaseItem.objects.filter(purchase_order = purchase_order):
                    p_item.is_active = False
                    p_item.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



######################################## Vendor  ########################################

# @login_required
@require_http_methods(['POST'])
def vendors(request):
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
    response_json = {'status':'', 'vendors':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
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
                    added_by = CustomUserBase.objects.get(id=request.user.id)
                )
                vendor.save()
                response_json['vendors'] = vendors_to_json([vendor])
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                vendors = Vendor.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                response_json['vendors'] = vendors_to_json(vendors)
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def delete_vendors(request):
    '''
    {
        "vendors_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
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
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST', 'GET'])
def vendor(request, id):
    '''
    TO get data [GET] to the url : /apiv1/inventory/vendors/<vendor id>
    To edit [POST] 
    Format : 
    {
        "action":"edit",
        "id":2,
        "first_name": "Raven2",
        "middle_name": "Ulric2 Davenport",
        "last_name": "Solomon2",
        "email": "qadeg@maili2nator.net",
        "website": "https://www.dogotime.org.uk",
        "tax_number": "974",
        "phone1": "+1 (149) 119-4092",
        "phone2": "+1 (381) 765-8778",
        "address": "Qui in at culpa unde",
        "is_active":true
    }
    '''
    response_json = {'status':'', 'vendors':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "edit":
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


######################################## Items ########################################
@login_required
@require_http_methods(['POST'])
def items(request):
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
    response_json = {'status':'', 'items':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                items = Item.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                response_json['items'] = items_to_json(items)
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == "add":
                item = Item.objects.create(
                    name = str(data_json['name']),
                    sales_price = data_json['sales_price'],
                    catagory = Catagory.objects.get(id=int(data_json['catagory']))
                )
                item.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required

@require_http_methods(['POST', 'GET'])
def item(request, id):
    '''
    use only get to get data 

    POST For editing
    {
        'action':'edit',
        id: 1
        name: "klj"
        is_active:True,
        catagory: 1
    }
    '''
    response_json = {'status':'', 'items':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            item = Item.objects.get(id=int(data_json['id']))
            response_json = {'status':False}
            if data_json['action'] == "edit":
                item.name = str(data_json['name'])
                item.catagory = ItemCatagory.objects.get(id=int(data_json['catagory']))
                item.is_active = data_json['is_active']
                item.save()
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    try:
        item = Item.objects.get(id=int(id))
        response_json['items'] = items_to_json([item])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def delete_items(request):
    '''
    {
        "items_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
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
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



######################################## itemCatagory ########################################

@login_required
@require_http_methods(['POST'])
def item_catagories(request):
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
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                catagroies = ItemCatagory.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                response_json['item_catagories'] = item_catagories_to_json(catagroies)
                response_json['status'] = True
            if data_json['action'] == "add":
                catagory = ItemCatagory.objects.create(
                    name = data_json['name']
                )
                catagory.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST', 'GET'])
def item_catagory(request, id):
    '''
    POST For editing
    {
        'action':'edit',
        is_active :True
        id: 1
        name: "klj"
    }
    '''
    response_json = {'status':'', 'items':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            item_catagory = ItemCatagory.objects.get(id=int(data_json['id']))
            response_json = {'status':False}
            if data_json['action'] == "edit":
                item_catagory.name = str(data_json['name'])
                item_catagory.is_active = data_json['is_active']
                item.save()
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    try:
        item_catagory = ItemCatagory.objects.get(id=int(id))
        response_json['item_catagories'] = item_catagories_to_json([item_catagory])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST', 'GET'])
def delete_item_catagories(request):
    '''
    {
        "item_catagories_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
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


######################################## Place ########################################
@login_required
@require_http_methods(['POST'])
def places(request):
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
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                places = Place.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                response_json['places'] = places_to_json(places)
                response_json['status'] = True
            if data_json['action'] == "add":
                place = Place.objects.create(
                    name = data_json['name']
                )
                place.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST', 'GET'])
def place(request, id):
    '''
    POST For editing
    {
        'action':'edit',
        id: 1
        name: "klj"
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            place = Place.objects.get(id=int(data_json['id']))
            response_json = {'status':False}
            if data_json['action'] == "edit":
                place.name = str(data_json['name'])
                place.save()
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    try:
        place = Place.objects.get(id=int(id))
        response_json['places'] = places_to_json([place])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def delete_places(request):
    '''
    {
        "places_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['places_id']
            for id in ids:
                places_id = Place.objects.get(id=int(id))
                place.is_active = False
                place.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


######################################## Placement ########################################
@login_required
@require_http_methods(['POST'])
def assign_place(request):
    '''
    To increase quntity, there must be objects unassigned on the related purchase_item

    assign placement foramt : 
    {
        'action':'assign',
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
    edit quantity in the placement 
    {
        'action':'edit',
        'id':3,
        'stock':3        
    }
    '''    
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "assign":
                place = Place.objects.get(id=int(data_json['place_id']))
                purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item']))
                placement = Placement.objects.create(
                    item = purchase_item,
                    place_on = place,
                    stock = int(data_json["quantity"])
                )
                placement.save()
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == 'delete':
                placement = Placement.objects.get(id=int(data_json['id']))
                placement.delete()
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == 'edit':
                placement = Placement.objects.get(id= int(data_json['id']))
                placement.stock = int(data_json['quantity'])
                placement.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@login_required
@require_http_methods(['POST'])
def purchase_items(request):
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
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                purchase_item = PurchaseItem.objects.create(
                    item = Item.objects.get(id=int(data_json['item'])),
                    purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order'])),
                    quantity = int(data_json['quantity']),
                    non_discount_price = data_json['non_discount_price'],
                    purchase_price = data_json['purchase_price'],
                    defective = data_json['defective'],
                    discount_type = data_json['discount_type'],
                    discount = data_json['discount'],
                    status = data_json['status']
                    )                
                purchase_item.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
        response_json = {'status':'', 'p_items':[]}
        # try:

        #     purchase_item = PurchaseOrder.objects.get(id=int(id))
        #     response_json['p_items'] = purchase_items_to_json([purchase_item])        
        #     response_json['status'] = True
        #     return JsonResponse(response_json)
        # except(ObjectDoesNotExist) as exp:
        #     return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
@require_http_methods(['POST', 'GET'])
def purchase_item(request, id):
    '''
    function to edit purchase item 
    {
        'action':'edit',
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
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                purchase_item = PurchaseItem.objects.get(id=id)
                purchase_item.item = Item.objects.get(id=int(data_json['item'])),
                purchase_item.purchase_order = PurchaseOrder.objects.get(id=int(data_json['purchase_order'])),
                purchase_item.quantity = int(data_json['quantity']),
                purchase_item.non_discount_price = data_json['non_discount_price'],
                purchase_item.purchase_price = data_json['purchase_price'],
                purchase_item.defective = data_json['defective'],
                purchase_item.discount_type = data_json['discount_type'],
                purchase_item.discount = data_json['discount'],
                purchase_item.status = data_json['status']              
                purchase_item.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def delete_purchase_items(request):
    '''
        {
            "purchase_items_id":[
                1,2
            ]
        }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['purchase_items_id']
            for id in ids:
                purhcase_item = PurchaseItem.objects.get(id=int(id))
                purchase_item.is_active = False
                purchase_item.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})