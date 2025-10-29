import sqlite3

DATABASE = 'todo.db' # La configuración de la BD vive aquí

def get_db_connection():
    """Crea una conexión a la BD SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn

def init_db():
    """Inicializa la base de datos leyendo el archivo schema.sql."""
    conn = get_db_connection()
    
    # Abrimos y leemos el archivo SQL
    with open('schema.sql', 'r') as f:
        # executescript permite ejecutar múltiples sentencias SQL
        conn.executescript(f.read()) 
        
    conn.commit()
    conn.close()