from db.connection import get_connection

def inserir(nome):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO equipe (nomeEquipe)
    VALUES (%s)
  """, (nome))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM equipe;")
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

def atualizar(id, nome):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE equipe
    SET nome=%s
    WHERE codEquipe=%s;
  """, (nome, id))
  conn.commit()
  cur.close()
  conn.close()

def deletar(id):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    DELETE FROM equipe
    WHERE codEquipe=%s
  """, (id))
  conn.commit()
  cur.close()
  conn.close()
