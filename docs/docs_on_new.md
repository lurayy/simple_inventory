## Gift card redeeme 
1. Redeeme Gift card: 
- payment/giftcard/redeeme
```
{
  'code' : 'FX5D671AA2',    [required]
  'action' : 'redeeme',     [required]
  'customer' : 1,           [required]
  'invoice':1,              [optional]
  'account':2               [required if invoice is given and accounting app is installed]
}
```

Possible Exceptions Throws : 
#### 1. Default payment method for gift card is not defined. Please setup the payment settings properly.
Solution : Setup default payment method in payment.settings. [use admin panel]

#### 2.Cannot redeeme gift card with discount in percentage without a invoice.
Solution : Add invoice

#### 3.This gift card is already redeemed.

#### 4.This gift card is not yet been activated. Please content the vendor of the gift card or the support.

#### 5.This gift card is not active so cannot be redeemed.

#### 6.This gift is not to be used a coupon. [has unique codes]

#### 7.This limited coupon has already reached it's limits.

#### 8.You need to install and setup the accounting module to use the accounting features.


2.  Get Redeeme History : 
- payment/giftcard/redeeme/histroy
```
{
  'action' : 'get',
  'filter' : "multiple",
  'filters' : {
    'gift_card' : 1,
    'unique_card' : None,
    'value': {
      'from': 0,
      'upto' : 10,
    },
    'invoice' : None,
    'customer' : None,
    'date' : {
        'from' : 
        'upto' :
    }
  },
  'start' :0,
  'end' : 2
}
```

## 3. Export Items : 
#### a. To pdf
- /inventory/items/export
```
data =  {
  'action' : 'export',
  'export' : 'pdf',
  'filters' : {
    'name' : None, / __str__,
    'weight' : None, / {
      'from' : 0,
      'upto' : None
    },
    'average_cost_price':  None / {
      'from' : 0,
      'upto' : None
    },
    'stock': None, / {'from' :  , 'upto':  }
    'sales_price': None / {'from' :  , 'upto':  },
    'category' : None / __id__,
    'sold' : None / {'from' :  , 'upto':  }
  },
  'start': 0,
  'end' : 25,
  'selected_fields': ["name", "description", "weight", "average_cost_price", "is_active", "category", "stock", "sales_price", "sold", "barcode"]
}
```
#### b. To excel : 
```
data =  {
  'action' : 'export',
  'export' : 'excel',
  'filters' : {
    'name' : None, / __str__,
    'weight' : None, / {
      'from' : 0,
      'upto' : None
    },
    'average_cost_price':  None / {
      'from' : 0,
      'upto' : None
    },
    'stock': None, / {'from' :  , 'upto':  }
    'sales_price': None / {'from' :  , 'upto':  },
    'category' : None / __id__,
    'sold' : None / {'from' :  , 'upto':  }
  },
  'start': 0,
  'end' : 25,
  'selected_fields': ["name", "description", "weight", "average_cost_price", "is_active", "category", "stock", "sales_price", "sold", "barcode"]
}
```

- To get fields that can be selected 
```
{
  action : get
}
```


## 4. Dashboard data

#### a. Accounting : 
- /accounting/summary
```
{
  action : get,
  filters : {
    date : None / {
      'from' : ,
      'upto' : ,
    }
  }
}
```
- return profit, expense and revenue.

#### b. Inventory :
- /inventory/summary
```
 {
    'action' : 'get',
    'filters' : {
        'low_items' : {
            'start' : __int__,
            'end' : __int__
        },
        'most_sold_items' : {
            'start' : __int__,
            'end' : __int__
        },
    }
}
```
- returns count of active items, total sold, list of low stock items in order and list of most sold items in order

#### c. Sales
- sales/summary
```
{
    'action' : 'get',
    'filters' : {
        'date' : {
            'start' : __datetime__,
            'end' :  __datetime__)
        },
        'delta' : __int__     [in days]
    }
}
```


## Get settings
a. Sales Settings
- [GET]
- /sales/settings/get

b. Universal Settings
- [GET]
- /user/settings/get

## Notification : 

1. GET : 
- user/notifications/get
```
{
  action : get,
  start : 
  end : 
  read : __bool__
}
```

2. Read:
- user/notifications/read
```
{
  action : read,
  notification_id :[ __id__,__id__,__id__,__id__ . . . ]
}
```


## Credit payment 
- payment/credit/pay
```
{
  action : credit_payment,
  credit_id : __payment_id__,
  amount : __float__,
  method : __method__,
  transaction_from : 
  transaction_id : 
  bank_name : 
  remarks
  choosen_account : account_id                  <= account id /cash ac
}
```

### bar code generator
- inventory/generate
```
{
  'action' : 'create',
  'type' : 'barcode',
  'count' : __int__
}
```

### import items 
- /inventory/import
```
{
  action : import,
  csv_file : __base64_of_csv__
}
```

eg : 
```
{
  'action' : 'import',
  'csv_file' : "bmFtZSxkZXNjcmlwdGlvbix3ZWlnaHQsY2F0ZWdvcnksc3RvY2ssc2FsZXNfcHJpY2UscHVyY2hhc2VfcHJpY2UsYmFyY29kZSx2YXRfZW5hYmxlZAppdGVtMSxsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDQyMzQyMzIsMQppdGVtMixsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDI1MTMyMDMsMQppdGVtMyxsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDI1MTMyMDIsMQ=="
}
```


- Excel Column Format
```name,description,weight,category,stock,sales_price,purchase_price,barcode,vat_enabled```


### Invoice Bill Export
- /sales/invoice/bill
```
{
  action : export,
  invoice: __invoice_id__
}
```



- Free entry is always added to the payment.amount.

- mass is always saved in grams in database.

Search filter for accounts : 

### non filter
{
  action : get,
  filter : none,
  start : 
  end :
}

### gives closed account
{
  action : get,
  filter : closed
  start : 
  end 
}

### name
{
  action  :get,
  filter : name,
  name : 
  start 
  end 
}

### Get only parent 
{
  action : get ,
  filter : parent,
  start 
  end 
}

### get child 
{
  action : get ,
  filter : account,
  account_id : 
  start :0 
  end : 0
}

### vendor 
{
  action : get 
  filter : vendor,
  vendor : vendor_id
  start
  end

}

### customer 
{
  action : get,
  filter : customer,
  customer : customer_id,
  start : 
  end : 
}


### multiple 
{
  action : get ,
  fliter : multiple,
  filters : {
    status: True/False
      closed : True/False,
    name: False/name_keyword,
    vendor : False/vendor_id,
    customer  : False/customer_id,
    current_amount  : True/False,
        current_amount_from : 
        current_amount_upto:
    credits  :True/False,
        credits_from
        credits_upto
    parent : True/False

    account_type : False/account_type_id,
    header : False/header_str
  }

  start : 
  end : 
}


# ledger entires filter : 
{
  'action' : get,
  filter : none
  start : 
  end :
}

### account : 
{
  action : get,
  filter : account,
  start : 
  end : 
  account_id : account_id
}

### multiple 
{
  action : get,
  start : 
  end : 
  filter : multiple 
  filters : {
    account : False/account_id,
    date : True/False,
      start_date,
      end_date,
    bundle_id : false/bundle_id,
    apply_is_add: True/False
        is_add : True/False
    amount : 
      amount_from 
      amount_upto
    payment_method :  False/payment_method_id
  }
}

# Gift cards : 
{
  action : get,
  filter :none
  start : 
  end : 
}

{
  action  : get 
  filter : name
  name  
  start 
  end
}

{
  action : get
  filter : code
  code : 
  start : 
  end : 
}

{
  action : get
  filter : multiple
  start 
  end 
  filters : {
    name : False/name
  category : False/category_id
  code : False/code_name,
  discount_type : False/percent
  apply_limited : True/False
    is_liimited :True/False
  apply_has_unique_codes : bool  
    has_unique_codes  : bool
  rate : bool
    rate_from
    rate_upto
  count_used  :bool
    count_used_from
    count_used_upto
  }
}


# Tax 
{
  action : get
  filter : none
  start 
  end 
}

{
  action  :get 
  filter : multiple
  filters : {
    name : False/str
    tax_type  : False/str
    code : False/str
    rate : bool
      rate_from : float
      rate_upto : float
  }
  start 
  end 
}


# Discount 
{
  action : get
  filter : none
  start 
  end 
}

{
  action  :get 
  filter : multiple
  filters : {
    name : False/str
    discount_type  : False/str
    code : False/str
    rate : bool
      rate_from : float
      rate_upto : float
  }
  start 
  end 
}



  name, description (optional) , weight( in grams 0 or value) , category, stock, sales_price, sold,  barcode , vat enabled (0 or 1), purchase_price, Quantity
