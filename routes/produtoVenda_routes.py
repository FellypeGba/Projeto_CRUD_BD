from flask import Blueprint, request, jsonify
import models.produtoVenda as model_produtoVenda

produto_venda_bp = Blueprint("produtoVenda", __name__)

@produto_venda_bp.route("/produtos-venda", methods=["POST"])
def inserir_vendaProduto():
  data = request.json
  model_produtoVenda.inserir(data["codVenda"], data["codProd"], data["qtdVenda"], data["valorUnitario"])
  return jsonify({"message": "Produto adicionado a venda com sucesso."})

@produto_venda_bp.route("/produtos-venda/", methods=["GET"])
def listar_produtos_todos():
  produtosVenda = model_produtoVenda.listarTudo()
  return jsonify(produtosVenda)

@produto_venda_bp.route("/produtos-venda/<int:codVenda>", methods=["GET"])
def listar_produtos(codVenda):
  produtosVenda = model_produtoVenda.listar(codVenda)
  return jsonify(produtosVenda)