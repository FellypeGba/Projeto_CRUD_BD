from flask import Blueprint, request, jsonify
import models.venda as model_venda

venda_bp = Blueprint("venda", __name__)

@venda_bp.route("/vendas", methods=["POST"])
def criar_venda():
  data = request.json
  model_venda.criar(data["dataVenda"], data["valorVenda"], data["statusVenda"], data["codCliente"])
  return jsonify({"message": "Venda criada com sucesso"})

@venda_bp.route("/vendas", methods=["GET"])
def listar_vendas():
  vendas = model_venda.listar()
  return jsonify(vendas)


#Opcional: Deletar venda

# @venda_bd.route("/venda/<int:codCliente>", methods=["DELETE"])
# def deletar_venda(codCliente):
#    model_venda.deletar(codCliente)
#    return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})