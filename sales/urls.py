from django.urls import path
from . import views
urlpatterns = [
    path('invoices/get', views.get_multiple_invoices, name="GET and add invoices"),
    path('invoices/delete', views.delete_invoices, name='Get and edit data ofa invoice'),
    path('invoice/get', views.get_invoice_details, name='dlete invoice'),
    path('invoice/update', views.update_invoice, name="status"),
    path('invoice/add', views.add_new_invoice, name='add'),

    path('customers/get', views.get_multiple_customers, name=""),
    path('customer/update', views.update_customer, name=''),
    path('customers/delete', views.delete_customers, name="delete customers"),
    path('customers/category', views.get_customer_categories, name='customer category'),
    path('customer/get', views.get_customer_details, name=''),
    path('customer/add', views.add_new_customer, name=''),
    path('customers/category/update', views.update_customer_categories),
    path('customers/category/delete', views.delete_customer_categories),
    path('customers/category/add', views.add_customer_categories),

    path('invoiceitems/get', views.get_multiple_invoices, name=""),
    path('invoiceitem/get', views.get_invoice_details, name=''),
    path('invoiceitems/delete', views.delete_invoice_items, name=""),    
    path('invoiceitems/update', views.update_invoice_item, name=""),
    path('invoiceitem/add', views.add_new_invoice_item, name=''),

    path('discounts/get', views.get_multiple_discounts, name=""),
    path('discount/get', views.get_discount_details, name=''),
    path('discounts/delete', views.delete_discount, name=""),
    path('discount/update', views.update_discount, name=''),
    path('discount/add', views.add_new_discount, name=''),

    path('taxes/get', views.get_multiple_taxes, name=""),
    path('tax/get', views.get_tax_details, name=''),
    path('taxes/delete', views.delete_taxes, name=""),
    path('tax/update', views.update_tax),
    path('tax/add', views.add_new_tax),

    path('export',views.export_sales_data, name="export data related to sales")
]