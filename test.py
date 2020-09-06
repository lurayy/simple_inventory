import requests
import json
base_url = "https://erp.mandalaitsolutions.com/api/v1/"

def login():    
    creds = {
        "username":"admin",
        "password":"pass"
    }
    log_in_url = base_url+"user/auth"

    r = requests.post(log_in_url, data=json.dumps(creds))
    print(r.text)
    token = r.json()["token"]

    print(token)

    headers = {
        "authorization":'JWT '+token,
    }

    sess = requests.get(base_url+"user/current", headers=headers)
    print(sess.text)
    return headers

def call(headers, data, url):
    sess = requests.post(base_url+url, headers=headers, data=json.dumps(data))
    print(sess.text)

if __name__ == "__main__":
    headers = login()
    with open('zip.txt', 'r') as zip:
        file_str = zip.read()
    
    data = {
        'action' : 'restore',
        'method' : 'upload',
        'file' : file_str
    }
    
    url = 'user/backup/restore'
    call(headers, data, url)