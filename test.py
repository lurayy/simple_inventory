import requests
import json
import datetime
base_url = 'http://localhost:8000/api/v1/'
# base_url = 'https://simpleim.herokuapp.com/api/v1/'
# base_url = "https://mandala-erp.herokuapp.com/api/v1/"
# base_url = "https://erp.mandalaitsolutions.com/api/v1/"

# data = {
#   'email' : "rabbit.bonex@gmail.com",
#   'code' : '610407',
#   'password' : 'newpass'
# }


# r = requests.post(base_url+'user/password/forget', data= json.dumps(data))
# print(r.text)


# r = requests.post(base_url+'user/password/code/validate', data= json.dumps(data))
# print(r.text)



# r = requests.post(base_url+'user/password/reset', data= json.dumps(data))
# print(r.text)

log_in_url = base_url+'user/auth'

creds = {
    'username':'admin',
    'password':'pass'
}


r = requests.post(log_in_url, data= json.dumps(creds))
# print(r.text)
token = r.json()['token']
r = requests.get(base_url+'user/verify')
csrftoken = r.json()['x-csrftoken']

# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTk1ODQzMTA1LCJlbWFpbCI6IiIsIm9yaWdfaWF0IjoxNTk1ODQzMDQ1fQ.CKglNlJx429keGzEsyc5i0j3VSzWock-BaD26lWmiXQ"
headers = {
    'authorization': 'JWT '+token
}

r = requests.get(base_url+'user/current', headers=headers)
# print(r.text)


# data = {
#   'token' : token
# }

# r = requests.post(base_url+'user/refresh', headers= headers, data = json.dumps(data))
# print(r.text)




# data = {
#   'action' : 'get',
#   'filter' : 'none',
#   'start' : 1,
#   'end' : 2
# }

# r = requests.post(base_url+'inventory/items/get', headers = headers, data= json.dumps(data))
# print(r.text)







# data = {
#   'action' : 'get',
#   'start' : 0,
#   'end' : 25,
#   'filter' : 'multiple',
#   'filters':{
#     'date':None,
#     'user':1,
#     'action' : "LOGIN"
#   }
# }


# r = requests.post(base_url+'user/logs/get', headers = headers, data= json.dumps(data))
# print(r.text)


# # data = {
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


# data = {
#   'action' : 'get'
# }

# sess = requests.post(base_url+'user/roles/get', headers=headers, data=json.dumps(data), verify=False)

# sess = requests.post(base_url+'user/role/valid', headers=headers, data=json.dumps(data), verify=False)
# roles = sess.json()

# res = {
#   'action' : 'add',
#   'name' : 'new_role_man',
#   'description' : "asdfasdfasdfasdf",
#   'role_id' : 1,
#   'powers' : roles['valid_powers'],
#   'values': []
# }

# for i in range(len(roles['valid_powers'])):
#   res['values'].append(True)

# # print(res)

# sess = requests.post(base_url+'user/role/add', headers=headers, data=json.dumps(res), verify=False)
# print(sess.text)

# data = {
#   'action' : 'update',
#   'first_name' : "ss",
#   'last_name': None,
#   'password' : None,
#   'profile' : None
# }

# sess = requests.post(base_url+'user/update', headers=headers, data=json.dumps(data))
# print(sess.text)
# # 

# with open('image.txt', 'r') as fi:
#     x = fi.readline()

# data = {
#   'action' : 'add',
#   'name' : "item123423422",
#   'sales_price' : 2234,
#   'catagory' : 1,
#   'description' : '',
#   'weight' : 2,
#   'average_cost_price' : 2342343,
#   'barcode' : 234323423,
#   'product_images' : [
#     {
#       'category' : "Thumbnail",
#       'base64': x
#     },
#     {
#       'category' : "Product",
#       'base64': x
#     }
#   ]  
# }

# data = {
#   'action' : 'add',
#   'name' : 'ssssss',
#   'weight': 0,
#   'description' : 's',
#   'average_cost_price' : 25,
#   "catagory" : 1,
#   'sales_price' : 25,
#   'weight_unit' : 'kg',
#   'barcode' : 12345234553,
#   'vat_enabled' : True,
#   'product_images' : None
# }
# sess = requests.post(base_url + 'inventory/item/add', headers=headers, data=json.dumps(data))
# print(sess.text)
# data = {
#     'action' : 'get',
#     'filters' : {
#         'date' : {
#             'from' : str(datetime.datetime.now() - datetime.timedelta(days = 90)),
#             'upto' : str(datetime.datetime.now() + datetime.timedelta(days = 90))
#         }
#     }
# }
# print(data)
# sess = requests.post(base_url+'accounting/summary', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#     'action' : 'get',
#     'start' :0,
#     'end' :10,
#     'read' :False
# }

# sess = requests.post(base_url + 'user/notifications/get', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'code' : 'FX522',
#   'action' : 'redeeme',
#   'customer' : 1,
#   'invoice':None,
#   'account':None
# }

# sess = requests.post(base_url+'payment/giftcard/redeeme', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'action':'get',
#   'filter' : 'none',
#   'start' : 0,
#   'end' : 25
# }

# data = {
#   "action":"get",
#   "filter":"multiple",
#   "filters":{
#     "name":"ano",
#     "status":None
#     },
#     "start":0,
#     "end":25
#   }

# sess = requests.post(base_url+'payment/giftcards/categories/get', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'action' : 'get',
#   'filter' : "multiple",
#   'filters' : {
#     'gift_card' : 1,
#     'unique_card' : None,
#     'value': {
#       'from': 0,
#       'upto' : 10,
#     },
#     'invoice' : None,
#     'customer' : None,
#     'date' : None
#   },
#   'start' :0,
#   'end' : 2
# }

# sess = requests.post(base_url+'payment/giftcard/redeeme/history', headers=headers, data=json.dumps(data))
# print(sess.text)


# data = {
#   'action' : 'get'
# }

# data =  {
#   'action' : 'export',
#   'export' : 'excel',
#   'filters' : {
#     'name' : None,
#     'weight' : None,
#     'average_cost_price': {
#       'from' : 0,
#       'upto' : None
#     },
#     'stock': None,
#     'sales_price': None,
#     'category' : None,
#     'sold' : None
#   },
#   'start': 0,
#   'end' : 25,
#   'selected_fields': ["name", "description", "weight", "average_cost_price", "is_active", "catagory", "stock", "sales_price", "sold", "barcode"]
# }
# sess = requests.post(base_url+'inventory/items/export', headers=headers, data=json.dumps(data))
# print(sess.text)

# with open('/mnt/d/file.xls', 'wb') as f:
#   f.write(sess.content)

# data = {
#   "action": "get",
#   "filters": {
#     "date": {
#       "start": "2020-11-27T12:59:48.316Z",
#       "end": "2020-12-01T12:15:19.434Z"
#     },
#   "delta": 1
#   }
# }

# sess = requests.post(base_url+'sales/summary', headers=headers, data=json.dumps(data))
# print(sess.text)

# sess = requests.get(base_url+'sales/settings/get', headers=headers)
# print(sess.text)

# data = {
#   'action' : 'create',
#   'type' : 'barcode',
#   'count' : 2
# }
# sess = requests.post(base_url+'inventory/generate', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'action' : 'import',
#   'csv_file' : "bmFtZSxkZXNjcmlwdGlvbix3ZWlnaHQsY2F0ZWdvcnksc3RvY2ssc2FsZXNfcHJpY2UscHVyY2hhc2VfcHJpY2UsYmFyY29kZSx2YXRfZW5hYmxlZAppdGVtMSxsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDQyMzQyMzIsMQppdGVtMixsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDI1MTMyMDMsMQppdGVtMyxsa2osMCxTbW9rZSwyNSwyNTAsMjAwLDI1MTMyMDIsMQ=="
# }
# sess = requests.post(base_url+'inventory/import', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'action' : 'credit_payment',
#   'credit_id' : 8,
#   'amount' : 283,
#   'method' : 1,
#   'transaction_from' : 'asfd',
#   'transaction_id' :'asd',
#   'bank_name' : 'asdf',
#   'remarks' : 'asdf',
#   'choosen_account' : 7
# }

# sess = requests.post(base_url+'payment/credit/pay', headers=headers, data=json.dumps(data))
# print(sess.text)

# data = {
#   'action' : 'add',
#   'payments' :[
#     {'amount' : 283,
#     'method' : 3,
#     'transaction_from' : 'asfd',
#     'transaction_id' :'asd',
#     'bank_name' : 'asdf',
#     'remarks' : 'asdf',
#     'account' : 8,
#     'invoice' :1
# }],

  
# }

# sess = requests.post(base_url+'payment/add', headers=headers, data=json.dumps(data))
# print(sess.text)


data = {
  'action' : 'export',
  'invoice' : 1
}
sess = requests.post(base_url+'sales/invoice/bill', headers=headers, data=json.dumps(data))
print(sess.text)
