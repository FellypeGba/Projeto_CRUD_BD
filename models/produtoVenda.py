from db.connection import get_connection

def inserir(codProd, codVenda, qtdVenda, valorUnd):
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
  cur = conn.cursor()
  cur.execute("""
    SELECT P.nomeProduto, PV.* FROM produtoVenda PV
    INNER JOIN produto P
    ON PV.codProd = P.codProd
    WHERE codVenda=%s;
  """, (codVenda))
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

