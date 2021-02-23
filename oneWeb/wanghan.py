
import os,requests,json
from collections import OrderedDict

url = 'http://127.0.0.1:8000/dao/testcase/globalVariable_exts/?globalId=1'
data = {"username":'wanghan','password':'123456q'}
data2 = {'key':'name','value':'wanghan','globalId':1}
a = {'msg': '登陆成功', 'username': 'wanghan', 'token':
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IndhbmdoYW4iLCJleHAiOjE2MTI4NTI3NjYsImVtYWlsIjoiMTU1OTI4NDA1MEBxcS5jb20iLCJvcmlnX2lhdCI6MTYxMjI0Nzk2Nn0.uV8YuN0-_Fd9t8X68hWYKtSH0m_2NF7-J9L75k4kuQE'}
headers = {'Content-Type': 'application/json',
            'Accept': 'application/json',
           'super-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IndhbmdoYW4iLCJleHAiOjE2MTI4NTYyNTYsImVtYWlsIjoiMTU1OTI4NDA1MEBxcS5jb20iLCJvcmlnX2lhdCI6MTYxMjI1MTQ1Nn0.6g11vCu8Nsk-RzP8KA4d3cJH__ZBtxhBCGaLR6rNpao'}


r = requests.get(url,json=data2,headers=headers)
print(r.text)