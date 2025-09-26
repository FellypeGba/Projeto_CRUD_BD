from db.connection import get_connection
import psycopg2.extras

def inserir(nome, cidade):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fabricante (nomeFabricante, cidadeFabricante)
        VALUES (%s, %s)
        RETURNING codFabricante;
    """, (nome, cidade))
    codFabricante = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return codFabricante

def listar():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM fabricante;")
    fabricantes = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return fabricantes

def filtrarNome(nome):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    busca = f"%{nome}%"
    cur.execute("SELECT * FROM fabricante WHERE nomeFabricante ILIKE %s;", (busca,))
    fabricantes = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return fabricantes

def atualizar(id, nome, cidade):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE fabricante SET nomeFabricante=%s, cidadeFabricante=%s
        WHERE codFabricante=%s
    """, (nome, cidade, id))
    conn.commit()
    cur.close()
    conn.close()
    return cur.rowcount > 0

def deletar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM fabricante WHERE codFabricante=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return cur.rowcount > 0
