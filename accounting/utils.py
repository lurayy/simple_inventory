from django.forms.models import model_to_dict 
from .models import  AccountType, Account, LedgerEntry, MonthlyStats
import dateutil.parser
from .serializers import  AccountTypeSerializer, AccountSerializer, LedgerEntrySerializer, MonthlyStatsSerializer, FreeEntrySerializer
from payment.models import Payment, PaymentMethod
from payment.utils import payment_to_json


def accounts_types_to_json (models):
    data = []
    for model in models:
        temp = (AccountTypeSerializer(model).data)
        data.append(temp)
    # choices = {
    #     "header_choices" : AccountType.HEADER_CHOICE
    # }
    # data.append(choices)
    return data

def accounts_to_json(models):
    data = []
    for model in models:
        temp = AccountSerializer(model).data
        temp['account_type_str'] = model.account_type.name
        temp['account_header_str'] = model.account_type.header
        if len( Account.objects.filter(parent = model)) > 0 :
            temp['has_child'] = True
        else:
            temp['has_child'] = False
        if model.parent:
            temp['parent_str'] = model.parent.name
            temp['parent_uuid'] = model.parent.uuid
        data.append(temp)
    return data

def ledger_entries_to_json(models):
    data = []
    for model in models:
        temp = LedgerEntrySerializer(model).data
        temp['account_str'] = model.account.name
        temp['account_type_str'] = model.account.account_type.name
        temp['header_str'] = model.entry_type.header
        temp['payment'] = payment_to_json([model.payment])
        data.append(temp)
    return data

def free_entries_to_json(models):
    data = []
    for model in models:
        temp  = FreeEntrySerializer(model).data
        data.append(temp)
    return data