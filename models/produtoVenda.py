from db.connection import get_connection
import psycopg2.extras

def inserir(codVenda, codProd, qtdVenda, valorUnd):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO produtoVenda (codVenda, codProd, qtdVenda, valorUnitario)
    VALUES (%s, %s, %s, %s)
  """, (codVenda, codProd, qtdVenda, valorUnd))
  conn.commit()
  cur.close()
  conn.close()

# alterar para mostrar o nome do produto e data da compra tambem
def listar(codVenda):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("""
    SELECT P.nomeProd, PV.qtdVenda, PV.valorUnitario FROM produtoVenda PV
    INNER JOIN produto P
    ON PV.codProd = P.codProd
    WHERE codVenda=%s;
  """, (codVenda,))
  produtosVenda = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return produtosVenda

#função de listar todas as relações venda-produto
def listarTudo():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    SELECT P.nomeProd, PV.* FROM produtoVenda PV
    INNER JOIN produto P
    ON PV.codProd = P.codProd
  """,)
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

