from django.db import models

class CustomPermission(models.Model):
    name = models.CharField(max_length=255)
    apply_payment = models.BooleanField(default=True)
    payment_methods = models.BooleanField(default=True)
    validate_gift_card = models.BooleanField(default=True)
    delete_gift_cards = models.BooleanField(default=True)
    gift_card = models.BooleanField(default=True)
    gift_cards = models.BooleanField(default=True)
    get_current_user = models.BooleanField(default=True)
    s_user = models.BooleanField(default=True)
    users = models.BooleanField(default=True)
    user_creation = models.BooleanField(default=True)
    user_logout = models.BooleanField(default=True)
    update_purchase_item = models.BooleanField(default=True)
    get_purchase_item_details = models.BooleanField(default=True)
    delete_purchase_items = models.BooleanField(default=True)
    add_new_purchase_item = models.BooleanField(default=True)
    get_mulitple_purchase_items = models.BooleanField(default=True)
    export_inventory = models.BooleanField(default=True)
    get_placements = models.BooleanField(default=True)
    assign_place = models.BooleanField(default=True)
    delete_places = models.BooleanField(default=True)
    update_place = models.BooleanField(default=True)
    add_new_place = models.BooleanField(default=True)
    get_multiple_places = models.BooleanField(default=True)
    delete_item_catagories = models.BooleanField(default=True)
    get_item_catagory_details = models.BooleanField(default=True)
    add_new_item_catagory = models.BooleanField(default=True)
    get_multiple_item_catagories = models.BooleanField(default=True)
    delete_items = models.BooleanField(default=True)
    update_item = models.BooleanField(default=True)
    get_item_details = models.BooleanField(default=True)
    add_new_item = models.BooleanField(default=True)
    get_multiple_items = models.BooleanField(default=True)
    get_vendor_details = models.BooleanField(default=True)
    update_vendor = models.BooleanField(default=True)
    delete_vendors = models.BooleanField(default=True)
    add_new_vendor = models.BooleanField(default=True)
    get_multiple_vendors = models.BooleanField(default=True)
    delete_purchase_orders = models.BooleanField(default=True)
    update_purchase_order = models.BooleanField(default=True)
    get_purchase_order_details = models.BooleanField(default=True)
    add_new_purchase_order = models.BooleanField(default=True)
    get_multiple_purchase_orders = models.BooleanField(default=True)
    purchase_order_statuss = models.BooleanField(default=True)
    export_data = models.BooleanField(default=True)
    delete_taxes = models.BooleanField(default=True)
    tax = models.BooleanField(default=True)
    taxes = models.BooleanField(default=True)
    delete_discount = models.BooleanField(default=True)
    discount = models.BooleanField(default=True)
    discounts = models.BooleanField(default=True)
    delete_invoice_items = models.BooleanField(default=True)
    invoice_item = models.BooleanField(default=True)
    invoice_items = models.BooleanField(default=True)
    customer_category = models.BooleanField(default=True)
    delete_customers = models.BooleanField(default=True)
    customer = models.BooleanField(default=True)
    customers = models.BooleanField(default=True)
    invoice_status = models.BooleanField(default=True)
    delete_invoices = models.BooleanField(default=True)
    invoice = models.BooleanField(default=True)
    invoices = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'