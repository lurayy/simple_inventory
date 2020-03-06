from django.urls import path
from . import views
urlpatterns = [
    path('invoices', views.invoices, name="GET and add invoices"),
    path('invoices/<int:id>', views.invoice, name='Get and edit data ofa invoice'),
    path('invoices/delete', views.delete_invoices, name='dlete invoice'),

    path('customers', views.customers, name=""),
    path('customers/<int:id>', views.customer, name=''),
    path('customers/delete', views.delete_customers, name="delete customers"),
    path('invoiceitems', views.invoice_items, name=""),
    path('invoiceitem/<int:id>', views.invoice_item, name=''),
    path('invoiceitems/delete', views.delete_invoice_items, name=""),
]