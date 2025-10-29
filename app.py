from flask import Flask
from db import init_db
from routes import register_routes # Importamos la función de registro

# 1. Crear la aplicación
app = Flask(__name__)

# 2. Inicializar la Base de Datos
# (Asegura que la tabla exista al arrancar)
with app.app_context():
    init_db()

# 3. Registrar todas las rutas del archivo routes.py
register_routes(app)

# (flask run buscará y usará esta variable 'app' por defecto)