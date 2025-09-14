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
  codVenda = cur.fetchone()[0]

  conn.commit()
  cur.close()
  conn.close()
  return codVenda

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

def gerar_relatorio():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  cur.execute("""
    SELECT
      COUNT(*) AS total_vendas,
      SUM(valorVenda) AS valor_total,
      AVG(valorVenda) AS valor_medio,
      MAX(valorVenda) AS maior_venda,
      MIN(valorVenda) AS menor_venda
    FROM venda;
  """)
  
  # fetchone() é usado porque a consulta retorna apenas uma linha com o resumo
  relatorio = cur.fetchone()
  
  cur.close()
  conn.close()
  
  # Converte o resultado para um dicionário Python padrão
  return dict(relatorio) if relatorio else None