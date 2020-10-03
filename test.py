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
    url = 'v1/inventory/item/update'
    data ={
  "action": "update",
  "item_id": 1,
  "name": "test closed",
  "sales_price": 444,
  "category": 1,
  "description": "",
  "weight": 0.065,
  "weight_unit": "kg",
  "average_cost_price": 33,
  "product_images": [],
  "remove_image": [],
  "barcode": "443434",
  "vat_enabled": True,
  "is_active": True
}
    call(headers, data, url)