from .models import Invoice, InvoiceItem 
from user_handler.models import Customer, CustomUserBase, Setting
from .serializers import InvoiceSerializer, InvoiceItemSerializer, CustomerSerializer, TaxSerializer, DiscountSerializer, CustomerCategorySerializer
from inventory.models import PurchaseItem, Place, Item
from inventory.utils import weight_conversion
from user_handler.models import ActivityLog
from bikram import samwat
from user_handler.serializers import CountrySerializer

def get_fiscal_year(date):
    start_fisal_year = 0
    end_fiscal_year = 0
    settings = Setting.objects.filter(is_active=True)[0]
    nepali_date = samwat.from_ad(date.date())
    if date.month != settings.change_fisal_year.month:
        if date.month < settings.change_fisal_year.month:
            start_fisal_year = int(date.year) - 1
            end_fiscal_year = int(date.year)
            nepali_start = int(nepali_date.year) - 1 
            nepali_end =  int(nepali_date.year)
        else:
            start_fisal_year = int(date.year)
            end_fiscal_year = int(date.year) + 1
            nepali_start = int(nepali_date.year) 
            nepali_end =  int(nepali_date.year) + 1
    elif date.day != settings.change_fisal_year.month:
        if date.day < settings.change_fisal_year.day:
            start_fisal_year = int(date.year) - 1
            end_fiscal_year = int(date.year)
            nepali_start = int(nepali_date.year) - 1
            nepali_end =  int(nepali_date.year)
        else:
            start_fisal_year = int(date.year)
            end_fiscal_year = int(date.year) + 1
            nepali_start = int(nepali_date.year) 
            nepali_end =  int(nepali_date.year) + 1
    else:
        start_fisal_year = int(date.year)
        end_fiscal_year = int(date.year) + 1
        nepali_start = int(nepali_date.year) 
        nepali_end =  int(nepali_date.year) + 1
    dates = {
        'bs' : str(nepali_start)[2:]+"/"+str(nepali_end)[2:],
        'ad' : str(start_fisal_year)[2:]+"/"+str(end_fiscal_year)[2:],
        'ird_fy' : str(nepali_start)+'.'+str(nepali_end)[1:]
    }
    return dates


def invoices_to_json(models):
    data = []
    for model in models:
        temp = (InvoiceSerializer(model).data)
        temp['customer_name'] = str(Customer.objects.get(id=temp['customer']))
        temp['added_by_name'] = str(CustomUserBase.objects.get(id=temp['added_by']))
        temp['status_name'] = str(model.status.name)
        x = ActivityLog.objects.filter(object_id = model.id, model = 'sales/invoice')
        temp['count_revision'] =  len(x)
        if temp['total_weight']:
            unit = Setting.objects.filter(is_active=True)[0].default_weight_unit
            temp['weight_unit'] = unit
            temp['total_weight'] = weight_conversion(temp['total_weight'], unit)
        temp['fiscal_year'] = get_fiscal_year(model.invoiced_on)
        data.append(temp)
    return data

def invoice_items_to_json(items):
    data = []
    for item in items:
        temp = InvoiceItemSerializer(item).data
        temp['item_name'] = str(Item.objects.get(id=temp['item']))
        temp['sold_from_name'] = str(Place.objects.get(id=temp['sold_from']))
        temp['applied_tax'] = []
        temp['applied_discount'] = []
        for tax in item.taxes.all().filter(is_active=True):
            temp['applied_tax'].append(TaxSerializer(tax).data)
        for discount in item.discount.all().filter(is_active=True):
            temp['applied_discount'].append(DiscountSerializer(discount).data)
        data.append(temp)
    return data
    
def discounts_to_json(discounts):
    data = []
    for discount in discounts:
        print(discount)
        temp = DiscountSerializer(discount).data
        data.append(temp)
    return data

def taxes_to_json(taxes):
    data = []
    for tax in taxes:
        temp = TaxSerializer(tax).data
        data.append(temp)
    return data


def customers_to_json(customers):
    data = []
    for customer in customers:
        temp = CustomerSerializer(customer).data
        temp['country_detail'] = CountrySerializer(customer.country).data
        if(temp['middle_name']):
            temp['name'] = str(temp['first_name']) + " " + str(temp['middle_name'] ) + " "+ str(temp['last_name'])
        else:
            temp['name'] = str(temp['first_name']) + " "+str(temp['last_name'])
        temp['category_str'] = str(customer.category)
        data.append(temp)
    return data

def categories_to_json(categories):
    data = []
    for category in categories:
        temp = CustomerCategorySerializer(category).data
        data.append(temp)
    return data

