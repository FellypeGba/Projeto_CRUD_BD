from db.connection import get_connection
import psycopg2.extras

def inserir(nome, email, cpf, dataNasc, telefone):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO cliente (nomeCliente, emailCliente, cpfCliente, dataNasc, telefoneCliente)
    VALUES (%s, %s, %s, %s, %s)
  """, (nome, email, cpf, dataNasc, telefone))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM cliente;")
  clientes = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return clientes

def atualizar(id, nome, email, telefone):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE cliente
    SET nomeCliente=%s, emailCliente=%s, telefoneCliente=%s
    WHERE codCliente=%s;
  """, (nome, email, telefone, id))
  conn.commit()
  cur.close()
  conn.close()

def deletar(id):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    DELETE FROM cliente
    WHERE codCliente=%s
  """, (id,))
  conn.commit()
  cur.close()
  conn.close()
