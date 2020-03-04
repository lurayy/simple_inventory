from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import json

from .models import PurchaseOrder, Item, PurchaseItem, Place, Placement
from .utils import get_data_from_purchase_orders, get_data_from_purchase_items

@login_required
@require_http_methods(['POST'])
def purchase_orders(request):
    '''
    View for handling operations related to Purchase order
    fomats : 
    GET: 
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'none',/'date',/'vendor',/'added_by',
    }
    '''
    if request.method == "POST":
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        # GET Handler
        if str(data_json['action']).lower() == "get":
            start = int(data_json["start"])
            end = int(data_json["end"])
            response_json = {'status':'', 'p_orders':[]}
            if str(data_json['filter']).lower() == "none":
                orders = PurchaseOrder.objects.filter().order_by('-invoiced_on')[start:end]
                response_json['p_orders'] = get_data_from_purchase_orders(orders)
                response_json['status'] = True
                return JsonResponse(response_json)


def purchase_order(request,id):
    ''' To get data about single purchase order
    '''
    response_json = {'status':'', 'p_order':{}, 'p_items':[]}
    order = PurchaseOrder.objects.get(id=int(id))
    response_json['p_order'] = get_data_from_purchase_orders([order])

    response_json['p_items'] = get_data_from_purchase_items(PurchaseItem.objects.filter(purchase_order=order))
    response_json['status'] = True
    return JsonResponse(response_json)

