from db.connection import get_connection

def criar(data, valor, codCliente, status):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO venda (dataVenda, valorVenda, statusVenda, codCliente)
    VALUES (%s, %s, %s, %s)
  """, (data, valor, status, codCliente))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM venda;")
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

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