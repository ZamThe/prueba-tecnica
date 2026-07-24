import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.endpoints import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 1. Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Incluir rutas de la API (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_STR)

# 3. Definir la ruta absoluta base basada en la ubicación de este main.py
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

# 4. Montar la carpeta 'frontend' para servir archivos estáticos (/static/app.js, /static/styles.css)
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# 5. Servir el index.html en la raíz (http://localhost:8000/)
@app.get("/", response_class=FileResponse)
def read_root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Servicio activo. Coloca el index.html en la carpeta 'frontend'"}