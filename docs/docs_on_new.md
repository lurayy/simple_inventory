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
- /inventory/items/export
```
data =  {
  'action' : 'export',
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