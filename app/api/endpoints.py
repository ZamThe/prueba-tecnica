from fastapi import APIRouter, Query
from app.core.config import settings
from app.services.external_api import github_service

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@router.get("/github/repositories/{username}")
async def get_github_repositories(
    username: str,
    page: int = Query(1, ge=1, description="Número de página para la paginación"),
    per_page: int = Query(10, ge=1, le=50, description="Cantidad de resultados por página")
):
    """
    Consume la API de GitHub usando Bearer Token con soporte para:
    - Autenticación segura
    - Paginación
    - Manejo de límites de consumo
    - Manejo de errores y reintentos automáticos
    """
    return await github_service.get_user_repositories(username, page, per_page)