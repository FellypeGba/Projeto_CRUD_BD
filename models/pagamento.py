from db.connection import get_connection
import psycopg2.extras

def inserir(nome):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO pagamento (nomePagamento)
    VALUES (%s)
  """, (nome,))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM pagamento ORDER BY codPagamaneto;")
  pagamentos = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return pagamentos