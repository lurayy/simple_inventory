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


data = {
        "action":"add",
        "ledger_entry":2,
        "amount":20,
        "remarks":'asdf'
    }

sess = requests.post(base_url+'accounting/ledger/entry/free/add', headers=headers, data=json.dumps(data), verify=False)
print(sess.text)