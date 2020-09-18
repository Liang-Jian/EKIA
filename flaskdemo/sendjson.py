import requests

data = {"username":"joker","password":"fuck"}

r = requests.post(url="http://118.25.78.198:5000/b",json=data)
print(r.text)
