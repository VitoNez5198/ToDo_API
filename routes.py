from flask import jsonify, request
from db import get_db_connection # Importamos la función de BD
import sqlite3 # Para el manejo de errores

# Esta función recibe la app de Flask como argumento
def register_routes(app):

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
        descripcion = data.get('descripcion')
        
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)',
                (titulo, descripcion)
            )
            conn.commit()
            new_id = cursor.lastrowid
            
            new_tarea = conn.execute('SELECT * FROM tareas WHERE id = ?', (new_id,)).fetchone()
            conn.close()
            
            return jsonify(dict(new_tarea)), 201
            
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"error": str(e)}), 500
            
    #---Endpoint para Actualizar una tarea (PUT)---
    @app.route('/tareas/<int:id>', methods=['PUT'])
    def update_tarea(id):
        data = request.get_json()
        
        if data is None:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        estado = data.get('estado')
        
        conn = get_db_connection()
        
        tarea_existente = conn.execute('SELECT * FROM tareas WHERE id = ?', (id,)).fetchone()
        if tarea_existente is None:
            conn.close()
            return jsonify({"message": "Tarea no encontrada"}), 404

        query = "UPDATE tareas SET "
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

        if not params:
            conn.close()
            return jsonify({"error": "No hay campos para actualizar"}), 400
            
        query = query.rstrip(', ') + " WHERE id = ?"
        params.append(id)

        try:
            conn.execute(query, tuple(params))
            conn.commit()
            
            updated_tarea = conn.execute('SELECT * FROM tareas WHERE id = ?', (id,)).fetchone()
            conn.close()
            
            return jsonify(dict(updated_tarea)) 

        except sqlite3.Error as e:
            conn.close()
            return jsonify({"error": str(e)}), 500

    #---Ednpoint para ELIMINAR una tarea (DELETE)---
    @app.route('/tareas/<int:id>', methods=['DELETE'])
    def delete_tarea(id):
        conn = get_db_connection()
        cursor = conn.execute('DELETE FROM tareas WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:
            return jsonify({"message": "Tarea no encontrada"}), 404
        return jsonify({"message": f"Tarea con ID {id} eliminada exitosamente"}), 200