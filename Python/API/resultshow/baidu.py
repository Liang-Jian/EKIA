

import requests
from requests import Request, Session

for i in range (0,2):
    s=requests.Session()
    r1= s.get('https://www.baidu.com/', verify=False)
    print(r1)