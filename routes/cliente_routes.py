from flask import Blueprint, request, jsonify
import models.cliente as model_cliente

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes", methods=["POST"])
def criar_cliente():
  data = request.json
  model_cliente.inserir(data["nomeCliente"], data["emailCliente"], data["cpfCliente"], data["dataNasc"], data["telefoneCliente"])
  return jsonify({"message": "Produto criado com sucesso"})

@cliente_bp.route("/clientes", methods=["GET"])
def listar_clientes():
  clientes = model_cliente.listar()
  return jsonify(clientes)

@cliente_bp.route("/clientes/<int:codCliente>", methods=["PUT"])
def atualizar_cliente(codCliente):
    data = request.json
    model_cliente.atualizar(codCliente, data["nomeCliente"], data["emailCliente"], data["telefoneCliente"])
    return jsonify({"message": f"Cliente {codCliente} atualizado com sucesso."})

@cliente_bp.route("/clientes/<int:codCliente>", methods=["DELETE"])
def deletar_cliente(codCliente):
    model_cliente.deletar(codCliente)
    return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})