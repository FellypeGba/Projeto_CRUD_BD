from flask import Blueprint, jsonify, request
import models.pagamento as model_pagamento

pagamento_bp = Blueprint("pagamento", __name__)

@pagamento_bp.route("/pagamentos", methods=["GET"])
def listar_pagamentos():
  pagamentos = model_pagamento.listar()
  return jsonify(pagamentos)

@pagamento_bp.route("/pagamentos", methods=["POST"])
def criar_pagamaneto():
  data = request.json
  model_pagamento.inserir(data["nomepagamento"])
  return jsonify({"message": "Pagamento adicionado com sucesso"})