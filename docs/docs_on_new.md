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
  'selected_fields': ["name", "description", "weight", "average_cost_price", "is_active", "catagory", "stock", "sales_price", "sold", "barcode"]
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
  'selected_fields': ["name", "description", "weight", "average_cost_price", "is_active", "catagory", "stock", "sales_price", "sold", "barcode"]
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
  notification_id : __id__
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