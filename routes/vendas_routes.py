from flask import Blueprint, request, jsonify
import models.venda as model_venda

venda_bp = Blueprint("venda", __name__)

@venda_bp.route("/vendas", methods=["POST"])
def criar_venda():
  data = request.json
  codVenda = model_venda.criar(
    data["datavenda"],
    data["valorvenda"],
    data["codpagamento"],
    data["codcliente"],
    data["codvendedor"],
    data.get("statuspagamento")
  )
  return jsonify({"message": "Venda criada com sucesso", "codVenda": codVenda})

@venda_bp.route("/vendas", methods=["GET"])
def listar_vendas():
  vendas = model_venda.listar()
  return jsonify(vendas)

@venda_bp.route("/vendas/relatorio", methods=["GET"])
def relatorio_vendas():
  relatorio = model_venda.gerar_relatorio()
  return jsonify(relatorio)


#Opcional: Deletar venda

# @venda_bd.route("/venda/<int:codCliente>", methods=["DELETE"])
# def deletar_venda(codCliente):
#    model_venda.deletar(codCliente)
#    return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})