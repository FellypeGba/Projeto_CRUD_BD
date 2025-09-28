from db.connection import get_connection
import psycopg2.extras

def inserir(nome, email, cpf, dataNasc, telefone, timeAmado, onePiece, cidade):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
      INSERT INTO cliente (nomeCliente, emailCliente, cpfCliente, dataNasc, telefoneCliente, timeAmado, onePiece, cidade)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, email, cpf, dataNasc, telefone, timeAmado, onePiece, cidade))
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

def exibirUm(id):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM cliente WHERE codCliente =%s;", (id,))
  cliente = cur.fetchone()
  cur.close()
  conn.close()
  return dict(cliente)

def buscaEmail(email):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM cliente WHERE emailCliente = %s;", (email,))
  cliente = cur.fetchone()
  cur.close()
  conn.close()
  return dict(cliente)

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

def filtrarNome(nome):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  buscaNome = f"%{nome}%"
  cur.execute("""
    SELECT * FROM cliente
    WHERE nomeCliente ILIKE (%s);
  """, (buscaNome,))

  clientes = [dict(row) for row in cur.fetchall()]
  conn.commit()
  cur.close()
  conn.close()
  return clientes


