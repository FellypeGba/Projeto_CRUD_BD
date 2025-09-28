import requests
import os
import json
from datetime import datetime

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

def cadastrarCliente():
  limparTela()
  print("--- Cadastro de Novo Cliente ---")
  dados_cliente = {
    "nomecliente": input("Nome completo: "),
    "emailcliente": input("Email: "),
    "cpfcliente": input("CPF (apenas números): "),
    "datanasc": input("Data de Nascimento: "),
    "telefonecliente": input("Telefone (opcional): "),
    "timeamado": input("Time do coração: "),
    "onepiece": input("Assiste One Piece (S/N): ").strip().lower() in ['sim', 's'],
    "cidade": input("Cidade: ")
  }
  
  sucesso, resposta = handle_request("POST", f"{BASE_URL}/clientes", json=dados_cliente)
  print(f"\n{resposta.get('message') or resposta}")
  input("\nPressione Enter para continuar...")
  return sucesso

#Função para o cliente checar os dados cadastrados dele:
def mostrarCliente(cliente):
  print("\n\nExibindo Informações Cadastradas")
  sucesso, dados = handle_request("GET", f"{BASE_URL}/clientes/{cliente['codcliente']}")
  colunas_cliente = [
    "cpfcliente",
    "nomecliente",
    "emailcliente",
    "datanasc",
    "telefonecliente",
    "timeamado",
    "onepiece",
    "cidade"
  ]
  if sucesso and dados:
    mostrarTabela(dados, colunas_cliente)

  input("\nPressione Enter para continuar...")

def loginCliente():
  limparTela()
  print("--- Login ---")
  email = input("Digite seu email para identificação: ")

  sucesso, cliente = handle_request("GET", f"{BASE_URL}/clientes/busca?email={email}")

  if sucesso:
    print(f"Bem-vindo(a), {cliente.get('nomecliente')}!")
    input("Pressione Enter para continuar...")
    return cliente
  print("Cliente não encontrado.")
  input("Pressione Enter para continuar...")

def filtrarProdutos():
  print("\n--- Consulta de Produtos ---")

  while True:
    nomeProd = input("\nDigite o nome para filtar (0 para sair): ")
    if nomeProd == '0':
      break;
    sucesso, produtos = handle_request("GET", f"{BASE_URL}/produtos/busca?nome={nomeProd}")
    if sucesso and produtos:
      mostrarTabela(produtos, ["codprod", "nomeprod", "descricao", "valor", "qtd", "categoria", "fabricante"])
    elif sucesso and not produtos:
      print("\nNenhum produto encontrado com este termo.")
    else:
      print(f"\nErro ao buscar produtos: {produtos}")

def listarProdutos():
  sucesso, produtos = handle_request("GET", f"{BASE_URL}/produtos")
  if sucesso:
    mostrarTabela(produtos, ["codprod", "nomeprod", "descricao", "valor", "qtd", "categoria", "fabricante"])
    return produtos
  else:
    print(f"\nErro ao buscar produtos: {produtos}")
    return []

def escolherVendedor():
  sucesso, vendedores = handle_request("GET", f"{BASE_URL}/vendedores")
  if not sucesso or not vendedores:
    print("Nenhum vendedor disponível.")
    return None
  print("\n--- Vendedores Disponíveis ---")
  mostrarTabela(vendedores, ["codvendedor", "nomevendedor", "emailvendedor"])
  while True:
    cod = input("Digite o código do vendedor para esta venda: ")
    if any(str(v["codvendedor"]) == cod for v in vendedores):
      return int(cod)
    print("Código inválido. Tente novamente.")

def realizarCompra(cliente):
  limparTela()
  print("--- Vitrine de Produtos ---")
  produtosDisponiveis = listarProdutos()
  if not produtosDisponiveis:
    input("\nNenhum produto disponível. Pressione Enter para voltar.")
    return

  carrinho = []
  totalVenda = 0.0

  while True:
    codProd = input("\nDigite o ID do produto para adicionar ao carrinho (ou '0' para finalizar): ")
    if codProd == "0":
      break
    
    produtoSelecionado = next((p for p in produtosDisponiveis if str(p.get("codprod")) == codProd), None)

    if not produtoSelecionado:
      print("ID de produto inválido.")
      continue
    
    try:
      qtd = int(input(f"Quantidade de '{produtoSelecionado['nomeprod']}': "))
      if qtd <= 0 or qtd > produtoSelecionado['qtd']:
        print(f"Quantidade inválida. Disponível: {produtoSelecionado['qtd']}")
        continue
    except ValueError:
      print("Quantidade deve ser um número.")
      continue
    
    carrinho.append({
      "codprod": produtoSelecionado["codprod"],
      "nomeprod": produtoSelecionado["nomeprod"],
      "qtdvenda": qtd,
      "valorunitario": float(produtoSelecionado["valor"])
    })
    totalVenda += qtd * float(produtoSelecionado["valor"])
    print(f"'{produtoSelecionado['nomeprod']}' adicionado. Total parcial: R$ {totalVenda:.2f}")

  if not carrinho:
    print("\nNenhum produto no carrinho. Compra cancelada.")
    input("\nPressione Enter para continuar...")
    return
  
  # Finalizar a venda
  print("\n--- Finalizando Compra ---")
  confirmacao = input(f"O total da sua compra é R$ {totalVenda:.2f}. Confirmar compra? (S/N): ")
  if confirmacao.lower() != 's':
    print("Compra cancelada.")
    input("\nPressione Enter para continuar...")
    return
  
  # Cria a venda 
  codVendedor = escolherVendedor()
  if not codVendedor:
    print("Compra cancelada por falta de vendedor.")
    input("\nPressione Enter para continuar...")
    return

  dadosVenda = {
    "datavenda": datetime.now().isoformat(),
    "valorvenda": totalVenda,
    "codstatus": 1,  # 1 = Processando (ajuste conforme necessário)
    "codcliente": cliente["codcliente"],
    "codvendedor": codVendedor
  }
  sucessoVenda, respVenda = handle_request("POST", f"{BASE_URL}/vendas", json=dadosVenda)

  if not sucessoVenda:
    print(f"Erro ao criar a venda: {respVenda}")
    input("\nPressione Enter para continuar...")
    return
  
  codVenda = respVenda.get("codVenda")

  # Adicionando os produtos a venda
  print("Adicionando produtos ao pedido...")
  erros = 0
  for item in carrinho:
    dadosProdutoVenda = {
      "codvenda": codVenda,
      "codprod": item["codprod"],
      "qtdvenda": item["qtdvenda"],
      "valorunitario": item["valorunitario"]
    }
    sucessoItem, respItem = handle_request("POST", f"{BASE_URL}/produtos-venda", json=dadosProdutoVenda)
    if not sucessoItem:
      print(f"Erro ao adicionar o produto '{item['nomeProd']}': {respItem}")
      erros += 1
  
  if erros == 0:
      print("\nCompra realizada com sucesso!")
  else:
      print(f"\nCompra finalizada com {erros} erros ao adicionar produtos.")
  
  input("\nPressione Enter para continuar...")

def verCompras(cliente):
  limparTela()
  print("--- Minhas Compras ---")
  
  sucesso, vendas = handle_request("GET", f"{BASE_URL}/vendas")
  minhasVendas = [v for v in vendas if v.get("codcliente") == cliente["codcliente"]]
  
  if not minhasVendas:
    print("Você ainda não fez nenhuma compra.")
  else:
    mostrarTabela(minhasVendas, ["codvenda", "datavenda", "valorvenda", "codstatus", "codvendedor"])
    
    codVenda_detalhes = input("\nDigite o ID da venda para ver os detalhes (ou Enter para voltar): ")
    if codVenda_detalhes.isdigit():
      sucessoDetalhe, detalhes = handle_request("GET", f"{BASE_URL}/produtos-venda/{codVenda_detalhes}")
      if sucessoDetalhe:
        print(f"\n--- Detalhes da Venda {codVenda_detalhes} ---")
        mostrarTabela(detalhes, ["nomeprod", "qtdvenda", "valorunitario"]) 
      else:
        print(f"Erro ao buscar detalhes: {detalhes}")

  input("\nPressione Enter para continuar...")

def menuCliente(cliente):
  while True:
    limparTela()
    print(f"Olá, {cliente['nomecliente']}! O que deseja fazer?")
    print("1. Ver todos os produtos")
    print("2. Buscar produto")
    print("3. Realizar nova compra")
    print("4. Ver minhas compras")
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
      realizarCompra(cliente)
    elif escolha == "4":
      verCompras(cliente)
    elif escolha == "5":
      mostrarCliente(cliente)
    elif escolha == "0":
      break
    else:
      print("Opção inválida!")

def main():
  cliente = None
  while True:
    limparTela()
    print("--- BEM-VINDO À F1 STORE ---")
    print("1. Login")
    print("2. Cadastrar")
    print("0. Sair")
    
    escolha = input("Sua escolha: ")

    if escolha == "1":
      cliente = loginCliente()
      if cliente:
        menuCliente(cliente)
    elif escolha == "2":
      cadastrarCliente()
    elif escolha == "0":
      print("\nSaindo... Até logo!")
      break
    else:
      print("Opção inválida!")

if __name__ == "__main__":
  main()