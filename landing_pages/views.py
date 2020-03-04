from django.shortcuts import render

def purchase_orders(request):
    return render (request, 'inventory/purchase_orders.html')
