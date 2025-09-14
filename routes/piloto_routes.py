from flask import Blueprint, request, jsonify
import models.piloto as model_piloto

piloto_bp = Blueprint("piloto", __name__)

@piloto_bp.route("/pilotos", methods=["POST"])
def inserir_piloto():
  data = request.json
  model_piloto.inserir(data["nomepiloto"], data["numero"], data["codequipe"])
  return jsonify({"message": "Piloto adicionada com sucesso"})

@piloto_bp.route("/pilotos", methods=["GET"])
def listar_pilotos():
  pilotos = model_piloto.listar()
  return jsonify(pilotos)

@piloto_bp.route("/pilotos/<int:codPiloto>", methods=["PUT"])
def atualizar_piloto(codPiloto):
  data = request.json
  model_piloto.atualizar(codPiloto, data["nomepiloto"], data["numero"], data["codequipe"])
  return jsonify({"message": f"Piloto {codPiloto} atualizado com sucesso."})

@piloto_bp.route("/pilotos/<int:codPiloto>", methods=["DELETE"])
def deletar_piloto(codPiloto):
  model_piloto.deletar(codPiloto)
  return jsonify({"mensagem": f"Piloto {codPiloto} deletado com sucesso."})

@piloto_bp.route("/pilotos/busca", methods=["GET"])
def buscar_cliente():
  nomePiloto = request.args.get('nome')
  pilotos = model_piloto.filtrarNome(nomePiloto) or ""
  return jsonify(pilotos)