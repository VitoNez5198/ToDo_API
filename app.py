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

# --- Endpoint para CREAR una nueva tarea (POST) ---
@app.route('/tareas', methods=['POST'])
def create_tarea():
    data = request.get_json() 

    if not data or 'titulo' not in data:
        return jsonify({"error": "El campo 'titulo' es requerido"}), 400

    titulo = data['titulo']
    descripcion = data.get('descripcion') # .get() es más seguro

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)',
            (titulo, descripcion)
        )
        conn.commit()
        new_id = cursor.lastrowid

        # Devuelve la tarea recién creada
        new_tarea = conn.execute('SELECT * FROM tareas WHERE id = ?', (new_id,)).fetchone()
        conn.close()


        return jsonify(dict(new_tarea)), 201 # 201 = Created

    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    

#---Endpoint para Actualizar una tarea (PUT)---

@app.route('/tareas/<int:id>', methods=['PUT'])
def update_tarea(id):
    data = request.getjson()
    
    #Verfifica que campos se queiren actrualizar
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    estado = data.get('estado')
    
    conn = get_db_connection()
    
    # Primero hay que verificar si la tarea existe
    tarea_existente = conn.execute('SELECT * FROM tareas WHERE id= ?', (id,)).fetchone()
    if tarea_existente is None:
        conn.close()
        return jsonify({"message": "Tarea no encontrada"}), 404

# Construir consulta SQL dinamicamente

    query = "UPDATE tareas SET"
    params = []

    if titulo is not None:
        query += "titulo = ?, "
        params.append(titulo)
    if descripcion is not None:
        query += "descripcion = ?, "
        params.append(descripcion)
    if estado is not None:
        query += "estado = ?, "
        params.append(estado)

    # quita la coma  el espacio extra del final
    query = query.rstrip(', ') + " WHERE if = ?"
    params.append(id)

    try:
        conn.execute(query, tuple(params))
        conn.commit()
        
        #devuelve la tarea actualizada
        update_tarea = conn.execute('SELECT * FROM tareas WHERE id = ?', (id)).fetchone()
        conn.close()

    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500