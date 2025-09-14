from db.connection import get_connection
import psycopg2.extras

def inserir(nome):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO equipe (nomeEquipe)
    VALUES (%s)
  """, (nome,))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM equipe;")
  equipes = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return equipes

def atualizar(id, nome):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE equipe
    SET nomeEquipe=%s
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
  """, (id,))
  conn.commit()
  cur.close()
  conn.close()

def filtrarNome(nome):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  buscaNome = f"%{nome}%"
  cur.execute("""
    SELECT * FROM equipe
    WHERE nomeEquipe ILIKE (%s);
  """, (buscaNome,))

  equipes = [dict(row) for row in cur.fetchall()]
  conn.commit()
  cur.close()
  conn.close()
  return equipes
