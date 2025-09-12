from db.connection import get_connection
import psycopg2.extras

def criar(data, valor, status, codCliente):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO venda (dataVenda, valorVenda, statusVenda, codCliente)
    VALUES (%s, %s, %s, %s)
    RETURNING codVenda;
  """, (data, valor, status, codCliente))
  novo_id = cur.fetchone()[0]

  conn.commit()
  cur.close()
  conn.close()
  return novo_id

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM venda;")
  vendas = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return vendas

#cancelar compra ?
def deletar(id):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    DELETE FROM venda
    WHERE codVenda=%s
  """, (id))
  conn.commit()
  cur.close()
  conn.close()