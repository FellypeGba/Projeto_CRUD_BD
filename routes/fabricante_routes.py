from flask import Blueprint, request, jsonify
import models.fabricante as model_fabricante

fabricante_bp = Blueprint("fabricante", __name__)

@fabricante_bp.route("/fabricantes", methods=["POST"])
def criar_fabricante():
    data = request.json
    cod = model_fabricante.inserir(data["nomefabricante"], data["cidadefabricante"])
    return jsonify({"message": "Fabricante criado com sucesso", "codFabricante": cod})

@fabricante_bp.route("/fabricantes", methods=["GET"])
def listar_fabricantes():
    fabricantes = model_fabricante.listar()
    return jsonify(fabricantes)

@fabricante_bp.route("/fabricantes/<int:id>", methods=["PUT"])
def atualizar_fabricante(id):
    data = request.json
    atualizado = model_fabricante.atualizar(id, data["nomefabricante"], data["cidadefabricante"])
    if atualizado:
        return jsonify({"message": "Fabricante atualizado com sucesso"})
    return jsonify({"message": "Fabricante não encontrado"}), 404

@fabricante_bp.route("/fabricantes/<int:id>", methods=["DELETE"])
def deletar_fabricante(id):
    deletado = model_fabricante.deletar(id)
    if deletado:
        return jsonify({"message": "Fabricante deletado com sucesso"})
    return jsonify({"message": "Fabricante não encontrado"}), 404

@fabricante_bp.route("/fabricantes/busca", methods=["GET"])
def buscar_fabricantes():
    nome = request.args.get("nome", "")
    resultado = model_fabricante.filtrarNome(nome)
    return jsonify(resultado)