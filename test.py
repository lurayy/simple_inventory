import requests
import json

base_url = 'http://localhost:8000/api/v1/'
# base_url = "https://simpleim.herokuapp.com/api/v1/"

log_in_url = base_url+'user/auth'

creds = {
    'username':'lurayy',
    'password':'pass'
}


r = requests.post(log_in_url, data=creds)
token = r.json()['token']
r = requests.get(base_url+'user/verify')
csrftoken = r.json()['x-csrftoken']

headers = {
    'authorization': 'JWT '+token,
    'x-csrftoken': csrftoken
}

sess = requests.get(base_url+'user/current', headers=headers)
print(sess.text)
print()

data = {
  'action' : 'get',
  'barcode': 5065,
  'filter': 'barcode',
}
# data = {
#   "action": "add",
#   "payments": [
#     {
#       "credit_payment_for": 6,
#       "invoice": None,
#       "purchase_order": 1,
#       "account": 5,
#       "amount": 2500,
#       "method": 1,
#       "bank_name": "",
#       "transaction_from": "",
#       "transaction_id": "",
#       "remarks": ""
#     }
#   ]
# }


sess = requests.post(base_url+'inventory/purchaseitems/get', headers=headers, data=json.dumps(data), verify=False)
print(sess.text)