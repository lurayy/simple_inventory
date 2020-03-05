from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def purchase_orders(request):
    return render (request, 'inventory/purchase_orders.html')
