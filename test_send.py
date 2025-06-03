import requests

url = "http://localhost:5000/"
payload = {
    "phone": "5586988673435",
    "buttonResponse": "Não tenho interesse"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.text)
