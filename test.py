import requests
import json
import datetime

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
    return (sess.json())

if __name__ == "__main__":
    headers = login()
    url = 'v1/user/role/valid'
    data = {
        'action' : 'get'
    }
    valids = call(headers, data, url)['valid_powers']
    data = {
        'action' : 'add',
        'name' : 'sdf33',
        'description' : 'asdfasdfasdf',
        'powers' : valids,
    }
    values = []
    for valid in valids:
        values.append(True)
    data['values'] = values
    url = 'v1/user/role/add'
    print(call(headers, data, url))

