import requests

url = "http://127.0.0.1:5000/clientes"

# Fazendo requisição GET para listar todos os clientes
response = requests.get(url)

print("Status:", response.status_code)

try:
    clientes = response.json()
    print("Clientes cadastrados:")
    for cliente in clientes:
        print(cliente)
except ValueError:
    print("Resposta não é JSON:", response.text)
