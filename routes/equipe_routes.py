from flask import Blueprint, request, jsonify
import models.equipe as model_equipe

equipe_bp = Blueprint("equipe", __name__)

@equipe_bp.route("/equipes", methods=["POST"])
def criar_equipe():
  data = request.json
  model_equipe.inserir(data["nomeEquipe"])
  return jsonify({"message": "Equipe adicionada com sucesso"})

@equipe_bp.route("/equipes", methods=["GET"])
def listar_equipes():
  equipes = model_equipe.listar()
  return jsonify(equipes)

@equipe_bp.route("/equipes/<int:codEquipe>", methods=["PUT"])
def atualizar_equipe(codEquipe):
  data = request.json
  model_equipe.atualizar(codEquipe, data["nomeEquipe"])
  return jsonify({"message": f"Equipe {codEquipe} atualizada com sucesso."})

@equipe_bp.route("/equipes/<int:codEquipe>", methods=["DELETE"])
def deletar_cliente(codEquipe):
  model_equipe.deletar(codEquipe)
  return jsonify({"mensagem": f"Equipe {codEquipe} deletada com sucesso."})