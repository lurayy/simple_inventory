import requests
import json

# base_url = 'http://localhost:8000/api/v1/'
base_url = "https://simpleim.herokuapp.com/api/v1/"
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
print(r.text)
token = r.json()['token']
r = requests.get(base_url+'user/verify')
csrftoken = r.json()['x-csrftoken']

headers = {
    'authorization': 'JWT '+token,
    'x-csrftoken': csrftoken
}

r = requests.get(base_url+'user/current', headers=headers)
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
#   'action': 'get',
#   'filter'  : 'none',
#   'start' : 0,
#   'end': 25
# }
# sess = requests.post(base_url + 'inventory/items/get', headers=headers, data=json.dumps(data))
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

data = {
  'action':'get',
  'filter' : 'none',
  'start' : 0,
  'end' : 25
}
sess = requests.post(base_url+'payment/giftcards/categories/get', headers=headers, data=json.dumps(data))
print(sess.text)

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
