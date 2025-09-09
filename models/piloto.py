from db.connection import get_connection

def inserir(nome, numero, codEquipe):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO piloto (nome, numero, codEquipe)
    VALUES (%s, %s, %s)
  """, (nome, numero, codEquipe))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM piloto;")
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

def atualizar(id, nome, numero, codEquipe):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE equipe
    SET nome=%s, numero=%s, codEquipe=%s
    WHERE codEquipe=%s;
  """, (nome,numero, codEquipe))
  conn.commit()
  cur.close()
  conn.close()

def deletar(id):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    DELETE FROM piloto
    WHERE codPiloto=%s
  """, (id))
  conn.commit()
  cur.close()
  conn.close()
