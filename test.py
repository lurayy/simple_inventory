import requests
import json
# base_url = "https://erp.mandalaitsolutions.com/api/v1/"
base_url = 'http://localhost:8000/api/v1/'

def login():    
    creds = {
        "username":"admin",
        "password":"pass"
    }
    log_in_url = base_url+"user/auth"

    r = requests.post(log_in_url, data=json.dumps(creds))
    # print(r.text)
    token = r.json()["token"]

    # print(token)

    headers = {
        "authorization":'JWT '+token,
    }

    sess = requests.get(base_url+"user/current", headers=headers)
    # print(sess.text)
    return headers

def call(headers, data, url):
    sess = requests.post(base_url+url, headers=headers, data=json.dumps(data))
    print(sess.text)

if __name__ == "__main__":
    headers = login()

    data = {
        'action' : 'get',
        'filter' : 'barcode',
        'barcode' :"9",
        'filters' : {
            'is_applied_name': True,
            'exact_name' : False,
            'name' : 'no',
            'is_applied_weight_from' : None,
            'is_applied_weight_upto' : None,
            'is_applied_average_cost_price_from' : None,
            'is_applied_average_cost_price_upto' : None,
            'is_applied_stock_upto' : None,
            'is_applied_stock_from' : None,
            'is_applied_sold_upto' : None,
            'is_applied_sold_from' : None,
            'is_applied_sales_price_from' : None,
            'is_applied_sales_price_upto' : None,
            'is_applied_category' : None
        },
        'start' : 0,
        'end' : 25
    }
    url = 'inventory/items/get'
    call(headers, data, url)