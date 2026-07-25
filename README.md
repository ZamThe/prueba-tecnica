API de Gestión y Sincronización de Repositorios (Prueba Técnica)

Aplicación web full-stack desarrollada para la consulta, gestión (CRUD) y sincronización automática de repositorios públicos de GitHub mediante una API RESTful en **FastAPI** y una interfaz interactiva con **Bootstrap 5** y JavaScript vanila.


🛠️ Tecnologías Utilizadas

**Backend**
- **Python 3.10+**
- **FastAPI**: Framework web asíncrono para la creación de la API.
- **SQLAlchemy**: ORM para la interacción con la base de datos.
- **Pydantic**: Validación y serialización de esquemas de datos.
- **Uvicorn**: Servidor ASGI de alto rendimiento.
- **PostgreSQL / SQLite**: Base de datos relacional para el almacenamiento local.

### **Frontend**
- **HTML5 & CSS3** (Custom Styles & Animations).
- **Bootstrap 5**: Componentes de UI y modales interactivos.
- **JavaScript ES6+**: Comunicación asíncrona mediante `Fetch API`.

---

📋 Características Principales

- ✅ **Sincronización con GitHub**: Importación y actualización dinámica de repositorios de cualquier usuario mediante la API oficial de GitHub.
- ✅ **CRUD Completo**:
  - **Crear**: Registro manual de repositorios locales.
  - **Leer**: Listado de repositorios almacenados en la base de datos local.
  - **Editar**: Actualización de datos (lenguaje, estrellas, propietario, etc.).
  - **Eliminar**: Eliminación permanente de un registro local.
- ✅ **Navegación Segura**: Normalización automática de URLs hacia GitHub (`https://`) abriendo en nuevas pestañas sin interferir con las rutas locales.
- ✅ **Manejo de Errores y Validaciones**: Sanitización de caracteres (anti-XSS) y respuestas HTTP adecuadas (`200`, `201`, `400`, `404`, `422`).

---
