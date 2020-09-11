# import requests
# import json
# # base_url = "https://erp.mandalaitsolutions.com/api/v1/"
# base_url = 'http://localhost:8000/api/v1/'

# def login():    
#     creds = {
#         "username":"admin",
#         "password":"pass"
#     }
#     log_in_url = base_url+"user/auth"

#     r = requests.post(log_in_url, data=json.dumps(creds))
#     # print(r.text)
#     token = r.json()["token"]

#     # print(token)

#     headers = {
#         "authorization":'JWT '+token,
#     }

#     sess = requests.get(base_url+"user/current", headers=headers)
#     # print(sess.text)
#     return headers

# def call(headers, data, url):
#     sess = requests.post(base_url+url, headers=headers, data=json.dumps(data))
#     print(sess.text)

# if __name__ == "__main__":
#     headers = login()

#     data = {
#         'action' : 'get',
#         'filter' : 'barcode',
#         'barcode' :"9",
#         'filters' : {
#             'is_applied_name': True,
#             'exact_name' : False,
#             'name' : 'no',
#             'is_applied_weight_from' : None,
#             'is_applied_weight_upto' : None,
#             'is_applied_average_cost_price_from' : None,
#             'is_applied_average_cost_price_upto' : None,
#             'is_applied_stock_upto' : None,
#             'is_applied_stock_from' : None,
#             'is_applied_sold_upto' : None,
#             'is_applied_sold_from' : None,
#             'is_applied_sales_price_from' : None,
#             'is_applied_sales_price_upto' : None,
#             'is_applied_category' : None
#         },    
#         'start' : 0,
#         'end' : 25
#     }
#     url = 'inventory/items/get'
#     call(headers, data, url)
import datetime

url = "http://103.1.92.174:9050/api/bill"
from bikram import samwat
import json
import requests
# data = {
#     'username' : "Test_CBMS",
#     'password' : "test@321",
#     'seller_pan' : '89415',
#     'buyer_pan' : '84512',
#     'fiscal_year' : "2077.2078",
#     'buyer_name' : 'test man',
#     'invoice_number' : "8465132",
#     'invoice_date' : "2074.06.25",
#     'total_sales' : 1130,
#     'taxable_sales_vat' : 1000 ,
#     'vat' : 130,
#     'excisable_amount' :0 ,
#     'excise' : 0,
#     'taxable_sales_hst' : 0,
#     'hst' : 0,
#     'amount_for_esf' : 0,
#     'esf' : 0,
#     'export_sales' : 0,
#     'tax_exmpted_sales' :0 ,
#     'isrealtime' : True,
#     'datetimeClient' :  str(datetime.datetime.now()),
# }

data  = {
    'username' : "Test_CBMS", 
    'password' : "test@321", 
    'seller_pan' : "999999999",
    'buyer_pan' : "123456789",
    'buyer_name':"", 
    'fiscal_year' : "2077.078", 
    'invoice_number':"105KKL sdf",
    'invoice_date':"2077.07.06", 
    'total_sales':1130,
    'taxable_sales_vat':1000, 
    'vat':130, 
    'excisable_amount':0, 
    'excise':0,
    'taxable_sales_hst':0,
    'hst':0, 
    'amount_for_esf':0, 
    'esf':0, 
    'export_sales':0,
    'tax_exempted_sales':0,
    'isrealtime':False, 
    'datetimeclient' : "11.09.2020 08:16:25" 
}; 
header = {
    'Content-Type' : 'application/json'
}
res = requests.post(url,headers = header,  data= json.dumps(data))

print(res.text)