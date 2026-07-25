# 🚀 Gestor de Repositorios de GitHub & Sincronización de API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

Un software web de pila completa (*Full-Stack*) diseñado para consumir e integrar la API pública de GitHub. Permite sincronizar repositorios de usuarios específicos, almacenarlos en una base de datos relacional y gestionarlos mediante una interfaz web interactiva que ejecuta operaciones **CRUD** completas (*Crear, Leer, Actualizar y Eliminar*).

---

## 📋 Tabla de Contenidos
- [Vista General](#-vista-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Variables de Entorno](#-variables-de-entorno)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Despliegue](#-despliegue)

---

## 🔍 Vista General

El sistema actúa como un puente entre la API de GitHub y un panel de administración local/remoto. Sus funciones principales incluyen:
- **Sincronización Automática:** Obtención e inserción masiva de repositorios públicos desde GitHub.
- **Gestión CRUD:** Interfaz intuitiva para crear registros manualmente, actualizar metadatos, visualizar detalles y eliminar repositorios.
- **Persistencia de Datos:** Almacenamiento seguro mediante mapeo objeto-relacional (ORM).

---

## 🏗️ Arquitectura del Sistema

La solución adopta un patrón de **Arquitectura Monolítica Ligera** con separación clara de responsabilidades (*Clean Architecture*):

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
