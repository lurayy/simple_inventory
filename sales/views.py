from .models import Invoice, InvoiceItem
from inventory.utils import str_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(['GET', 'POST'])
def invoices(request):
    ''' fucntion to get data from sales, will add filter later
    filter = None
    {
        'action':'get',
        'filter':'none',
        'start':0,
        'end':10,        
    }

    filter = Status
    {
        'action':'get',
        'filter':'status',
        'start':0,
        'end':10,
        'status':'draft'/'sent'/'due'/'paid'        
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
    filter by customer :
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'customer',
        'customer_id':1
    }
    filter by multiple:
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'multiple',
        'status':'draft',
        'customer_id':1,
        ...... 
        # need more work after colaborating with front end
    }
    add : 
    {
        'action':'add',
    }
    '''
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if str(data_json['action']) == "get":
                start = int(data_json["start"])
                end = int(data_json["end"])
                response_json = {'status':'', 'sales':[]}
                if str(data_json['filter']).lower() == "none":
                    invoices = Invoice.objects.filter(is_active=True).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "status":
                    invoices = Invoice.objects.filter(is_active=True, status=str(data_json['status']).upper()).order_by('-invoiced_on')[start:end]            
                # filter using date, will have to do after front-end
                if str(data_json['filter']).lower() == "date":
                    start_date = str_to_datetime(str(data_json['start_date']))
                    end_date = str_to_datetime(str(data_json['end_date']))
                    invoices = Invoice.objects.filter(is_active=True, invoiced_on__range = [start_date, end_date]).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "customer":
                    customer_obj = Customer.objects.get(is_active=True, id=int(data_json['customer_id']))
                    invoices = Invoice.objects.filter(customer=customer_obj).order_by('-invoiced_on')[start:end]
                if str(data_json['filter']).lower() == "added_by":
                    added_by_obj = CustomUserBase.objects.get(id=int(data_json['added_by']))
                    invoices = Invoice.objects.filter(is_active=True, added_by=added_by_obj).order_by('-invoiced_on')[start:end] 
                response_json['invoices'] = invoices_to_json(invoices)
                response_json['status'] = True
                return JsonResponse(response_json)
            # add after frontend
            if str(data_json['action'] == "add"):
                pass
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
@require_http_methods(['GET', 'POST'])
#edit invoice order 
def invoice(request,id):
    ''' To get data about single purchase order
    To get info about a single invoice, trigger /apiv1/inventory/porders/<invoice_id>/
    To edit the data, you can POST on the same link: 
    POST format:
    {
        'action':'edit',
        'id':1,
        'invoiced_on': "2019-11-16T08:15:00.000",
        'completed_on: "2019-11-16T08:15:00.000",
        'paid_amount': 2500,
        'added_by':1,                <- added_by id
        'customer':1,                  <- customer id 
        'status':'paid',

    }
    '''
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['edit'] == "edit":
                invoice = PurchaseOrder.objects.get(id=int(data_json['id']))
                invoice.total_cost = data_json['total_cost']
                invoice.added_by = CustomUserBase.objects.get(id=int(data_json["added_by"])) 
                invoice.customer = Customer.objects.get(id=int(data_json['customer']))
                invoice.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                invoice.completed_on = str_to_datetime(data_json['completed_on'])
                invoice.status = str(data_json['status']).upper()
                invoice.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    response_json = {'status':'', 'invoice':{}, 'invoice_items':[]}
    try:
        invoice = Invoice.objects.get(id=int(id))
        response_json['invoice'] = invoices_to_json([order])
        response_json['invoice_items'] = invoice_items_to_json(InvoiceItem.objects.filter(invoice=invoice))        
        response_json['status'] = True
        return JsonResponse(response_json)
    except(ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
def delete_invoices(request):
    '''
    {
        "invoices_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['invoices_id']
            if ids is None:
                raise Exception('Empty Invoice list')
            for id in ids:
                invoice = Invoice.objects.get(id=int(id))
                invoice.is_active = False
                invoice.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



######################################## Customer  ########################################

@login_required
@require_http_methods(['POST'])
def customers(request):
    '''
    Fucntion to get and add customers data
    POST Format:
    {
        'action':"get",
        'start':0,
        'end':20
    } 
    add format : 
    {
        'action':'add',
        first_name: "lkj"
        middle_name: "lkj"
        last_name: "lk"
        email: "jlk@c.com"
        website: "j"
        tax_number: "lkj"
        phone1: "lk"
        phone2: "j"
        address: "lk"
    }
    '''
    response_json = {'status':'', 'customers':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                customer = Customer.objects.create(
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
                customer.save()
                response_json['customers'] = customers_to_json([customer])
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                customers = Customer.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                response_json['customers'] = customers_to_json(customer)
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
def delete_customers(request):
    '''
    {
        "customers_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['customers_id']
            if ids is None:
                raise Exception('Empty Customers list')
            for id in ids:
                customer = Customer.objects.get(id=int(id))
                customer.is_active = False
                customer.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
def customer(request, id):
    '''
    TO get data [GET] to the url : /apiv1/sales/customers/<customer id>
    To edit [POST] 
    Format : 
    {
        'action':'edit',
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
    response_json = {'status':'', 'customers':[]}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "edit":
                customer = Customer.objects.get(id=int(data_json['id']))
                customer.first_name = str(data_json['first_name'])
                customer.last_name = str(data_json['last_name'])
                customer.middle_name = str(data_json['middle_name'])
                customer.email = str(data_json['email'])
                customer.website = str(data_json['website'])
                customer.tax_number = str(data_json['tax_number'])
                customer.phone1 = str(data_json['phone1'])
                customer.phone2 = str(data_json['phone2'])
                customer.address = str(data_json['address'])
                customer.is_active = (data_json['is_active'])
                customer.added_by = CustomUserBase.objects.get(id=int(data_json['added_by']))
                customer.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    try:
        customer = customer.objects.get(id=int(id))
        response_json['customers'] = customers_to_json([customer])
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, ObjectDoesNotExist) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

######################################## InvoieItems ########################################
@login_required
def invoice_items(request):
    '''
    function to add purchase item 
    {
        'action':'add',
        'item': 1,
        'purchase_item':5,
        'sold_from':2,
        'invoice':3,
        'quantity':3,
        'price':34234,
        'tax_total':55,
        'discount_type':'fixed',
        'discount':1351,
        'sub_total':54,
        'total':234
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if request.method == "add":
                invoice_item = InvoiceItem.objects.create(
                    item = Item.objects.get(id=int(data_json['item'])),
                    purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item'])),
                    sold_from = Place.objects.get(id=int(data_json['sold_from'])),
                    invoice = Invoice.objects.get(id=int(data_json['invoice'])),

                    quantity = int(data_json['quantity']),
                    price = data_json['price'],
                    discount_type = data_json['discount_type'],
                    discount = data_json['discount'],
                    tax_total = data_json['tax_total'],
                    sub_total = data_json['sub_total'],
                    total = data_json['total']
                    )                
                invoice_item.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
def invoice_item(request, id):
    '''
    function to edit purchase item 
    {
        'action':'edit',
        'item': 1,
        'purchase_item':5,
        'sold_from':2,
        'invoice':3,
        'quantity':3,
        'price':34234,
        'tax_total':55,
        'discount_type':'fixed',
        'discount':1351,
        'sub_total':54,
        'total':234
    }
    delete
    {
        action:delete,
        'id':3
    }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "edit":
                invoice_item = InvoiceItem.objects.get(id=id)
                invoice_item.item = Item.objects.get(id=int(data_json['item'])),
                invoice_item.purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item'])),
                invoice_item.sold_from = Place.objects.get(id=int(data_json['sold_from'])),
                invoice_item.invoice = Invoice.objects.get(id=int(data_json['invoice'])),

                invoice_item.quantity = int(data_json['quantity']),
                invoice_item.price = data_json['price'],
                invoice_item.discount_type = data_json['discount_type'],
                invoice_item.discount = data_json['discount'],
                invoice_item.tax_total = data_json['tax_total'],
                invoice_item.sub_total = data_json['sub_total'],
                invoice_item.total = data_json['total']           
                invoice_item.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
            
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
def delete_invoice_items(request):
    '''
        {
            "invoice_items_id":[
                1,2
            ]
        }
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['invoice_items_id']
            for id in ids:
                invoice_item = InvoiceItem.objects.get(id=int(id))
                invoice_item.is_active = False
                invoice_item.save()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})