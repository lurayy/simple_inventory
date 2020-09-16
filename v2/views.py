from django.shortcuts import render
from sales.models import Invoice, InvoiceItem, InvoiceStatus, SalesSetting
from user_handler.models import Customer, Discount, Tax, Setting
from payment.models import PaymentMethod, Payment, Settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from user_handler.permission_check import bind, check_permission
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from inventory.utils import str_to_datetime
from user_handler.views import log
from inventory.models import Item, PurchaseItem, PurchaseOrder, Place, Placement
from django.conf import settings

@require_http_methods(['POST'])
@bind
def create_invoice_all(self, request):
    jwt_check = check_permission(self.__name__, request.headers['Authorization'].split(' ')[1])
    if jwt_check:
        if not jwt_check['status']:
            return JsonResponse(jwt_check)            
        try:
            invoice = False
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            data = {'token':request.headers['Authorization'].split(' ')[1]}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            response_json = {'status':False}
            if data_json['action'] == "create":
                invoice = create_invoice(data_json['invoice'], user)
                create_invoice_items(data_json['invoice_items'], invoice, user)
                do_payment(invoice)
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            if invoice:
                invoice.delete()
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})

def create_invoice(data_json, user):
    s = SalesSetting.objects.filter(is_active=True)[0]
    invoice = Invoice.objects.create(
        added_by = user,
        customer = s.default_customer_qk_sales,
        invoiced_on = str_to_datetime(data_json['invoiced_on']),
        due_on = str_to_datetime(data_json['due_on']),
        status = InvoiceStatus.objects.get(id = data_json['status']),
        total_amount = 0,
        bill_amount=0,
        weight_unit = data_json['weight_unit'],
        total_weight = data_json['total_weight'],
        additional_discount= data_json['additional_discount']
    )
    invoice.save()
    log('sales/invoice', 'create', invoice.id, str(invoice), {}, user)
    return invoice

def create_invoice_items(invoice_items, invoice, user):
    old_status = invoice.status
    invoice.status = InvoiceStatus.objects.filter(is_sold=False)[0]
    invoice.save()
    for invoice_item_json in invoice_items:
            invoice_item = InvoiceItem.objects.create(
                item = Item.objects.get(id=int(invoice_item_json['item'])),
                purchase_item = PurchaseItem.objects.get(id=int(invoice_item_json['purchase_item'])),
                sold_from = Place.objects.get(id=int(invoice_item_json['sold_from'])),
                invoice = invoice,
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
            log('sales/invoice_item', 'create', invoice_item.id, str(invoice_item), {'invoice': invoice.id}, user)
    invoice.status = old_status
    invoice.save()

def do_payment(invoice):
    s = Setting.objects.filter(is_active=True)[0]
    s2 = Settings.objects.filter(is_active=True)[0]
    temp = Payment.objects.create(
            invoice = invoice,
            amount=invoice.bill_amount,
            method= s2.default_payment_method_qk_sales,
            transaction_from = '',
            transaction_id = '',
            bank_name = '',
            remarks = '',
        )
    temp.save()  
    if "accounting" in settings.INSTALLED_APPS:
        from accounting.models import AccountingSettings, payemnt_entry_to_system
        s3 = AccountingSettings.objects.filter(is_active=True)[0]
        payemnt_entry_to_system(s3.default_account_qk_sales, temp)
    temp.invoice.save()
    
    