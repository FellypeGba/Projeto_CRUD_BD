from flask import Blueprint, request, jsonify
import models.venda as model_venda

venda_bd = Blueprint("venda", __name__)

@venda_bd.route("/venda", methods=["POST"])
def criar_venda():
  data = request.json
  model_venda.inserir(data["dataVenda"], data["statusVenda"], data["codCliente"])
  return jsonify({"message": "Venda criada com sucesso"})

@venda_bd.route("/venda", methods=["GET"])
def listar_vendas():
  clientes = model_venda.listar()
  return jsonify(clientes)


#Opcional: Deleta venda

# @venda_bd.route("/venda/<int:codCliente>", methods=["DELETE"])
# def deletar_venda(codCliente):
#    model_venda.deletar(codCliente)
#    return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})