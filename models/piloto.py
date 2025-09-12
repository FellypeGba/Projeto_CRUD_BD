from db.connection import get_connection
import psycopg2.extras

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
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM piloto;")
  pilotos = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return pilotos

def atualizar(id, nome, numero, codEquipe):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE piloto
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
  """, (id,))
  conn.commit()
  cur.close()
  conn.close()
