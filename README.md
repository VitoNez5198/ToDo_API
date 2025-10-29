# API de Gestión de Tareas (To-Do List)

Este es un proyecto de API REST simple, creado con Python y Flask, que permite a los usuarios gestionar una lista de tareas. Es un proyecto de portafolio enfocado en demostrar los fundamentos del desarrollo backend, la creación de endpoints CRUD y la interacción con una base de datos SQL.

---

## Tecnologías Utilizadas

* **Python 3:** Lenguaje principal.
* **Flask:** Micro-framework para crear la API.
* **SQLite3:** Base de datos SQL ligera para el almacenamiento de datos.

---

## Instalación y Ejecución

Sigue estos pasos para levantar el proyecto localmente.

### 1. Requisitos Previos

* Tener [Python 3](https://www.python.org/downloads/) instalado.
* Tener [Git](https://git-scm.com/downloads) instalado.

### 2. Clonar el Repositorio

```
git clone https://github.com/VitoNez5198/ToDo_API.git
cd ToDo_API
```

### 3. Crear y Activar el entorno Virtual

### Crear el entorno virtual
`python -m venv venv`

### Activar en Windows (Git Bash)
`source venv/Scripts/activate`


### 4. Instalar dependencias

Asegúrate de tener el entorno activado.

`pip install -r requirements.txt`

### 5.Ejecutar la Aplicaicion

`flask run`

La API ahora estará corriendo en http://127.0.0.1:5000

## Guía de Endpoints de la API

Puedes usar Postman o cURL para probar los endpoints.

---

### 1. Obtener todas las tareas

* **Método:** `GET`
* **Ruta:** `/tareas`
* **Respuesta Exitosa (200):**

```json
[
    {
        "id": 1,
        "titulo": "Aprender Flask",
        "descripcion": "Crear mi primer endpoint",
        "estado": "pendiente"
    },
    {
        "id": 2,
        "titulo": "Escribir README",
        "descripcion": "Documentar el proyecto",
        "estado": "completada"
    }
]
```

### 2. Obtener una tarea por ID

* **Método:** `GET`
* **Ruta:** `/tareas/<id>` (Ej: `/tareas/1`)
* **Respuesta Exitosa (200):**

```json
{
    "id": 1,
    "titulo": "Aprender Flask",
    "descripcion": "Crear mi primer endpoint",
    "estado": "pendiente"
}
```
* **Respuesta de Error (404):**

```json
{
    "message": "Tarea no encontrada"
}
```

### 3. Crear una nueva tarea

* **Método:** `POST`
* **Ruta:** `/tareas`
* **Cuerpo (Body) - JSON Requerido:**


```json
{
    "titulo": "Mi Nueva Tarea",
    "descripcion": "Esta es la descripción (opcional)."
}
```
* **Respuesta Exitosa (201):**

```JSON

{
    "id": 3,
    "titulo": "Mi Nueva Tarea",
    "descripcion": "Esta es la descripción (opcional).",
    "estado": "pendiente"
}
```
### 4. Actualizar una tarea
* **Método:** `PUT`
* **Ruta:** `/tareas/<id>` (Ej: `/tareas/3`)
* **Cuerpo (Body) - JSON (envía solo lo que quieras cambiar):**

```json

{
    "titulo": "Título Actualizado",
    "estado": "completada"
}
```
* **Respuesta Exitosa (200):**

```json

{
    "id": 3,
    "titulo": "Título Actualizado",
    "descripcion": "Esta es la descripción (opcional).",
    "estado": "completada"
}
```

### 5. Eliminar una tarea
* **Método:** `DELETE`
* **Ruta:** `/tareas/<id>` (Ej: `/tareas/3`)
* **Respuesta Exitosa (200):**

```json
{
    "message": "Tarea con ID 3 eliminada exitosamente"
}
```