from django.db import models

class CustomPermission(models.Model):
    name = models.CharField(max_length=255)
    get_ledger_entry_details = models.BooleanField(default=True)
    add_new_ledger_entry = models.BooleanField(default=True)
    get_multiple_ledger_entries = models.BooleanField(default=True)
    get_multiple_ledger_entry_types = models.BooleanField(default=True)
    get_multiple_account_types = models.BooleanField(default=True)
    update_account = models.BooleanField(default=True)
    delete_accounts = models.BooleanField(default=True)
    get_account_details = models.BooleanField(default=True)
    add_new_account = models.BooleanField(default=True)
    get_multiple_accounts = models.BooleanField(default=True)
    apply_payment = models.BooleanField(default=True)
    get_payment_methods = models.BooleanField(default=True)
    update_gift_card = models.BooleanField(default=True)
    delete_unique_cards = models.BooleanField(default=True)
    validate_gift_card = models.BooleanField(default=True)
    delete_gift_cards = models.BooleanField(default=True)
    get_gift_card_details = models.BooleanField(default=True)
    get_multiple_gift_cards = models.BooleanField(default=True)
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
    get_single_place = models.BooleanField(default=True)
    delete_places = models.BooleanField(default=True)
    update_place = models.BooleanField(default=True)
    add_new_place = models.BooleanField(default=True)
    get_multiple_places = models.BooleanField(default=True)
    update_item_category = models.BooleanField(default=True)
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
    export_sales_data = models.BooleanField(default=True)
    add_new_tax = models.BooleanField(default=True)
    update_tax = models.BooleanField(default=True)
    delete_taxes = models.BooleanField(default=True)
    get_tax_details = models.BooleanField(default=True)
    get_multiple_taxes = models.BooleanField(default=True)
    add_new_discount = models.BooleanField(default=True)
    update_discount = models.BooleanField(default=True)
    delete_discount = models.BooleanField(default=True)
    get_discount_details = models.BooleanField(default=True)
    get_multiple_discounts = models.BooleanField(default=True)
    add_new_invoice_item = models.BooleanField(default=True)
    update_invoice_item = models.BooleanField(default=True)
    delete_invoice_items = models.BooleanField(default=True)
    get_invoice_details = models.BooleanField(default=True)
    get_multiple_invoices = models.BooleanField(default=True)
    get_customer_category = models.BooleanField(default=True)
    add_customer_categories = models.BooleanField(default=True)
    delete_customer_categories = models.BooleanField(default=True)
    update_customer_categories = models.BooleanField(default=True)
    add_new_customer = models.BooleanField(default=True)
    get_customer_details = models.BooleanField(default=True)
    get_customer_categories = models.BooleanField(default=True)
    delete_customers = models.BooleanField(default=True)
    update_customer = models.BooleanField(default=True)
    get_multiple_customers = models.BooleanField(default=True)
    add_new_invoice = models.BooleanField(default=True)
    update_invoice = models.BooleanField(default=True)
    delete_invoices = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name}"
