from .models import Invoice, InvoiceItem, InvoiceStatus
from inventory.models import Place, Placement, Item, PurchaseItem
from inventory.utils import str_to_datetime 
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import json
from .utils import invoices_to_json, invoice_items_to_json, discounts_to_json, taxes_to_json, customers_to_json, categories_to_json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from user_handler.models import Tax, Discount
from user_handler.models import Customer, CustomUserBase, Tax, Discount, CustomerCategory
from .serializers import InvoiceStatusSerializer
from user_handler.permission_check import bind, check_permission

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


@require_http_methods(['POST'])
@bind
def get_multiple_invoices(self, request):
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            # GET Handler
            if str(data_json['action']) == "get":
                start = int(data_json["start"])
                end = int(data_json["end"])
                response_json = {'status':False, 'sales':[]}
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
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_invoice(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if str(data_json['action'] == "add"):
                stat = InvoiceStatus.objects.filter(is_active=True, is_sold=False)
                if (len(stat) == 0):
                    raise Exception("Create a invoice status first. Contact Admin.")
                valid_data = VerifyJSONWebTokenSerializer().validate({'token':request.headers['Authorization'].split(' ')[1]})
                user = valid_data['user']
                invoice = Invoice.objects.create(
                    added_by = user,
                    customer = Customer.objects.get(id=int(data_json['customer'])),
                    invoiced_on = str_to_datetime(data_json['invoiced_on']),
                    due_on = str_to_datetime(data_json['due_on']),
                    status = stat[0],
                    total_amount = 0,
                    bill_amount=0,
                    total_weight = data_json['total_weight'],
                    additional_discount= data_json['additional_discount']
                )
                invoice.save()
                response_json['status'] = True
                response_json['invoice'] = invoices_to_json([invoice])
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
#update invoice order 
def update_invoice(self, request):
    ''' To get data about single purchase order
    To get info about a single invoice, trigger /apiv1/inventory/porders/<invoice_id>/
    To update the data, you can POST on the same link: 
    POST format:
    {
        'action':'update',
        'id':1,
        'invoiced_on': "2019-11-16T08:15:00.000",
        'completed_on: "2019-11-16T08:15:00.000",
        'bill_amount': 2500,
        'added_by':1,                <- added_by id
        'customer':1,                  <- customer id 
        'status':'paid',

    }
    '''
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            response_json = {'status':False, 'invoice':{}, 'invoice_items':[]}
            if data_json['action'] == "update":
                new_status = InvoiceStatus.objects.get(id=data_json['status']) 
                invoice = Invoice.objects.get(id=int(data_json['invoice_id']))
                if (new_status == invoice.status and invoice.status.is_sold ==True):
                    raise Exception("Cannot update Invoice Or Invoice Item if it's already sold.")
                elif (new_status != invoice.status):
                    invoice.status = new_status
                    invoice.save()
                invoice.customer = Customer.objects.get(id=int(data_json['customer']))
                invoice.invoiced_on = str_to_datetime(data_json['invoiced_on'])
                invoice.due_on = str_to_datetime(data_json['due_on'])
                invoice.status = InvoiceStatus.objects.get(id=data_json['status'])  
                invoice.additional_discount = float(data_json['additional_discount'])
                invoice.total_weight = data_json['total_weight']
                invoice.save()
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_invoice_details(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == 'get':
                invoice = Invoice.objects.get(id=int(data_json['invoice_id']))
                response_json['invoice'] = invoices_to_json([invoice])
                response_json['invoice_items'] = invoice_items_to_json(InvoiceItem.objects.filter(invoice=invoice))
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_invoices(self, request):
    '''
    {
        "invoices_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

######################################## Customer  ########################################


@require_http_methods(['POST'])
@bind
def get_multiple_customers(self, request):
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
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == "name":
                    customers = Customer.objects.filter(is_active=True, first_name__icontains=str(data_json['name']).lower() ).order_by('id')[int(data_json['start']):int(data_json['end'])]
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_customer(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        response_json = {'status':False}
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
                    category = CustomerCategory.objects.get(id=data_json['category'])
                )
                customer.save()
                response_json['customers'] = customers_to_json([customer])
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})  
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_customers(self, request):
    '''
    {
        "customers_id":[
            1,2
        ]
    }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def update_customer(self, request):
    '''
    TO get data [GET] to the url : /apiv1/sales/customers/<customer id>
    To update [POST] 
    Format : 
    {
        'action':'update',
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
    response_json = {'status':False, 'customers':[]}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
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
                customer.category = CustomerCategory.objects.get(id=data_json['category'])
                customer.save()
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_customer_details(self, request):
    response_json = {'status':False, 'customers':[]}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                customer = Customer.objects.get(id=int(data_json['customer_id']))
                response_json['customers'] = customers_to_json([customer])
                response_json['status'] = True
            return JsonResponse(response_json)        
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_customer_categories(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try: 
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                response_json = {
                    'status':True,
                    'customerCategories': categories_to_json(CustomerCategory.objects.filter(is_active=True))
                }
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
                return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_customer_categories(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try: 
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                category = CustomerCategory.objects.get(id=data_json['customer_category_id'])
                category.name = data_json['name']
                category.is_active = data_json['is_active']
                response_json['status'] = True
                category.save()
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
                return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_customer_category(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try: 
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                category = CustomerCategory.objects.get(id=data_json['customer_category_id'])
                response_json = {
                    'status':True,
                    'customerCategories': categories_to_json([category])
                }
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
                return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def add_customer_categories(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try: 
            response_json['status'] = True
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "add":
                category = CustomerCategory.objects.create(name=data_json['name'])
                category.save()
                response_json['category'] = categories_to_json([category])
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
                return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_customer_categories(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "delete":
                ids = data_json['customer_category_ids']
                if ids is None:
                    raise Exception('Empty List')
                for id in ids:
                    customer = CustomerCategory.objects.get(id=int(id))
                    customer.is_active = False
                    customer.save()
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



######################################## InvoieItems ########################################

@require_http_methods(['POST'])
@bind
def add_new_invoice_item(self, request):
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
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
                    price = float(data_json['price']),
                    )
                invoice_item.save()
                for dis_id in data_json['discounts']:
                    dis = Discount.objects.get(id=int(dis_id))
                    invoice_item.discount.add(dis)
                for tax_id in data_json['taxes']:
                    tax = Tax.objects.get(id=int(tax_id))
                    invoice_item.taxes.add(tax)
                invoice_item.save()
                invoice_item.invoice.save()
                invoice_item.invoice.save()
                response_json = {'status':True}
            if data_json['action'] == "add_multiple":
                for invoice_item_json in data_json['invoice_items']:
                    try:
                        invoice_item = InvoiceItem.objects.create(
                            item = Item.objects.get(id=int(invoice_item_json['item'])),
                            purchase_item = PurchaseItem.objects.get(id=int(invoice_item_json['purchase_item'])),
                            sold_from = Place.objects.get(id=int(invoice_item_json['sold_from'])),
                            invoice = Invoice.objects.get(id=int(invoice_item_json['invoice'])),
                            quantity = invoice_item_json['quantity'],
                            price = invoice_item_json['price'],
                            )
                        invoice_item.save()
                        for dis_id in invoice_item_json['discounts']:
                            dis = Discount.objects.get(id=int(dis_id))
                            invoice_item.discount.add(dis)
                        for tax_id in invoice_item_json['taxes']:
                            tax = Tax.objects.get(id=int(tax_id))
                            invoice_item.taxes.add(tax)
                        invoice_item.save()
                        invoice_item.invoice.save()
                        invoice_item.invoice.save()
                    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
                        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                response_json = {'status':True}
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def update_invoice_item(self, request):
    '''
    function to update purchase item 
    {
        'action':'update',
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
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
                invoice_item = InvoiceItem.objects.get(id=data_json["invoice_item_id"])
                if(invoice_item.invoice.status.is_sold):
                    raise Exception("Cannot update item's that are already sold.")
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
            if data_json['action'] == "update_multiple":
                for invoice_item_json in data_json['invoice_items']:
                    invoice_item = InvoiceItem.objects.get(id=invoice_item_json["invoice_item_id"])
                    if(invoice_item.invoice.status.is_sold):
                        raise Exception("Cannot update item's that are already sold.")
                    invoice_item.item = Item.objects.get(id=int(invoice_item_json['item']))
                    invoice_item.purchase_item = PurchaseItem.objects.get(id=int(invoice_item_json['purchase_item']))
                    invoice_item.sold_from = Place.objects.get(id=int(invoice_item_json['sold_from']))
                    invoice_item.invoice = Invoice.objects.get(id=int(invoice_item_json['invoice']))
                    invoice_item.quantity = int(invoice_item_json['quantity'])
                    invoice_item.price = float(invoice_item_json['price'])
                    invoice_item.discount.clear()
                    for dis_id in invoice_item_json['discounts']:
                        dis = Discount.objects.get(id=int(dis_id))
                        invoice_item.discount.add(dis)
                    invoice_item.taxes.clear()
                    for tax_id in invoice_item_json['taxes']:
                        tax = Tax.objects.get(id=int(tax_id))
                        invoice_item.taxes.add(tax)
                    invoice_item.save()
                    invoice_item.save()
                    invoice_item.invoice.save()
                    response_json = {'status':True}
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

@require_http_methods(['POST'])
@bind
def get_invoice_item_details(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)        
            if data_json['action'] == "get":
                invoice_item = InvoiceItem.objects.get(id=data_json['invoice_item_id'])
                response_json['invoice_items'] = invoice_items_to_json([invoice_item])
                response_json['status'] = True
            return JsonResponse(response_json)            
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
        
@require_http_methods(['POST'])
@bind
def delete_invoice_items(self, request):
    '''
        {
            "invoice_items_id":[
                1,2
            ]
        }
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            ids = data_json['invoice_items_id']
            for id in ids:
                invoice_item = InvoiceItem.objects.get(id=int(id))
                if (invoice_item.invoice.status.is_sold == True):
                    raise Exception("Cannot Delete items if the invoice's items are already sold.")
                invoice_item.delete()
            response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_multiple_discounts(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    discounts = Discount.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['discounts'] = discounts_to_json(discounts)
                    response_json['status'] = True
                    return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_discount(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def update_discount(self, request):
    response_json =  {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
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


@require_http_methods(['POST'])
@bind
def get_discount_details(self, request):
    response_json =  {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)        
            if data_json['action'] == "get":
                discounts = Discount.objects.filter(is_active=True, id = data_json['discount_id'])
                response_json['discounts'] = discounts_to_json(discounts)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

            

@require_http_methods(['POST'])
@bind
def delete_discount(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def add_new_tax(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
        except (KeyError, json.decoder.JSONDecodeError, IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@require_http_methods(['POST'])
@bind
def get_multiple_taxes(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                if data_json['filter'] == 'none':
                    taxes = Tax.objects.filter(is_active=True).order_by('id')[int(data_json['start']):int(data_json['end'])]
                    response_json['taxes'] = taxes_to_json(taxes)
                    response_json['status'] = True
                return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

@require_http_methods(['POST'])
@bind
def update_tax(self, request):
    response_json =  {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "update":
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def get_tax_details(self, request):
    response_json =  {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] == "get":
                taxes = Tax.objects.get(is_active=True, id = data_json['tax_id'])
                response_json['taxes'] = taxes_to_json([taxes])
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,   Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def delete_taxes(self, request):
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
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
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})



@require_http_methods(['POST'])
@bind
def get_invoice_status(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):    
        statuss = InvoiceStatus.objects.all()
        data = []
        for status in statuss:
            temp =  InvoiceStatusSerializer(status).data
            data.append(temp)
        return JsonResponse({'status':True, 'data':data})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})


@require_http_methods(['POST'])
@bind
def export_sales_data(self, request):
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        return JsonResponse({'status':True}) 
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
    'invoices':data,
    'headers':fields
    }
    html = template.render(data)
    pdf = render_to_pdf('export_items_data', data)
    return pdf