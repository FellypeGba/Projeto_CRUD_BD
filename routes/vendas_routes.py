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

@venda_bp.route("/vendas/relatorio/vendedor/<int:codVendedor>", methods=["GET"])
def relatorio_mensal_por_vendedor(codVendedor):
  try:
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)

    if not ano or not mes:
      return jsonify({"erro": "Os parâmetros 'ano' e 'mês' são obrigatórios na consulta."}), 400

    relatorio = model_venda.gerar_relatorio_vendedor_mensal(codVendedor, mes, ano)

    if relatorio:
      return jsonify(relatorio)
    else:
      return jsonify({"mensagem": "Nenhum dado de venda encontrado para este vendedor no período especificado."}), 404
      
  except Exception as e:
    return jsonify({"erro": str(e)}), 500


#Opcional: Deletar venda

# @venda_bd.route("/venda/<int:codCliente>", methods=["DELETE"])
# def deletar_venda(codCliente):
#    model_venda.deletar(codCliente)
#    return jsonify({"mensagem": f"Cliente {codCliente} deletado com sucesso."})