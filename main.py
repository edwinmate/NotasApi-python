from fastapi import FastAPI
from typing import Dict
import sqlite3
 
app = FastAPI()
conn = sqlite3.connect('my_notaApi', check_same_thread=False)
cur = conn.cursor()

note_table = '''
    CREATE TABLE IF NOT EXISTS Notas (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        descripcion TEXT,
        nota TEXT
    );
'''
cur.execute(note_table)
conn.commit()

@app.post("/api/notes")
def guardar_nota(dic: Dict):
    queryInsert = f"""INSERT INTO Notas 
    (id,titulo,descripcion,nota) VALUES (
        '{dic['id']}',
        '{dic['titulo']}',
        '{dic['descripcion']}',
        '{dic['nota']}'
    )"""
    try:
        cur.execute(queryInsert)
        conn.commit()
        return {"status":True}
    except Exception as error:
        return {"status":False, "msg":str(error)}
  
@app.get("/api/notes/all")
def allnotes():
    my_listnotes=[]
    queryGetnotes = """
    SELECT id,titulo,descripcion,nota FROM Notas
    """
    cur.execute(queryGetnotes)
    all = cur.fetchall()

    for notes in all:
        my_listnotes.append({
            "id": notes[0],
            "titulo": notes[1],
            "descripcion": notes[2],
            "nota": notes[3],
           
        })
 
    return {"status":True, "data":my_listnotes}

@app.get("/api/notes/{id}")
def onenotes(id:int):
    
    queryGetnotas = f"""
    SELECT id,titulo,descripcion,nota FROM Notas
    WHERE id = {id}
    """
    cur.execute(queryGetnotas)
    ones = cur.fetchone()

    return {
            "id": ones[0],
            "titulo": ones[1],
            "descripcion": ones[2],
            "nota": ones[3],
           
        }
 
@app.delete("/api/notes/{id}")
def eliminar_registro(id:int):
    queryDelete = f"""
    DELETE FROM Notas WHERE id= {id}
    """
 
    try:
        cur.execute(queryDelete)
        conn.commit()
        return {"status":True}
    except Exception as error:
        return {"status":False, "msg":str(error)}
    
