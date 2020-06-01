#### 1. Get Multiple Accounts Details 
- URL : api/v1/accounting/accounts/get
```
    {
        "action":"get",
        "start":0,
        "end":20,
        "filter":"none"
    }
```
- filter : name 
```
    {
        "action":"get",
        "start":0,
        "end":20,
        "filter":"name",
        "name": "someKeyword"
    }
```

#### 2. Add New Account 
- URL : api/v1/accounting/account/add
```
    {
        "action":"add",
        "account_type":1,
        "name":"new account",
        "opening_balance":5,
        "opening_date":"2018-12-19T09:26:03.478039",
        "parent":True,
        "parent_id":2,
        "parent_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97"
    }
```

#### 3. Get Account Details 
- URL : api/v1/accounting/accounting/account/get
```
    {
        "action":"get",
        "account_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97"
    }
```

#### 4. Delete Accounts
- URL :  api/v1/accounting/accounts/delete
```
    {
        "action":"delete",
        "accounts_ids : [1],
        "accounts_uuids":["a9140902-7863-40f6-b01a-ec5045d38c97"]
    }
```

#### 5. Update Account 
- URL : api/v1/accouting/account/update
```
    {
        "action":"update/delete/close",
        "accounts_id" : 1,
        "accounts_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97",
        "name": "temp",
        "opening_date":"2018-12-19T09:26:03.478039",
        "new_parent":True/False
        "parent_id":2,
        "parent_uuid":"a9140902-7863-40f6-b01a-ec5045d38c97"
    }
```
