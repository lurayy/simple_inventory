## Gift Card Category 

1. Get multiple gift card category 
- /payment/giftcards/categories/get
```
{
    action : get,
    filter : none,
    start : __int__,
    end : __int__
}
```
- With Filters :
```
{
    action : get,
    filter : multiple,
    filters : {
        name : None / __str__,
        status : None / {
            is_active : __bool__
        }
    }
}
```

2. Get Gift Card Category
- /payment/giftcards/category/get
```
{
    action : get,
    gift_card_category : __id__
}
```

3. Add Gift Card Category
- /payment/giftcards/category/add
```
{
    action : add,
    name : __str__
}
```

4. Update gift card category 
- /payment/giftcards/category/update
```
{
    action : update,
    name : None / __str__,
    is_active : None / __bool__                 [works for making it True only]
}
```

5. Delete Gift card category 
- /payment/giftcards/category/delete
```
{
    action : delete,
    gift_card_categories : [
        __id__,
        __id__,
        ...
    ]
}
```