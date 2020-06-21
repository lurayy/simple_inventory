try:
            stat = MonthlyStats.objects.filter(date__year = instance.entry_for.date.year).filter(date__year = instance.entry_for.date.month)
            stat = stat[0]
        except:
            stat = MonthlyStats.objects.create(
                date = instance.entry_for.date
            )

        if instance.entry_for.entry_type.is_add:
            if instance.entry_for.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets + instance.amount
            elif instance.entry_for.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities + instance.amount
            elif instance.entry_for.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue  + instance.amount
            elif instance.entry_for.entry_type.header == "expense":
                stat.total_expense = stat.total_expense + instance.amount
            elif instance.entry_for.entry_type.header == "draw":
                stat.total_draw = stat.total_draw + instance.amount
            elif instance.entry_for.entry_type.header == "equity":
                stat.total_equity = stat.total_equity + instance.amount
        else:
            if instance.entry_for.entry_type.header == "assets":
                    stat.total_assets = stat.total_assets - instance.amount
            elif instance.entry_for.entry_type.header == "liabilities":
                stat.total_liabilities = stat.total_liabilities - instance.amount
            elif instance.entry_for.entry_type.header == "revenue ":
                stat.total_revenue  = stat.total_revenue - instance.amount
            elif instance.entry_for.entry_type.header == "expense":
                stat.total_expense = stat.total_expense - instance.amount
            elif instance.entry_for.entry_type.header == "draw":
                stat.total_draw = stat.total_draw - instance.amount
            elif instance.entry_for.entry_type.header == "equity":
                stat.total_equity = stat.total_equity - instance.amount
        stat.save()


@receiver(post_save, sender=Payment)
def handle_accounting_for_payment_post_save(sender, instance, created, **kwargs):
    settings = DefaultEntryType.objects.filter(is_active=True)[0]
    if created:
        signals.post_save.disconnect(handle_accounting_for_payment_post_save, sender=Payment)
        instance.save()
        signals.post_save.connect(handle_accounting_for_payment_post_save, sender=Payment)
        if instance.purchase_order or instance.invoice:
            invoice = True
            if instance.purchase_order:
                invoice = False
                if instance.invoice:
                    raise Exception("Both invoice and purchase order cann be assigned to same payment.")
            if instance.method.header == "credit":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account_on_cr,
                        entry_type = settings.entry_type_for_credit_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account_on_dr,
                        entry_type = settings.entry_type_for_credit_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_credit_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_credit_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "pre-paid":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_pre_paid_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_pre_paid_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_pre_paid_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_pre_paid_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "cash":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_cash_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_cash_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_cash_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_cash_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "transfer":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_transfer_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_transfer_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_transfer_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_transfer_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
            if instance.method.header == "bank":
                if invoice:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_bank_invoice_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_sales_account,
                        entry_type = settings.entry_type_for_bank_invoice_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.invoice.invoice_number
                        )
                else:
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_dr,
                        entry_type = settings.entry_type_for_bank_purchase_order_dr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )
                    entry = LedgerEntry.objects.create(
                        payment = instance,
                        account = settings.default_purchase_account_on_cr,
                        entry_type = settings.entry_type_for_bank_purchase_order_cr,
                        date = django.utils.timezone.now(),
                        bundle_id = instance.purchase_order.uuid
                        )   



# For payment update
# @receiver(pre_save, sender=Payment)
# def pre_save_payment_handler(sender, instance, *args, **kwargs):
#     if instance.id:
#         old = Payment.objects.get(id=instance.id)
#         if instance.amount != old.amount:
#             amount  = instance.amount - old.amount
#             for entry in LedgerEntry.objects.filter(payment = instance):
#                 free = FreeEntryLedger.objects.create(
#                     entry_for = entry,
#                     amount = amount
#                 )


# @receiver(models.signals.post_save, sender=PurchaseOrder)
# def handle_accounting_post_save(sender, instance, created, **kwargs):
#     print("ledger entry")
#     print(instance.status.is_end)
#     if instance.status.is_end:
#         settings = AccountingSettings.objects.filter(is_active=True)[0]
#         date = django.utils.timezone.now()
#         remarks = str(instance.uuid) + str(date)
#         if instance.discount_type == "percent":
#             purchase_cost = instance.total_cost - instance.total_cost*0.01*instance.discount
#         else:
#             purchase_cost = instance.total_cost - instance.discount
#         x =  LedgerEntry.objects.filter(account = settings.default_purchase_account, entry_type = settings.default_purchase_order_entry_type_on_dr, remarks=remarks)
#         y = LedgerEntry.objects.filter(account = settings.default_purchase_account, entry_type = settings.default_purchase_order_entry_type_on_cr, remarks=remarks)
#         if len(x) < 0:
#             reverse_entries(x)
#         if len(y) < 0:
#             reverse_entries(x)
#         entry = LedgerEntry.objects.create(
#             account = settings.default_purchase_account,
#             entry_type = settings.default_purchase_order_entry_type_on_dr,
#             date = datetime.datetime.today(),
#             remarks = remarks,
#             amount = purchase_cost
#         )
#         print(entry)
#         entry2 = LedgerEntry.objects.create(
#             account = settings.default_purchase_account,
#             entry_type = settings.default_purchase_order_entry_type_on_cr,
#             remarks = remarks,
#             amount = purchase_cost,
#             date = datetime.datetime.today()
#         )
#         entry.save()
#         entry2.save()



def reverse_entries(entries):
    for entry in entries:
        remarks = "reverse_minus" + entry.remarks
        x = LedgerEntry.objects.create(
            accounnt = entry.account,
            entry_type = entry.entry_type,
            remarks = remarks,
            amount = -1*entry.amount,
            date = datetime.datetime.today()
        )
        x.save()
        entry.remarks = "reverse_plus" + entry.remarks
        entry.save()



@require_http_methods(['POST'])
@bind
def get_multiple_ledger_entry_types(self, request):
    '''
    url : api/v1/accouting/ledger/type/get
    '''
    response_json = {'status':False}
    if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
        response_json = {'status':False}
        try:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['action'] =="get":
                response_json['ledger_entry_types'] = entry_types_to_json(EntryType.objects.filter(is_active=True))
                response_json['status'] = True
            return JsonResponse(response_json)
        except (KeyError, json.decoder.JSONDecodeError,  IntegrityError, ObjectDoesNotExist, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        return JsonResponse({'status':False, "error":'You are not authorized.'})
