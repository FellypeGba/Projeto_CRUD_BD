from db.connection import get_connection

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
  cur = conn.cursor()
  cur.execute("SELECT * FROM cliente;")
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

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
  """, (id))
  conn.commit()
  cur.close()
  conn.close()
