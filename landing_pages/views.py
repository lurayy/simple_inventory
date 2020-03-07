from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def purchase_orders(request):
    return render (request, 'inventory/purchase_orders.html')

@login_required
def dashboard(request):
    return render (request, 'dashboard.html')