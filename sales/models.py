from django.db import models
from inventory.models import PurchaseItem, Place, Item, Placement
from user_handler.models import Customer, CustomUserBase, Tax, Discount
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import signals
import uuid
from django.conf import settings
from django.template.loader import get_template 
from django.core.files.base import ContentFile
import xhtml2pdf.pisa as pisa
from django.template import Context
import cgi
import datetime
from io import BytesIO
from django.http import HttpResponse
import django.dispatch
from user_handler.models import Setting


class InvoiceStatus(models.Model):
    name = models.CharField(max_length=255)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

class Invoice(models.Model):
    ''' schema for invoice'''
    added_by = models.ForeignKey(
        CustomUserBase, on_delete=models.PROTECT, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True)
    invoiced_on = models.DateTimeField(default=0)
    due_on = models.DateTimeField()
    invoice_number = models.CharField(max_length=255)

    total_amount = models.FloatField(default=0)
    bill_amount = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)
    total_weight = models.FloatField(default=0)
    weight_unit = models.CharField(max_length=25, default='kg')
    tax_total = models.PositiveIntegerField(default=0)
    discount_total = models.PositiveIntegerField(default=0)
    additional_discount = models.PositiveIntegerField(default=0)    
    is_sent = models.BooleanField(default=False)

    serial = models.PositiveIntegerField(default=0)
    fiscal_year_ad = models.CharField(default='', max_length=6, null=True, blank=True)
    fiscal_year_bs = models.CharField(default='', max_length=6, null=True, blank=True)

    status = models.ForeignKey(
        InvoiceStatus, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # new fields
    is_synced_with_ird = models.BooleanField(default=False)
    is_bill_printed = models.BooleanField(default=False)
    printed_timestamp = models.DateTimeField(null=True, blank=True)
    printed_by = models.ForeignKey(CustomUserBase, on_delete=models.PROTECT, null=True, blank=True, related_name='printed_invoices')
    is_realtime = models.BooleanField(default=True)

    bill_print_count = models.PositiveIntegerField(default = 0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_canceled = models.BooleanField(default=False)
    cancelation_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.customer} {self.invoice_number}'

    def save(self, *args, **kwargs):
        self.total_amount = round(self.total_amount, 2)
        self.bill_amount = round(self.bill_amount, 2)
        self.paid_amount = 0
        from payment.models import Payment
        if self.id:
            payments_list = Payment.objects.all().filter(invoice=self.id)
            for pay in payments_list:
                if pay.method.header != "credit" and pay.is_paid_credit == False:
                    self.paid_amount = self.paid_amount + pay.amount
        super(Invoice, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ('invoice_number',)


def update_ird_bill(invoice):
    settings = Setting.objects.filter(is_active=True)[0]
    url = "http://103.1.92.174:9050/api/billreturn"
    from bikram import samwat
    from .utils import get_fiscal_year
    import requests
    import json
    y =  samwat.from_ad(invoice.updated_at.date())
    nepali_invoiced_on = samwat.from_ad(invoice.invoiced_on.date())
    x = datetime.datetime.now()
    str_datetime = str(x.month).zfill(2) + '.' + str(x.day).zfill(2)+ '.' + str(x.year) +' ' + str(x.hour).zfill(2) + ':' + str(x.minute).zfill(2) + ':' + str(x.second).zfill(2)
    x = str(nepali_invoiced_on.year)+'.'+str(nepali_invoiced_on.month).zfill(2)+'.'+str(nepali_invoiced_on.day)
    data = {

        'username' : "Test_CBMS", 
        'password' : "test@321", 
        'seller_pan' : "999999999",
        'buyer_pan' : "123456789",
        'buyer_name':"", 
        'fiscal_year' : str(get_fiscal_year(invoice.invoiced_on)['ird_fy']), 
        'invoice_number': str(invoice.invoice_number),
        'invoice_date':str(x),
        'ref_invoice_number' : invoice.invoice_number,
        'credit_note_number' : invoice.invoice_number,
        'credit_note_date' : str(str(y.year)+'.'+str(y.month)+'.'+str(y.day)),
        'reason_for_return' : str(invoice.cancelation_reason),
        'total_sales':invoice.bill_amount,
        'taxable_sales_vat':invoice.total_amount - invoice.discount_total, 
        'vat':invoice.tax_total, 
        'excisable_amount':0, 
        'excise':0,
        'taxable_sales_hst':0,
        'hst':0, 
        'amount_for_esf':0, 
        'esf':0, 
        'export_sales':0,
        'tax_exempted_sales':0,
        'isrealtime':True, 
        'datetimeclient' : str(str_datetime)
    }
    header = {
        'Content-Type' : 'application/json'
    }
    res = requests.post(url,headers = header,  data= json.dumps(data))
    if str(res.json()) == "200":
        response = {
            'msg' :"Bill synced with IRD server."
        }
    elif str(res.json()) == "101":
        response = {
            'msg' :"Bill already synced with the server."
        }
    elif str(res.json()) == "100":
        response = {
            'msg' :"IRD server login username and password doesnot match."
        }
    else:
        response = {
            'msg' : 'Error while syncing with the IRD server, check your internet connection or try contacting the admins.'
        }
    
    invoice.is_synced_with_ird = True
    invoice.save()
    return response

    

def sync_with_ird(invoice):
    print('sync start')
    settings = Setting.objects.filter(is_active=True)[0]
    url = "http://103.1.92.174:9050/api/bill"
    from bikram import samwat
    from .utils import get_fiscal_year
    import requests
    import json
    nepali_invoiced_on = samwat.from_ad(invoice.invoiced_on.date())
    x = datetime.datetime.now()
    str_datetime = str(x.month).zfill(2) + '.' + str(x.day).zfill(2)+ '.' + str(x.year) +' ' + str(x.hour).zfill(2) + ':' + str(x.minute).zfill(2) + ':' + str(x.second).zfill(2)
    x = str(nepali_invoiced_on.year)+'.'+str(nepali_invoiced_on.month).zfill(2)+'.'+str(nepali_invoiced_on.day)
    data  = {
        'username' : "Test_CBMS", 
        'password' : "test@321", 
        'seller_pan' : "999999999",
        'buyer_pan' : "123456789",
        'buyer_name':"", 
        'fiscal_year' : str(get_fiscal_year(invoice.invoiced_on)['ird_fy']), 
        'invoice_number': str(invoice.invoice_number),
        'invoice_date':str(x),
        'total_sales':invoice.bill_amount,
        'taxable_sales_vat':invoice.total_amount - invoice.discount_total, 
        'vat':invoice.tax_total, 
        'excisable_amount':0, 
        'excise':0,
        'taxable_sales_hst':0,
        'hst':0, 
        'amount_for_esf':0, 
        'esf':0, 
        'export_sales':0,
        'tax_exempted_sales':0,
        'isrealtime':True, 
        'datetimeclient' : str(str_datetime)
    }
    header = {
        'Content-Type' : 'application/json'
    }
    res = requests.post(url,headers = header,  data = json.dumps(data))
    if str(res.json()) == "200":
        response = {
            'msg' :"Bill synced with IRD server."
        }
    elif str(res.json()) == "101":
        response = {
            'msg' :"Bill already synced with the server."
        }
    elif str(res.json()) == "100":
        response = {
            'msg' :"IRD server login username and password doesnot match."
        }
    else:
        response = {
            'msg' : 'Error while syncing with the IRD server, check your internet connection or try contacting the admins.'
        }
    invoice.is_synced_with_ird = True
    invoice.save()
    return response


def generate_invoice_number(invoice):
    try:
        from .utils import get_fiscal_year
        setting = Setting.objects.filter(is_active=True)[0]
        years = get_fiscal_year(invoice.invoiced_on)
        latest = Invoice.objects.filter(fiscal_year_ad = years['ad']).order_by('-serial')
        print(latest)
        if len(latest) != 0:
            serial = latest[0].serial
            serial = serial + 1
        else:
            serial = 0
        invoice_number = setting.branch_code + str(serial).zfill(6) + " " + years['bs']
        print(invoice_number)
        return ([invoice_number, years, str(serial).zfill(6)])
    except:
        raise Exception("Settings is not setup properly.")



class InvoiceItem(models.Model):
    ''' this model hold the items and the details of that item, that are add to invoice'''
    purchase_item = models.ForeignKey(
        PurchaseItem, on_delete=models.PROTECT, null=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True)
    sold_from = models.ForeignKey(Place, on_delete=models.PROTECT, null=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.PositiveIntegerField(default=1)

    price = models.FloatField()
    
    sub_total = models.FloatField(blank=True, null=True)

    discount_amount = models.FloatField(blank=True, null=True)

    total_without_tax = models.FloatField(blank=True, null=True)

    tax_total = models.FloatField(blank=True, null=True)

    total = models.FloatField(blank=True, null=True)

    discount = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=InvoiceItem)
def post_save_handler(sender, created, instance, **kwargs):
    instance.tax_total = 0
    instance.sub_total = 0
    instance.discount_amount = 0
    instance.total = 0
    applied_taxex = instance.taxes.all().filter(is_active=True)
    applied_discounts = instance.discount.all().filter(is_active=True)
    instance.sub_total = instance.price*instance.quantity

    for discount in applied_discounts:
        if discount.discount_type == 'fixed':
            instance.discount_amount = instance.discount_amount + \
                (discount.rate) * instance.quantity
        else:
            instance.discount_amount = instance.discount_amount + \
                (instance.sub_total*discount.rate)/100
    
    instance.total_without_tax = instance.sub_total - instance.discount_amount
    for tax in applied_taxex:
        if tax.tax_type == 'fixed':
            instance.tax_total = instance.tax_total + \
                (tax.rate) * instance.quantity
        else:
            instance.tax_total = instance.tax_total + \
                (instance.total_without_tax*tax.rate)/100
    instance.total = instance.total_without_tax + instance.tax_total
    signals.post_save.disconnect(post_save_handler, sender=InvoiceItem)
    instance.save()
    signals.post_save.connect(post_save_handler, sender=InvoiceItem)


@receiver(pre_save, sender=Invoice)
def tranction_handler(sender, instance, **kwargs):
    if instance.id is None:
        x = generate_invoice_number(instance)
        instance.invoice_number = x[0]
        instance.fiscal_year_ad = x[1]['ad']
        instance.fiscal_year_bs = x[1]['bs']
        instance.serial = x[2]
        if instance.status.is_sold == True:
            sales_sub(instance)
    else:
        old_status = Invoice.objects.get(id=instance.id).status
        if instance.status != old_status:
            if old_status.is_sold == False:
                if instance.status.is_sold == True:
                    sales_sub(instance)
            if old_status.is_sold == True:
                if instance.status == False:
                    sales_add(instance)
    instance.total_amount = 0
    instance.discount_total = 0
    instance.tax_total = 0
    for invoice_item in instance.invoice_items.all():
        instance.total_amount = instance.total_amount + invoice_item.sub_total
        instance.discount_total = instance.discount_total + invoice_item.discount_amount
        instance.tax_total = instance.tax_total + invoice_item.tax_total
    instance.bill_amount = instance.total_amount - instance.discount_total + instance.tax_total - instance.additional_discount
    if instance.total_weight or instance.weight_unit:
        if instance.weight_unit == "g":
            pass
        elif instance.weight_unit == "kg":
            instance.total_weight = instance.total_weight * 1000
            instance.weight_unit = "g"
        elif instance.weight_unit == "lb":
            instance.total_weight = instance.total_weight * 452
            instance.weight_unit = "g"
        else:
            raise Exception("Accepted weight units g [gram], kg[kilogram] and lb[pound]")



# @receiver(post_save, sender=Invoice)
# def invoice_post_handler(sender, instance, created, **kwargs):
#     if created:
#         print('post')
#         sync_with_ird(instance)
#     send_update_invoice(instance)


def sales_sub(invoice):
    for item in invoice.invoice_items.filter():
        if item.purchase_item.stock < item.quantity:
            raise Exception(
                f'{item.item}\" quantity is greater than it\"s avaible stock.')
        item.purchase_item.stock = item.purchase_item.stock - item.quantity
        item.purchase_item.sold = item.purchase_item.sold + item.quantity
        item.purchase_item.save()
        item.item.stock = item.item.stock - item.quantity
        item.item.sold = item.item.sold + item.quantity
        item.item.save()
        sold_from = Placement.objects.get(
            placed_on=item.sold_from, purchase_item=item.purchase_item)
        sold_from.stock = sold_from.stock - item.quantity
        sold_from.save()
        print(item.item.sold)

def sales_add(invoice):
    for item in invoice.invoice_items.filter():
        item.purchase_item.stock = item.purchase_item.stock + item.quantity
        item.purchase_item.sold = item.purchase_item.sold - item.quantity
        item.purchase_item.save()
        item.item.stock = item.item.stock + item.quantity
        item.item.sold = item.item.sold - item.quantity
        item.item.save()
        place = Place.objects.get(name='unassigned')
        sold_from = Placement.objects.get(
            placed_on=place, purchase_item=item.purchase_item)
        sold_from.stock = sold_from.stock + item.quantity
        sold_from.save()
        item.sold_from = place
        item.save()
        print(item.item.sold)


def send_update_invoice(invoice):
    if invoice.status.is_sold:
        if invoice.customer.email:
            from sales.utils import invoices_to_json, invoice_items_to_json
            from django.core.mail import send_mail
            import weasyprint
            from user_handler.models import Setting
            from payment.models import Payment
            invoice_items = InvoiceItem.objects.filter(invoice = invoice)
            setting = Setting.objects.filter()[0]
            data = {
                'invoice' : invoices_to_json([invoice])[0] ,
                'invoice_items' : invoice_items_to_json(invoice_items),
                'company' : {
                    'name' : setting.company,
                    'address' : setting.company_address,
                    'pan' : setting.pan_number
                }
            } 
            data['invoice']['customer_pan'] = invoice.customer.tax_number
            data['invoice']['customer_address'] = invoice.customer.address

            data['invoice']['invoiced_on'] = invoice.invoiced_on.date()
            data['invoice']['due_on'] = invoice.due_on.date()
            data['invoice']['due_amount'] = invoice.bill_amount - invoice.paid_amount

            data['invoice']['payment_methods'] = ''
            for payment in Payment.objects.filter(refunded = False, is_paid_credit = False, is_active = True ):
                data['invoice']['payment_methods'] = data['invoice']['payment_methods'] + str(payment.method).capitalize() + ", " 
            template = get_template('invoice_bill.html')
            html = template.render({'data':data})

            res = send_mail("Invoice", "Some generic Message", settings.EMAIL_HOST_USER, [invoice.customer.email], html_message=html)
            if not invoice.is_sent:
                if res:
                    invoice.is_sent = True
                    invoice.save()
                else:
                    print("Invoice cannot be sent through email.")


def render_to_pdf(template_src, context_dict={}):
    template = get_template('invoice.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return {'pdf' : HttpResponse(result.getvalue(), content_type='application/pdf'), 'html': html}
    return None


def export_data(data):
    template = get_template('invoice.html')
    data = {
        'today': datetime.date.today(),
        'data': data
    }
    html = template.render(data)
    pdf = render_to_pdf('invoice', data)
    return pdf

class SalesSetting(models.Model):
    default_place_to_sold_from = models.ForeignKey(Place, on_delete=models.PROTECT)
    default_vat_tax = models.ForeignKey(Tax, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
