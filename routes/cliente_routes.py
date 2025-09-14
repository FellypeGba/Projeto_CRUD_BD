from flask import Blueprint, request, jsonify
import models.cliente as model_cliente
import psycopg2.extras

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes", methods=["POST"])
def criar_cliente():
  try:
    data = request.json
    model_cliente.inserir(data["nomecliente"], data["emailcliente"], data["cpfcliente"], data["datanasc"], data["telefonecliente"])
    return jsonify({"message": "Cliente criado com sucesso"})
  
  except psycopg2.errors.UniqueViolation as e:
    errorMessage = "Violação de dado único."
    if 'emailcliente' in str(e).lower(): errorMessage = "Já existe um cadastro com este email."
    elif 'cpfcliente' in str(e).lower(): errorMessage = "Já existe um cadastro com este CPF."
    return({"message": errorMessage})
  except Exception as e:
    return jsonify({"erro": f"Ocorreu um erro inesperado. Tente novamente."})

@cliente_bp.route("/clientes", methods=["GET"])
def listar_clientes():
  clientes = model_cliente.listar()
  return jsonify(clientes)

@cliente_bp.route("/clientes/<int:codCliente>", methods=["PUT"])
def atualizar_cliente(codCliente):
  data = request.json
  print("Dados recebidos: ", data)
  model_cliente.atualizar(codCliente, data["nomecliente"], data["emailcliente"], data["telefonecliente"])
  return jsonify({"message": f"Cliente {codCliente} atualizado com sucesso."})

@cliente_bp.route("/clientes/<int:codCliente>", methods=["DELETE"])
def deletar_cliente(codCliente):
  model_cliente.deletar(codCliente)
  return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})

@cliente_bp.route("/clientes/<int:codCliente>", methods=["GET"])
def exibir_cliente(codCliente):
  cliente = model_cliente.exibirUm(codCliente)
  if cliente:
    return jsonify(cliente)
  else:
    return jsonify({"erro": "Cliente não encontrado"})

@cliente_bp.route("/clientes/busca", methods=["GET"])
def buscar_clientes():
  email = request.args.get('email')
  nome = request.args.get('nome')

  if email:
    cliente = model_cliente.buscaEmail(email)
    if cliente:
      return jsonify(cliente)
    else:
      return jsonify({"erro": "Cliente com este email não foi encontrado"})

  elif nome:
    clientes = model_cliente.filtrarNome(nome)
    return jsonify(clientes)
  