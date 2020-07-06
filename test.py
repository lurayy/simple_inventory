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
print(r.text)
token = r.json()['token']
r = requests.get(base_url+'user/verify')
csrftoken = r.json()['x-csrftoken']

headers = {
    'authorization': 'JWT '+token,
    'x-csrftoken': csrftoken
}

data = {
  'action': 'get',
  'filter': 'added_by',
  'added_by' : user_id
}


data = {
  'action': 'get',
  'filter': 'invoice_number',
  'invoice_number' : 
}

# sess = requests.post(base_url+'inventory/purchaseitems/get', headers=headers, data=json.dumps(data), verify=False)
# print(sess.text)