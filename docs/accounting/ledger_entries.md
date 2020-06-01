#### 1. Get Multiple Ledger Entries
- URL : api/v1/accouting/ledger/entries/get
```
    url : api/v1/accouting/ledger/entries/get
    {
        "action":"get",
        "filter":"none",
        "start":0,
        "end":5
    }
    {
        "action":"get",
        "filter":"account",
        "start":0,
        "end":5,
        "account_id":1
    }
```

#### 2. Add New Legder Entry
- URL : api/v1/accounting/ledger/entry/add
```
    {
        "action":"add",
        "account_id":1,
        "ledger_entry_type_id":2,
        "remarks":"some sassy remarks",
        "date":"2018-12-19T09:26:03.478039",
        "amount":25.2153
    }
```

#### 3. Get Ledger Entry Details
- URL : api/v1/accouting/ledger/entry/get
```
    {
        "action":"get",
        "ledger_entry_id":2
    }
```
