import requests
import json
import datetime

# base_url = "https://erp.mandalaitsolutions.com/api/v1/"
base_url = 'http://localhost:8000/api/'  

def login():    
    creds = {
        "username":"admin",
        "password":"pass"
    }
    log_in_url = base_url+"v1/user/auth"
    r = requests.post(log_in_url, data=json.dumps(creds))
    token = r.json()["token"]
    headers = {
        "authorization":'JWT '+token,
    }
    sess = requests.get(base_url+"v1/user/current", headers=headers)
    return headers

def call(headers, data, url):
    sess = requests.post(base_url+url, headers=headers, data= json.dumps(data))
    print(sess.text)

if __name__ == "__main__":
    headers = login()
    url = 'v1/sales/invoiceitems/update'
    data = {
        "action": "update_multiple",
        "invoice_items": [
            {
            "invoice_item_id": 1,
            "invoice": 1,
            "item": 1,
            "sold_from": 1,
            "purchase_item": 1,
            "quantity": 120,
            "price": 976,
            "discounts": [],
            "taxes": [
                1
            ]
            }
        ]
    }
    call(headers, data, url)