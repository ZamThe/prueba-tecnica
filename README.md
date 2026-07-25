🚀 Proyecto: Gestor de repositorios de GitHub y sincronización de API
Esta iniciativa es un software web de pila completa que ha sido creado para utilizar la API pública de GitHub, sincronizar repositorios de usuarios concretos, almacenarlos en una base de datos y proporcionar una interfaz web interactiva para llevar a cabo las operaciones CRUD (Actualizar, Leer, Crear y Eliminar) sobre los registros.


Arquitectura Utilizada
La solución utiliza una arquitectura monolítica ligera con separación limpia de capas:

Frontend: Interfaz estática (Single Page Application - SPA) basada en HTML5, Vanilla JavaScript (ES6+) y Bootstrap 5, servida directamente desde FastAPI.

Backend: FastAPI (Python 3.11) estructurado en módulos:

api/: Definición de endpoints de la API.

core/: Configuración del sistema, seguridad y sesión de Base de Datos.

models/: Modelos ORM de SQLAlchemy.

schemas/: Esquemas de validación de datos con Pydantic.

services/: Lógica de negocio e integración con la API externa de GitHub.

Base de Datos: SQLite3 / PostgreSQL gestionado a través de SQLAlchemy ORM.


Tecnologías Seleccionadas
Lenguaje: Python 3.11

Framework Web: FastAPI (v0.110+)

Servidor ASGI: Uvicorn / Gunicorn

ORM & DB: SQLAlchemy, Pydantic v2, SQLite3

Cliente HTTP: httpx / requests

Frontend: HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5, Bootstrap Icons

PaaS / Despliegue: Railway


