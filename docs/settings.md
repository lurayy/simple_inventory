# Settings 

1. Universal Settings

a. Get
- /user/settings/get

b. Update settings 
- /user/settings/update
```
{
    action : update ,
    default_weight_unit : kg/g/lb  or Null,
    company :str / null
    
    company_address : str /null
    branch :str/ null
    branch_code : str / null - will be used  in invoice number
    pan_number : str /null
    manufacturer : str/null
    distributor : str/null
    contact  : str/null
    manufacturer_address : str/null
    manufacturer_website : str/nul
    change_fisal_year : date() / Null          # only using day and month 
    stock_low_notification_on  : __int__ /null,
    ird_username : str/null,
    ird_password : str/null
}
```


2. Sales Settings

a. Get
- /sales/settings/get

b. Update settings
- /sales/settings/update
```
{
    action : update
    default_place_to_sold_from  : __place_id__/null ,
    default_vat_tax : __tax_id__ / null
}
```


3. Payment Settings

a. Get
- /payment/settings/get

b. Update
- /payment/settings/update
```
{
    action : update,
    default_gift_card_payment_method : __payment_method_id__ / NUll
}
```

4. Accounting Settings

a. Get
- /accounting/settings/get

b. Update 
- /accounting/settings/update
```
{
    action : update,

    default_purchase_account_on_cash : __id__ / Null,
    default_purchase_account_on_credit : __id__ / Null,
    default_purchase_account_on_bank : __id__ / Null,
    default_purchase_account_on_transfer : __id__ / Null,
    default_purchase_account_on_pre_paid : __id__ / Null,
    default_invoice_account_on_credit : __id__ / Null,
    default_invoice_account_on_cash : __id__ / Null,
    default_invoice_account_on_bank : __id__ / Null,
    default_invoice_account_on_transfer : __id__ / Null,
    default_invoice_account_on_pre_paid : __id__ / Null,
    default_invoice_account_on_credit : __id__ / Null, 

    default_purchase_action_on_cash_is_add : null / {
        state : __bool__
    }
    default_purchase_action_on_credit_is_add : null / {
        state : __bool__
    }
    default_purchase_action_on_bank_is_add : null / {
        state : __bool__
    }
    default_purchase_action_on_transfer_is_add : null / {
        state : __bool__
    }
    default_purchase_action_on_pre_paid_is_add : null / {
        state : __bool__
    }
    default_invoice_action_on_cash_is_add : null / {
        state : __bool__
    }
    default_invoice_action_on_credit_is_add : null / {
        state : __bool__
    }
    default_invoice_action_on_bank_is_add : null / {
        state : __bool__
    }
    default_invoice_action_on_transfer_is_add : null / {
        state : __bool__
    }
    default_invoice_action_on_pre_paid_is_add : null / {
        state : __bool__
    }

}
```


5. Notification settings

a. Get
- /user/notifications/settings/get

b. Update 
```
{
    action : update,
    notification_setting_id : __id__,
    roles : [
        role_id, role_id , 
    ]                   <- New Role set
}
```