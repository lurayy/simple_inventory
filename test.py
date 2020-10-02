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
    url = 'v1/sales/invoice/update'
    data ={
  "action": "update",
  "invoice_id": 1,
  "customer": 8,
  "invoiced_on": "2020-10-02T07:04:44.142Z",
  "due_on": "2020-10-02T07:04:44.142Z",
  "additional_discount": 0,
  "total_weight": 3.84,
  "is_sent": False,
  "weight_unit": "kg",
  "status": 1
}
    call(headers, data, url)