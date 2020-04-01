from django.urls import path
from . import views
urlpatterns = [
    path('invoices', views.invoices, name="GET and add invoices"),
    path('invoice', views.invoice, name='Get and edit data ofa invoice'),
    path('invoices/delete', views.delete_invoices, name='dlete invoice'),

    path('invoices/status', views.invoice_status, name="status"),

    path('customers', views.customers, name=""),
    path('customer', views.customer, name=''),
    path('customers/delete', views.delete_customers, name="delete customers"),

    path('invoiceitems', views.invoice_items, name=""),
    path('invoiceitem', views.invoice_item, name=''),
    path('invoiceitems/delete', views.delete_invoice_items, name=""),

    
    path('discounts', views.discounts, name=""),
    path('discount', views.discount, name=''),
    path('discounts/delete', views.delete_discount, name=""),

    path('taxes', views.taxes, name=""),
    path('tax', views.tax, name=''),
    path('taxes/delete', views.delete_taxes, name=""),
]