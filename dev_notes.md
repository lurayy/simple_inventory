# TO-DO
1. Add model's function for stock management 
2. keep track of sales in purchaseitems too
3. Make a page where all the deleted(inactive) items are, waiting to be reveived

## Future Task 
- create a clean up script that deletes all the inactive objects in the database that are not related to anything (as a key)

### Things 
- make ;; To increase quntity, there must be objects unassigned on the related purchase_item
- in fend , is_active true is normal , false is muted gray  
- to apply discount or taxes, 2 saves have to be done. item.save() .save()
    - first save creates the relations 
    - second save triggers the update 
    
## complete 
- purchase_order/purchase_item
- Vendors


- Free entry is always added to the payment.amount.



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