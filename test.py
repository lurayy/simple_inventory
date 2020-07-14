import requests
import json

base_url = 'http://localhost:8000/api/v1/'
# base_url = "https://simpleim.herokuapp.com/api/v1/"

log_in_url = base_url+'user/auth'

creds = {
    'username':'admin',
    'password':'pass'
}


r = requests.post(log_in_url, data=creds)
print(r.text)
token = r.json()['token']
r = requests.get(base_url+'user/verify')
csrftoken = r.json()['x-csrftoken']

headers = {
    'authorization': 'JWT '+token,
    'x-csrftoken': csrftoken
}


# data = {
#   "action": "get",
#   "filter": "multiple",
#   "filters": {
#     "name": False,
#     "category": False,
#     "code": False,
#     "discount_type": False,
#     "apply_limited": False,
#     "is_limited": False,
#     "apply_has_unique_codes": True,
#     "has_unique_codes": True,
#     "rate": False,
#     "rate_from": "",
#     "rate_upto": "",
#     "count_used": False,
#     "count_used_from": "",
#     "count_used_upto": ""
#   },
#   "start": 0,
#   "end": 25
# }

# data = {
#   "action":"get",
#   "filter":"none",
#   "start":0,
#   "end":25
# }

# data = {
#   "action": "get",
#   "filter": "multiple",
#   "filters": {
#     "account": 4,
#     "date": False,
#     "start_date": None,
#     "end_date": None,
#     "bundle_id": None,
#     "apply_is_add": False,
#     "is_add": False,
#     "amount": False,
#     "amount_from": "",
#     "amount_upto": "",
#     "payment_method": False
#   },
#   "start": 0,
#   "end": 25
# }

data = {
  'action' : 'get',
  'filter' : 'none',
  'account_id' : 1,
  'account_uuid': "df44354a-d2e5-4b21-ac4f-e456d5c2aea1",
  'start' : 0,
  'end' : 25
}
sess = requests.post(base_url+'accounting/account/transactions/get', headers=headers, data=json.dumps(data), verify=False)
print(sess.text)