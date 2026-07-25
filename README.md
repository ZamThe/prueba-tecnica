# 🚀 Gestor de Repositorios de GitHub & Sincronización de API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

Un software web de pila completa (*Full-Stack*) creado para utilizar e integrar la API pública de GitHub. Permite la sincronización de los repositorios de usuarios concretos, su almacenamiento en una base de datos relacional y su gestión a través de una interfaz web interactiva que lleva a cabo operaciones completas **CRUD** (Crear, Leer, Actualizar y Eliminar).

---

## 🔍 Vista General

El sistema actúa como un puente entre la API de GitHub y un panel de administración local/remoto. Sus funciones principales incluyen:
- **Sincronización Automática:** Obtención e inserción masiva de repositorios públicos desde GitHub.
- **Gestión CRUD:** Interfaz intuitiva para crear registros manualmente, actualizar metadatos, visualizar detalles y eliminar repositorios.
- **Persistencia de Datos:** Almacenamiento seguro mediante mapeo objeto-relacional (ORM).

---

## 🏗️ Arquitectura del Sistema

La solución adopta un patrón de **Arquitectura Monolítica Ligera** con separación clara de responsabilidades:

```text
┌───────────────────────────────────────────────────────────┐
│                     Navegador Web                         │
│       (SPA: HTML5 + Bootstrap 5 + Vanilla JavaScript)      │
└─────────────────────────────┬─────────────────────────────┘
                              │ HTTP / JSON
                              ▼
┌───────────────────────────────────────────────────────────┐
│                       FastAPI                             │
│ ┌──────────────┐    ┌──────────────┐    ┌───────────────┐ │
│ │  Endpoints   │───>│   Services   │───>│ API de GitHub │ │
│ └──────────────┘    └──────────────┘    └───────────────┘ │
│        │                   │                              │
│        ▼                   ▼                              │
│ ┌──────────────┐    ┌──────────────┐                      │
│ │   Schemas    │    │ Models (ORM) │                      │
│ └──────────────┘    └──────────────┘                      │
└─────────────────────────────┬─────────────────────────────┘
                              │ SQLAlchemy
                              ▼
┌───────────────────────────────────────────────────────────┐
│              Base de Datos (SQLite3 / Postgres)           │
└───────────────────────────────────────────────────────────┘



