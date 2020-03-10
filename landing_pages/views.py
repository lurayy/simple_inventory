from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm, PurchaseItemForm
from inventory.models import PurchaseOrder, PurchaseItem 
from inventory.utils import purchase_orders_to_json, purchase_items_to_json

@login_required
def purchase_orders(request):
    return render (request, 'inventory/purchase_orders.html')

@login_required
def dashboard(request):
    return render (request, 'dashboard.html')

@login_required
def staff_list(request):
    return render(request, 'user/staff_list.html')


@login_required
def vendors(request):
    return render (request, 'inventory/vendors.html')

@login_required
def items(request):
    return render (request, 'inventory/items.html')

@login_required
def places(request):
    return render (request, 'inventory/places.html')

@login_required
def invoices(request):
    return render (request, 'sales/invoices.html')

@login_required
def customers(request):
    return render (request, 'sales/customers.html')


@login_required
def create_purchase_order(request):
    form = PurchaseOrderForm()
    return render(request, 'inventory/create_purchase_order.html',{'form':form})
    
@login_required
def edit_purchase_order(request,id):
    order_object = PurchaseOrder.objects.get(id=id)
    order = purchase_orders_to_json([order_object])
    form = PurchaseOrderForm(
        initial=order[0]
    )
    items_obj = order_object.items.all()
    item_forms = []
    for item  in items_obj:
        temp = purchase_items_to_json([item])
        item_form = PurchaseItemForm(
            initial = temp[0]
        )
        item_forms.append(item_form)
    return render(request, 'inventory/purchase_order.html',{'form':form, 'item_forms':item_forms})


