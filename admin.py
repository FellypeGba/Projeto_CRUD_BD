import requests

BASE_URL = "http://127.0.0.1:5000" #URL da aplicação

ENTIDADES = {
    "clientes": ["nomecliente", "emailcliente", "cpfCliente", "datanasc", "telefonecliente"],
    "equipes": ["nomeequipe"],
    "pilotos": ["nomepiloto", "numero", "codequipe"],
    "produtos": ["nomeprod", "descricao", "qtd", "valor", "ano_temporada", "codequipe", "codpiloto"],
    "vendas": ["valorvenda", "statusvenda", "codcliente"],
    "produtos-venda": ["codvenda", "codprod", "qtdvenda", "valorunitario"]
}

ENTIDADES_EDITAR = {
    "clientes": ["nomecliente", "emailcliente", "telefonecliente"],
    "equipes": ["nomeequipe"],
    "pilotos": ["nomepiloto", "numero", "codequipe"],
    "produtos": ["nomeprod", "descricao", "qtd", "valor", "ano_temporada", "codequipe", "codpiloto"],
    "vendas": ["valorvenda", "statusvenda", "codcliente"],
    "produtos-venda": ["codvenda", "codprod", "qtdvenda", "valorunitario"]
}


def menu():
    print("\n=== ADMIN CRUD ===")
    print("1. Cliente")
    print("2. Equipe")
    print("3. Piloto")
    print("4. Produto")
    print("5. Venda")
    print("6. ProdutoVenda")
    print("0. Sair")
    return input("Escolha a entidade: ")

def operacoes(entidade):
    print(f"\n=== {entidade.upper()} ===")
    print("1. Listar")
    print("2. Inserir")
    print("3. Atualizar")
    print("4. Deletar")
    print("0. Voltar")
    return input("Escolha a operação: ")

def operacoesSimples(entidade):
    print(f"\n=== {entidade.upper()} ===")
    print("1. Listar")
    print("2. Inserir")
    return input("Escolha a operação: ")

#mostra a entidade de forma mais apresentável
def mostrarEntidade(lista):
    for elemento in lista:
        print(elemento)


def crudSimples(entidade):
    while True:
        op = operacoesSimples(entidade)
        if op == "1":  # Listar
            r = requests.get(f"{BASE_URL}/{entidade}")
            retorno = (r.json())
            mostrarEntidade(retorno)

        elif op == "2":  # Inserir
            dados = {}
            for campo in ENTIDADES[entidade]:
                dados[campo] = input(f"{campo}: ")
            r = requests.post(f"{BASE_URL}/{entidade}", json=dados)
            print(r.json())

        elif op == "0":
            break

        else:
            print("Erro de Seleção de Operação")


def crud(entidade):
    while True:
        op = operacoes(entidade)
        if op == "1":  # Listar
            r = requests.get(f"{BASE_URL}/{entidade}")
            retorno = (r.json())
            mostrarEntidade(retorno)

        elif op == "2":  # Inserir
            dados = {}
            for campo in ENTIDADES[entidade]:
                dados[campo] = input(f"{campo}: ")
            r = requests.post(f"{BASE_URL}/{entidade}", json=dados)
            print(r.json())

        elif op == "3":  # Atualizar
            cod = input(f"ID do(a) {entidade[:-1]} a atualizar: ")
            dados = {}
            for campo in ENTIDADES_EDITAR[entidade]:
                dados[campo] = input(f"Novo {campo}: ")
            r = requests.put(f"{BASE_URL}/{entidade}/{cod}", json=dados)
            print(r.json())

        elif op == "4":  # Deletar
            cod = input(f"ID do(a) {entidade[:-1]} a excluir: ")
            r = requests.delete(f"{BASE_URL}/{entidade}/{cod}")
            print(r.json())

        elif op == "0":
            break

        else:
            print("Erro de Seleção de Operação")


def main():
    while True:
        escolha = menu()
        if escolha == "1":
            crud("clientes")
        elif escolha == "2":
            crud("equipes")
        elif escolha == "3":
            crud("pilotos")
        elif escolha == "4":
            crud("produtos")
        elif escolha == "5":
            crudSimples("vendas")
        elif escolha == "6":
            crudSimples("produtos-venda")
        elif escolha == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
