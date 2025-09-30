import requests
import os
import json
from datetime import datetime
from urllib.parse import urlencode

BASE_URL = "http://127.0.0.1:5000"

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


#Função para o vendedor checar os dados cadastrados dele:
def mostrarVendedor(vendedor):
  print("\n\nExibindo Informações Cadastradas...\n")
  sucesso, dados = handle_request("GET", f"{BASE_URL}/vendedores/{vendedor['codvendedor']}")
  colunas_vendedor = [
    "nomevendedor",
    "emailvendedor",
    "datanasc",
    "telefonevendedor",
  ]
  if sucesso and dados:
    mostrarTabela(dados, colunas_vendedor)

  input("\nPressione Enter para continuar...")

def loginVendedor():
  limparTela()
  print("--- Login ---")
  email = input("Digite seu email para identificação: ")

  sucesso, vendedor = handle_request("GET", f"{BASE_URL}/vendedores/busca?email={email}")

  if sucesso:
    print(f"Bem-vindo(a), {vendedor.get('nomevendedor')}!")
    input("Pressione Enter para continuar...")
    return vendedor
  print("Vendedor não encontrado.")
  input("Pressione Enter para continuar...")

def filtrarProdutos():
  limparTela()
  print("--- Consulta de Produtos ---")
  print("Deixe o campo em branco e pressione Enter para não usar um filtro.")

  nome = input("\nNome do produto: ")
  categoria = input("Categoria: ")
  preco_min = input("Preço mínimo (ex: 50.00): ")
  preco_max = input("Preço máximo (ex: 200.00): ")
  fabricadoMari = input("Apenas fabricados em Mari? (S/N): ")
  estoque_baixo = input("Verificar produtos com estoque baixo? (S/N): ")

  params = {}
  if nome:
    params['nome'] = nome
  if categoria:
    params['categoria'] = categoria
  if preco_min:
    params['preco_min'] = preco_min
  if preco_max:
    params['preco_max'] = preco_max
  if fabricadoMari.strip().lower() == 's':
    params['mari'] = 'true'
  if estoque_baixo.strip().lower() == 's':
    params['estoque_baixo'] = 'true'

  if not params:
    print("\nNenhum filtro aplicado. Buscando todos os produtos...")
  
  query_string = urlencode(params)
  url_final = f"{BASE_URL}/produtos/busca?{query_string}"
  print("\nBuscando...")
  sucesso, produtos = handle_request("GET", url_final)

  if sucesso and produtos:
    mostrarTabela(produtos, ["codprod", "nomeprod", "descricao", "valor", "qtd", "categoria", "fabricante", "cidadefabricante"])
  elif sucesso and not produtos:
    print("\nNenhum produto encontrado com os filtros aplicados.")
  else:
    print(f"\nErro ao buscar produtos: {produtos}")

  input("\nPressione Enter para continuar...")

def listarProdutos():
  sucesso, produtos = handle_request("GET", f"{BASE_URL}/produtos")
  if sucesso:
    mostrarTabela(produtos, ["codprod", "nomeprod", "descricao", "valor", "qtd", "categoria", "fabricante"])
    return produtos
  else:
    print(f"\nErro ao buscar produtos: {produtos}")
    return []
  
def gerarRelatorio(vendedor):
  limparTela()
  print("\n--- Relatório Mensal de Vendas ---\n")
  
  ano = input("Digite o ano (ex: 2025): ")
  mes = input("Digite o mês (ex: 9): ")

  if not ano.isdigit() or not mes.isdigit():
    print("\nAno e mês devem ser valores numéricos.")
    input("\nPressione Enter para continuar...")
    return

  codVendedor = vendedor['codvendedor']
  url = f"{BASE_URL}/vendas/relatorio/vendedor/{codVendedor}?ano={ano}&mes={mes}"
  sucesso, relatorio = handle_request("GET", url)

  if sucesso and relatorio:
    print(f"\n--- Relatório de Vendas de {mes}/{ano} ---\n")
    colunas_relatorio = [
        "total_vendas", 
        "valor_total", 
        "valor_medio", 
        "maior_venda", 
        "menor_venda"
    ]
    mostrarTabela([relatorio], colunas_relatorio)
  else:
    print(f"\nNão foi possível gerar o relatório: {relatorio}")

  input("\nPressione Enter para continuar...")

def verVendas(vendedor):
  limparTela()
  print("--- Minhas Vendas ---")
  
  sucesso, vendas = handle_request("GET", f"{BASE_URL}/vendas")
  minhasVendas = [v for v in vendas if v.get("codvendedor") == vendedor["codvendedor"]]
  
  if not minhasVendas:
    print("Você ainda não fez nenhuma venda.")
  else:
    mostrarTabela(minhasVendas, ["codvenda", "datavenda", "valorvenda", "nomepagamento", "statuspagamento", "nomecliente"])
    
    codVenda_detalhes = input("\nDigite o ID da venda para ver os detalhes (ou Enter para voltar): ")
    if codVenda_detalhes.isdigit():
      sucessoDetalhe, detalhes = handle_request("GET", f"{BASE_URL}/produtos-venda/{codVenda_detalhes}")
      if sucessoDetalhe:
        print(f"\n--- Detalhes da Venda {codVenda_detalhes} ---")
        mostrarTabela(detalhes, ["nomeprod", "qtdvenda", "valorunitario"]) 
      else:
        print(f"Erro ao buscar detalhes: {detalhes}")

  input("\nPressione Enter para continuar...")

def menuCliente(vendedor):
  while True:
    limparTela()
    print(f"Olá, {vendedor['nomevendedor']}! O que deseja fazer?")
    print("1. Ver todos os produtos")
    print("2. Buscar produto")
    print("3. Ver minhas vendas")
    print("4. Ver retaltório de vendas")
    print("5. Ver minhas informações")
    print("0. Sair")

    escolha = input("Sua escolha: ")
    if escolha == "1":
      limparTela()
      print("--- Vitrine de Produtos ---")
      listarProdutos()
      input("\nPressione Enter para voltar...")
    elif escolha == "2":
      filtrarProdutos()
    elif escolha == "3":
      verVendas(vendedor)
    elif escolha == "4":
      gerarRelatorio(vendedor)
    elif escolha == "5":
      mostrarVendedor(vendedor)
    elif escolha == "0":
      break
    else:
      print("Opção inválida!")

def main():
  vendedor = None
  while True:
    limparTela()
    print("--- BEM-VINDO À F1 STORE ---")
    print("1. Login")
    print("0. Sair")
    
    escolha = input("Sua escolha: ")

    if escolha == "1":
      vendedor = loginVendedor()
      if vendedor:
        menuCliente(vendedor)
    elif escolha == "0":
      print("\nSaindo... Até logo!")
      break
    else:
      print("Opção inválida!")

if __name__ == "__main__":
  main()