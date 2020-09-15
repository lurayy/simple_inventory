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
    token = r.json()["token"]
    headers = {
        "authorization":'JWT '+token,
    }
    sess = requests.get(base_url+"user/current", headers=headers)
    return headers

def call(headers, data, url):
    sess = requests.post(base_url+url, headers=headers, data=json.dumps(data))
    print(sess.text)


def restore():    
    url = 'user/backup/restore'
    data = {
        'action' : 'restore',
        'method' : 'selection',
        'date': '2020-09-15',
        'time' : '16:03:55'
    }
    call(headers, data, url)

def backup():
    url = 'user/backup/create'
    data = { 
        'action' : 'backup'
    }
    call(headers, data, url)

    url = 'user/backups/get'
    data = {
        'action' : 'get',
    }
    call(headers, data, url)


if __name__ == "__main__":
    headers = login()
    # backup()
    restore()

    # url = 'accounting/accounts/types/get'
    # data = {
    #         "action": "get",
    #         "filter": "multiple",
    #         "filters": {
    #             "name": "a",
    #             "header": None,
    #             "status": None
    #         },
    #         "start": 0,
    #         "end": 50
    #     }
    # call(headers, data, url)



# import datetime

# url = "http://103.1.92.174:9050/api/bill"
# from bikram import samwat
# import json
# import requests
# # data = {
# #     'username' : "Test_CBMS",
# #     'password' : "test@321",
# #     'seller_pan' : '89415',
# #     'buyer_pan' : '84512',
# #     'fiscal_year' : "2077.2078",
# #     'buyer_name' : 'test man',
# #     'invoice_number' : "8465132",
# #     'invoice_date' : "2074.06.25",
# #     'total_sales' : 1130,
# #     'taxable_sales_vat' : 1000 ,
# #     'vat' : 130,
# #     'excisable_amount' :0 ,
# #     'excise' : 0,
# #     'taxable_sales_hst' : 0,
# #     'hst' : 0,
# #     'amount_for_esf' : 0,
# #     'esf' : 0,
# #     'export_sales' : 0,
# #     'tax_exmpted_sales' :0 ,
# #     'isrealtime' : True,
# #     'datetimeClient' :  str(datetime.datetime.now()),
# # }

# data  = {
#     'username' : "Test_CBMS", 
#     'password' : "test@321", 
#     'seller_pan' : "999999999",
#     'buyer_pan' : "123456789",
#     'buyer_name':"", 
#     'fiscal_year' : "2077.078", 
#     'invoice_number':"105Ksdf",

#     'invoice_date':"2077.07.06", 
    
#     'total_sales':11300,
#     'taxable_sales_vat':10000, 
#     'vat':1300, 
#     'excisable_amount':0, 
#     'excise':0,
#     'taxable_sales_hst':0,
#     'hst':0, 
#     'amount_for_esf':0, 
#     'esf':0, 
#     'export_sales':0,
#     'tax_exempted_sales':0,
#     'isrealtime':False, 
#     'datetimeclient' : "11.09.2020 08:16:25" 
# }; 
# header = {
#     'Content-Type' : 'application/json'
# }
# res = requests.post(url,headers = header,  data= json.dumps(data))

# print(res.text)