from flask import Blueprint, request, jsonify
#from Projeto_CRUD_BD.db.connection import get_connection
from db.connection import get_connection
import psycopg2.extras

# Uso do "blueprint" para agrupar todas as rotas
routes = Blueprint("routes", __name__)

# =====================
# CLIENTE
# =====================

@routes.route("/clientes", methods=["POST"])
def criar_cliente():
    data = request.json
    query = """
        INSERT INTO cliente (nomecliente, emailcliente, cpfCliente, datanasc, telefonecliente)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING codcliente;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (
        data["nomecliente"],
        data["emailcliente"],
        data["cpfCliente"],
        data["datanasc"],
        data["telefonecliente"]
    ))
    codcliente = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"codCliente": codcliente}), 201


@routes.route("/clientes", methods=["GET"])
def listar_clientes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM cliente;")
    clientes = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(clientes)


@routes.route("/clientes/<int:codcliente>", methods=["PUT"])
def atualizar_cliente(codcliente):
    data = request.json
    query = """
        UPDATE cliente
        SET nomecliente=%s, emailcliente=%s, telefonecliente=%s
        WHERE codcliente=%s;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (
        data["nomecliente"],
        data["emailcliente"],
        data["telefonecliente"],
        codcliente
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": f"Cliente {codcliente} atualizado"})


@routes.route("/clientes/<int:codcliente>", methods=["DELETE"])
def deletar_cliente(codcliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cliente WHERE codcliente=%s;", (codcliente,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": f"Cliente {codcliente} deletado"})


# =====================
# VENDA
# =====================

@routes.route("/vendas", methods=["POST"])
def criar_venda():
    data = request.json
    query = """
        INSERT INTO venda (datavenda, valorvenda, status, codcliente)
        VALUES (%s, %s, %s, %s)
        RETURNING codvenda;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (
        data["datavenda"],
        data["valorvenda"],
        data["status"],
        data["codcliente"]
    ))
    codvenda = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"codVenda": codvenda}), 201


@routes.route("/vendas", methods=["GET"])
def listar_vendas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM venda;")
    vendas = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(vendas)


# =====================
# PRODUTO-VENDA
# =====================

@routes.route("/produtos-venda", methods=["POST"])
def criar_produtovenda():
    data = request.json
    query = """
        INSERT INTO produtovenda (codvenda, codprod, qtdvenda, valorunitario)
        VALUES (%s, %s, %s, %s);
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (
        data["codvenda"],
        data["codprod"],
        data["qtdvenda"],
        data["valorunitario"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Produto adicionado à venda"}), 201


@routes.route("/produtos-venda/<int:codvenda>", methods=["GET"])
def listar_produtosvenda(codvenda):
    query = "SELECT * FROM produtovenda WHERE codvenda=%s;"
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, (codvenda,))
    itens = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(itens)
