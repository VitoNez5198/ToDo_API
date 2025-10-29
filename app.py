import sqlite3
from flask import Flask, jsonify, request

# --- Configuración de la Base de Datos ---
DATABASE = 'todo.db' # Nombre del archivo de la BD

def get_db_connection():
    """Crea una conexión a la BD SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente' 
        );
    """)
    conn.commit()
    conn.close()

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)

# Inicializa la BD al arrancar la app
with app.app_context():
    init_db()

# --- Ruta de Prueba ---
@app.route('/')
def index():
    return "API To-Do List está funcionando!"