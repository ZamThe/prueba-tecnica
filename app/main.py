from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import router as api_router

# Aquí es donde se define la variable "app" que busca Uvicorn
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Servicio activo y corriendo correctamente"}