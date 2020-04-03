from .models import Invoice, InvoiceItem, InvoiceStatus
from inventory.models import Place, Placement, Item, PurchaseItem
from inventory.utils import str_to_datetime 
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import json
from .utils import invoices_to_json, invoice_items_to_json, discounts_to_json, taxes_to_json, customers_to_json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from user_handler.models import Tax, Discount
from user_handler.models import Customer, CustomUserBase, Tax, Discount
from .serializers import InvoiceStatusSerializer
@login_required
@require_http_methods(['POST'])
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
                    invoices = Invoice.objects.filter(is_active=True, status=str(data_json['status']).lower()).order_by('-invoiced_on')[start:end]            
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
            if str(data_json['action'] == "add"):
                invoice = Invoice.objects.create(
                    paid_amount = data_json['paid_amount'],
                    added_by = CustomUserBase.objects.get(id=int(data_json["added_by"])),
                    customer = Customer.objects.get(id=int(data_json['customer'])),
                    invoiced_on = str_to_datetime(data_json['invoiced_on']),
                    due_on = str_to_datetime(data_json['due_on']),
                    status =InvoiceStatus.objects.get(id=data_json['status'])          
                )
                invoice.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
@require_http_methods(['POST'])
#edit invoice order 
def invoice(request):
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
            response_json = {'status':'', 'invoice':{}, 'invoice_items':[]}
            if data_json['action'] == "edit":
                new_status = InvoiceStatus.objects.get(id=data_json['status']) 
                invoice = Invoice.objects.get(id=int(data_json['invoice_id']))
                
                if (new_status == invoice.status and invoice.status.is_sold ==True):
                    raise Exception("Cannot Edit Invoice Or Invoice Item if it's already sold.")
                elif (new_status != invoice.status):
                    invoice.status = new_status
                    invoice.save()
                invoice.customer = Customer.objects.get(id=int(data_json['customer']))
                invoice.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                invoice.due_on = str_to_datetime(data_json['due_on'])
                invoice.status = InvoiceStatus.objects.get(id=data_json['status'])  
                invoice.additional_discount = float(data_json['additional_discount'])
                invoice.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == 'get':
                invoice = Invoice.objects.get(id=int(data_json['invoice_id']))
                response_json['invoice'] = invoices_to_json([invoice])
                response_json['invoice_items'] = invoice_items_to_json(InvoiceItem.objects.filter(invoice=invoice))
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
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
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
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
                )
                customer.save()
                response_json['customers'] = customers_to_json([customer])
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                if data_json['filter'] == "name":
                    customers = Customer.objects.filter(is_active=True, first_name__contains=data_json['name']).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['customers'] = customers_to_json(customers)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                else:
                    customers = Customer.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['customers'] = customers_to_json(customers)
                    response_json['status'] = True
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
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
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def customer(request):
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
                customer.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                customer = Customer.objects.get(id=int(data_json['customer_id']))
                response_json['customers'] = customers_to_json([customer])
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


######################################## InvoieItems ########################################
@login_required
@require_http_methods(['POST'])
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
            if data_json['action'] == "add":
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
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def invoice_item(request):
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
    '''
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {}
            if data_json['action'] == "edit":
                
                invoice_item = InvoiceItem.objects.get(id=data_json["invoice_item_id"])
                if(invoice_item.invoice.status.is_sold):
                    raise Exception("Cannot edit item's that are already sold.")
                invoice_item.item = Item.objects.get(id=int(data_json['item']))
                invoice_item.purchase_item = PurchaseItem.objects.get(id=int(data_json['purchase_item']))
                invoice_item.sold_from = Place.objects.get(id=int(data_json['sold_from']))
                invoice_item.invoice = Invoice.objects.get(id=int(data_json['invoice']))
                invoice_item.quantity = int(data_json['quantity'])
                invoice_item.price = float(data_json['price'])
                invoice_item.discount.clear()
                for dis_id in data_json['discount']:
                    dis = Discount.objects.get(id=int(dis_id))
                    invoice_item.discount.add(dis)
                invoice_item.taxes.clear()
                for tax_id in data_json['taxes']:
                    tax = Tax.objects.get(id=int(tax_id))
                    invoice_item.taxes.add(tax)
                invoice_item.save()
                invoice_item.save()
                invoice_item.invoice.save()
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                invoice_item = InvoiceItem.objects.get(id=data_json['invoice_item_id'])
                response_json['invoice_items'] = invoice_items_to_json([invoice_item])
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
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
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})




@login_required
@require_http_methods(['POST'])
def discounts(request):
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                discount = Discount.objects.create(
                    name = data_json['name'],
                    code = data_json['code'],
                    discount_type = data_json['discount_type'],
                    rate = data_json['rate']
                )
                discount.save()
                response_json['discounts'] = discounts_to_json([discount])
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    discounts = Discount.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['discounts'] = discounts_to_json(discounts)
                    response_json['status'] = True
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def discount(request):
    response_json =  {}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                discounts = Discount.objects.filter(is_active=True, id = data_json['discount_id'])
                response_json['discounts'] = discounts_to_json(discounts)
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == "edit":
                discount = Discount.objects.get(is_active=True, id = data_json['discount_id'])
                discount.name = data_json['name']
                discount.code = data_json['code']
                discount.discount_type = data_json['discount_type']
                discount.rate = data_json['rate']
                discount.is_active = data_json['is_active']
                discount.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def delete_discount(request):
    response_json = {}
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        ids = data_json['discounts_id']
        for id in ids:
            discount = Discount.objects.get(id=int(id))
            discount.is_active = False
            discount.save()
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def taxes(request):
    response_json = {'status':''}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                tax = Tax.objects.create(
                    name = data_json['name'],
                    code = data_json['code'],
                    tax_type = data_json['tax_type'],
                    rate = data_json['rate']
                )
                tax.save()
                response_json['taxes'] = taxes_to_json([tax])
                response_json = {'status':True}
                return JsonResponse(response_json)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    taxes = Tax.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['taxes'] = taxes_to_json(taxes)
                    response_json['status'] = True
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
@require_http_methods(['POST'])
def tax(request):
    response_json =  {}
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                taxes = Tax.objects.get(is_active=True, id = data_json['tax_id'])
                response_json['taxes'] = taxes_to_json([taxes])
                response_json['status'] = True
                return JsonResponse(response_json)
            if data_json['action'] == "edit":
                tax = Tax.objects.get(is_active=True, id = data_json['tax_id'])
                tax.name = data_json['name']
                tax.code = data_json['code']
                tax.tax_type = data_json['tax_type']
                tax.rate = data_json['rate']
                tax.is_active = data_json['is_active']
                tax.save()
                response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@login_required
@require_http_methods(['POST'])
def delete_taxes(request):
    response_json = {}
    try:
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        ids = data_json['taxes_id']
        for id in ids:
            tax = Tax.objects.get(id=int(id))
            tax.is_active = False
            tax.save()
        response_json['status'] = True
        return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})



@login_required
@require_http_methods(['POST'])
def invoice_status(request):
    if request.method == "POST":
        statuss = InvoiceStatus.objects.all()
        data = []
        for status in statuss:
            temp =  InvoiceStatusSerializer(status).data
            data.append(temp)
        return JsonResponse({'status':True, 'data':data})

