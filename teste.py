import requests

url = "http://127.0.0.1:5000/clientes"

data = {
    "nomecliente": "Maria Souza",
    "emailcliente": "maria@example.com",
    "cpf": "12345678901",
    "datanasc": "1990-05-20",
    "telefonecliente": "85999999999"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Resposta:", response.json())
