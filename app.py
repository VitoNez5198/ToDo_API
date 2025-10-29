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

# --- Endpoint para OBTENER TODAS las tareas (GET) ---
@app.route('/tareas', methods=['GET'])
def get_all_tareas():
    conn = get_db_connection()
    tareas_cursor = conn.execute('SELECT * FROM tareas').fetchall()
    conn.close()

    # Convierte los resultados a una lista de diccionarios
    tareas_list = [dict(tarea) for tarea in tareas_cursor]

    return jsonify(tareas_list)

# --- Endpoint para OBTENER UNA tarea por ID (GET) ---
@app.route('/tareas/<int:id>', methods=['GET'])
def get_tarea(id):
    conn = get_db_connection()
    tarea = conn.execute('SELECT * FROM tareas WHERE id = ?', (id,)).fetchone()
    conn.close()

    if tarea is None:
        return jsonify({"message": "Tarea no encontrada"}), 404

    return jsonify(dict(tarea))