# URL= 'http://127.0.0.1:8000/api/friend-request/'
URL= 'http://127.0.0.1:8000/api/friend-request/1/accept/'

import requests


data = {
    'to_user':7
}

# import pdb;pdb.set_trace()

# r = requests.get(url=URL, data=data)
r = requests.get(url=URL)

