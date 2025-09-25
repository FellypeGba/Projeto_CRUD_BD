from flask import Blueprint, request, jsonify
import models.vendedor as model_vendedor

vendedor_bp = Blueprint("vendedor", __name__)

@vendedor_bp.route("/vendedores", methods=["POST"])
def criar_vendedor():
    data = request.json
    codVendedor = model_vendedor.criar(
        data["nomevendedor"], data["emailvendedor"], data["datanasc"], data["telefonevendedor"]
    )
    return jsonify({"message": "Vendedor criado com sucesso", "codVendedor": codVendedor})

@vendedor_bp.route("/vendedores", methods=["GET"])
def listar_vendedores():
    vendedores = model_vendedor.listar()
    return jsonify(vendedores)

@vendedor_bp.route("/vendedores/<int:id>", methods=["GET"])
def obter_vendedor(id):
    vendedor = model_vendedor.obter(id)
    if vendedor:
        return jsonify(vendedor)
    return jsonify({"message": "Vendedor não encontrado"}), 404

@vendedor_bp.route("/vendedores/<int:id>", methods=["PUT"])
def atualizar_vendedor(id):
    data = request.json
    atualizado = model_vendedor.atualizar(
        id, data["nomevendedor"], data["emailvendedor"], data["datanasc"], data["telefonevendedor"]
    )
    if atualizado:
        return jsonify({"message": "Vendedor atualizado com sucesso"})
    return jsonify({"message": "Vendedor não encontrado"}), 404


## Deletar vendedor ??
@vendedor_bp.route("/vendedores/<int:id>", methods=["DELETE"])
def deletar_vendedor(id):
    deletado = model_vendedor.deletar(id)
    if deletado:
        return jsonify({"message": "Vendedor deletado com sucesso"})
    return jsonify({"message": "Vendedor não encontrado"}), 404


