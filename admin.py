import requests
import os

BASE_URL = "http://127.0.0.1:5000"

ENTIDADES = {
  "clientes": ["codcliente", "nomecliente", "emailcliente", "cpfcliente", "datanasc", "telefonecliente"],
  "equipes": ["codequipe","nomeequipe"],
  "pilotos": ["codpiloto", "nomepiloto", "numero", "codequipe"],
  "produtos": ["codprod","nomeprod", "descricao", "qtd", "valor", "ano_temporada", "codequipe", "codpiloto"],
  "vendas": ["codvenda", "datavenda", "valorvenda", "statusvenda", "codcliente"],
  "produtos-venda": ["nomeprod" ,"codvenda", "codprod", "qtdvenda", "valorunitario"]
}

ENTIDADES_EDITAR = {
  "clientes": ["nomecliente", "emailcliente", "telefonecliente"],
  "equipes": ["nomeequipe"],
  "pilotos": ["nomepiloto", "numero", "codequipe"],
  "produtos": ["nomeprod", "descricao", "qtd", "valor", "ano_temporada", "codequipe", "codpiloto"],
}

ENTIDADES_BUSCAR = {
  "clientes": "nomecliente",
  "equipes": "nomeequipe",
  "pilotos": "nomepiloto",
  "produtos": "nomeprod"
}

def limparTela():
  os.system('cls' if os.name == 'nt' else 'clear')

def handle_request(method, url, **kwargs):
  try:
    response = requests.request(method, url, **kwargs)
    if response.status_code == 204:
      return True, {"success": "Operação realizada com sucesso."}
    response.raise_for_status()
    return True, response.json()
  except Exception as e:
    return False, f"Erro ao realizar a operação. Tente novamente."

def menu():
  limparTela()
  print("=== ADMINISTRAÇÃO F1 STORE ===\n")
  print("1. Gerenciar Clientes")
  print("2. Gerenciar Equipes")
  print("3. Gerenciar Pilotos")
  print("4. Gerenciar Produtos")
  print("5. Gerenciar Vendas")
  print("6. Gerenciar Produtos da Venda")
  print("0. Sair")
  return input("Escolha a entidade: ")

def operacoes(entidade):
  limparTela()
  print(f"\n=== GERENCIAR {entidade.upper()} ===\n")
  print("1. Listar")
  print("2. Pesquisar por nome")
  print("3. Inserir")
  print("4. Atualizar")
  print("5. Deletar")
  print("0. Voltar")
  return input("Escolha a operação: ")

def operacoesSimples(entidade):
  limparTela()
  print(f"\n=== GERENCIAR {entidade.upper()} ===\n")
  print("1. Listar")
  print("2. Inserir")
  if (entidade == "vendas"): print("3. Gerar relatório")
  print("0. Voltar")
  return input("Escolha a operação: ")

def mostrarTabela(dados, colunas):
  if not isinstance(dados, list): dados = [dados]
  if not dados:
    print("Nenhum registro encontrado.")
    return

  larguras = {key: len(str(key)) for key in colunas}
  for item in dados:
    for key, value in item.items():
      if key in larguras:
        larguras[key] = max(larguras[key], len(str(value)))

  cabecalho = " | ".join(key.ljust(larguras[key]) for key in colunas)
  print(cabecalho)
  print("-" * len(cabecalho))

  for item in dados:
    linha_str = " | ".join(str(item.get(key, 'N/A')).ljust(larguras[key]) for key in colunas)
    print(linha_str)

def listar(entidade):
  sucesso, dados = handle_request("GET", f"{BASE_URL}/{entidade}")
  if sucesso and dados:
    mostrarTabela(dados, ENTIDADES[entidade])

def inserir(entidade):
  dados = {}
  for campo in ENTIDADES[entidade][1:]:
    dados[campo] = input(f"{campo}: ")
  sucesso, resposta = handle_request("POST", f"{BASE_URL}/{entidade}", json=dados)
  if sucesso:
    print(f"\n{resposta.get('message', 'Registro inserido.')}")

def atualizar(entidade):
  cod = input(f"\nID do(a) {entidade[:-1]} a atualizar: ")
  dados = {}
  for campo in ENTIDADES_EDITAR[entidade]:
    valor = input(f"Novo {campo}: ")
    if valor: 
      dados[campo] = valor

  if dados:
    sucesso, resposta = handle_request("PUT", f"{BASE_URL}/{entidade}/{cod}", json=dados)
    if sucesso:
      print(f"\n{resposta.get('message', 'Registro atualizado.')}")
    else: print("\nNão foi possível atualizar.")
  else: print("\nNenhum dado foi alterado.")

def deletar(entidade):
  cod = str(input(f"\nID do(a) {entidade[:-1]} a excluir: "))
  sucesso, resposta = handle_request("DELETE", f"{BASE_URL}/{entidade}/{cod}")
  if sucesso:
    print(f"\n{resposta.get('message', 'Registro deletado.')}")

def buscar(entidade):
  nome = input(f"\nNome do(a) {entidade[:-1]} para buscar: ")
  sucesso, dados = handle_request("GET", f"{BASE_URL}/{entidade}/busca?nome={nome}")
  if sucesso and dados:
    mostrarTabela(dados, ENTIDADES[entidade])

def gerar_relatorio(entidade):
  print("--- RELATÓRIO GERAL DE VENDAS ---")
  sucesso, relatorio = handle_request("GET", f"{BASE_URL}/vendas/relatorio")
  if relatorio:
    print(f"Quantidade de vendas: {relatorio['total_vendas']}")
    print(f"Valor total das vendas: R$ {float(relatorio['valor_total']):.2f}")
    print(f"Valor médio por venda: R$ {float(relatorio['valor_medio']):.2f}")
    print(f"Maior venda: R$ {float(relatorio['maior_venda']):.2f}")
    print(f"Menor venda: R$ {float(relatorio['menor_venda']):.2f}")
  
def crudSimples(entidade):
  while True:
    limparTela()
    op = operacoesSimples(entidade)
    print()
    if op == "1": 
      listar(entidade)
      input("\nPressione Enter para continuar...")

    elif op == "2":  # Inserir
      inserir(entidade)
      input("\nPressione Enter para continuar...")

    elif op == "3" and entidade == "vendas":
      gerar_relatorio(entidade)
      input("\nPressione Enter para continuar...")

    elif op == "0":
      break

    else:
      print("Erro de Seleção de Operação")


def crud(entidade):
  while True:
    op = operacoes(entidade)
    print()
    if op == "1": 
      listar(entidade)
      input("\nPressione Enter para continuar...")

    if op == "2": 
      buscar(entidade)
      input("\nPressione Enter para continuar...")

    elif op == "3":  # Inserir
      inserir(entidade)
      input("\nPressione Enter para continuar...")

    elif op == "4":  # Atualizar
     listar(entidade)
     atualizar(entidade)
     input("\nPressione Enter para continuar...")

    elif op == "5":  # Deletar
      listar(entidade)
      deletar(entidade)
      input("\nPressione Enter para continuar...")

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
      print("\nSaindo... Até logo!")
      break
    else:
      print("Opção inválida!")

if __name__ == "__main__":
    main()