import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld/adam/22")
print(response.json())