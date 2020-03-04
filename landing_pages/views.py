from django.shortcuts import render

def purchase_order(request):
    return render (request, 'inventory/purchase_order.html')
