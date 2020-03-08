from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm

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
    print(form)
    return render(request, 'inventory/create_purchase_order.html',{'form':form})
    


