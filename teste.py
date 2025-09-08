import requests

#conectando com a aplicação
url = "http://127.0.0.1:5000/clientes"

#preparando a instância no formato json
data = {
    "nomecliente": "Maria Souza",
    "emailcliente": "mariasouza@example.com",
    "cpf": "12345678901",
    "datanasc": "1990-05-20",
    "telefonecliente": "85999999999"
}

#fazendo a requsição para a inserção
response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Resposta:", response.json())
