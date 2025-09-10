from db.connection import get_connection

def inserir(nome, numero, codEquipe):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO piloto (nomePiloto, numero, codEquipe)
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
    SET nomePiloto=%s, numero=%s, codEquipe=%s
    WHERE codPiloto=%s;
  """, (nome,numero, codEquipe, id))
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
