from db.connection import get_connection
import psycopg2.extras

def criar(data, valor, status, codCliente, codVendedor, statusPagamento=None):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
      INSERT INTO venda (dataVenda, valorVenda, codPagamaneto, codCliente, codVendedor, statusPagamento)
      VALUES (%s, %s, %s, %s, %s, %s)
      RETURNING codVenda;
  """, (data, valor, status, codCliente, codVendedor, statusPagamento))
  codVenda = cur.fetchone()[0]
  conn.commit()
  cur.close()
  conn.close()
  return codVenda

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("""
    SELECT
        v.codvenda,
        v.datavenda,
        v.valorvenda,
        v.statuspagamento,
        v.codcliente,
        p.nomepagamento,
        ve.nomevendedor
    FROM
        venda v
    JOIN
        pagamento p ON v.codpagamaneto = p.codpagamaneto
    JOIN
        vendedor ve ON v.codvendedor = ve.codvendedor;
  """)
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
  relatorio = cur.fetchone()
  cur.close()
  conn.close()
  return dict(relatorio) if relatorio else None