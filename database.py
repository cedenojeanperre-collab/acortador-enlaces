import sqlite3

def conectar():
    coneccion = sqlite3.connect("enlaces.db")
    coneccion.row_factory = sqlite3.Row
    return coneccion

def crear_tabla():
    coneccion = conectar()
    cur = coneccion.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            url_original TEXT NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            clics INTEGER DEFAULT 0
       )       
    """)
    coneccion.commit()
    coneccion.close()
    
if __name__ == "__main__":
    crear_tabla()
    print('Tabla creada correctamente')
     
      