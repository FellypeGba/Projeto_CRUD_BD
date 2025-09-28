from flask import Blueprint, request, jsonify
import models.produto as model_produto

produto_bp = Blueprint("produto", __name__)

@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
  data = request.json
  model_produto.inserir(data["nomeprod"], data["descricao"], data["qtd"], data["valor"], data["ano_temporada"], data["categoria"], data["codequipe"], data["codpiloto"], data["codfabricante"])
  return jsonify({"message": "Produto criado com sucesso"})

@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
  produtos = model_produto.listar()
  return jsonify(produtos)

@produto_bp.route("/produtos/<int:codProd>", methods=["PUT"])
def atualizar_produto(codProd):
  data = request.json
  model_produto.atualizar(codProd, data["nomeprod"], data["descricao"], data["qtd"], data["valor"], data["ano_temporada"], data["categoria"], data["codequipe"], data["codpiloto"], data["codfabricante"])
  return jsonify({"message": f"Produto {codProd} atualizado com sucesso."})

@produto_bp.route("/produtos/<int:codProd>", methods=["DELETE"])
def deletar_produto(codProd):
  model_produto.deletar(codProd)
  return jsonify({"mensagem": f"Produto {codProd} deletado com sucesso."})

@produto_bp.route("/produtos/busca", methods=["GET"])
def buscar_produto():
  nomeProd = request.args.get('nome')
  produtos = model_produto.filtrarNome(nomeProd) or ""
  return jsonify(produtos)