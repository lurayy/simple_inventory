import requests
import json

base_url = 'http://localhost:8000/api/v1/'

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


# data = {
#         "action":"add",
#         "ledger_entry":2,
#         "amount":20,
#         "remarks":'asdf'
#     }
# data = {"action":"add","payments":[{"invoice":"","purchase_order":1,"account":1,"amount":2233,"method":"2","bank_name":"","transaction_from":"","transaction_id":"","remarks":""}]}
# data  = {
#    "action":"add",
#    "payments":[
#       {
#          "invoice":None,
#          "invoice":1,
#          "account":4,
#          "amount":2233,
#          "method":1,
#          "bank_name":"",
#          "transaction_from":"",
#          "transaction_id":"",
#          "remarks":""
#       }
#    ]
# }

data  = {
   'action':'add',
   'payments': [
       {
            'invoice':None,
            'purchase_order':None,
            'amount':333,
            'method':3,
            'transaction_from':5,
            'transaction_id':531,
            'bank_name':'asdf',
            'remarks': 'asdf',
            'credit_payment_for':5,
            'account':8
       }
   ]
}
# base_url = "https://simpleim.herokuapp.com/api/v1/"

sess = requests.post(base_url+'payment/add', headers=headers, data=json.dumps(data), verify=False)
print(sess.text)