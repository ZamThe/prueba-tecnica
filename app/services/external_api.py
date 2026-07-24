import logging
import httpx
from fastapi import HTTPException, status
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings

# Configurar sistema de registros / logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExternalAPIService")

class ExternalAPIService:
    def __init__(self):
        self.base_url = settings.GITHUB_API_URL
        self.token = settings.GITHUB_TOKEN

    def _get_headers(self):
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "FastAPI-App"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # Reintento automático: máximo 3 intentos si falla la red
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=6),
        retry_if_exception_type(httpx.RequestError),
        reraise=True
    )
    async def get_user_repositories(self, username: str, page: int = 1, per_page: int = 10):
        url = f"{self.base_url}/users/{username}/repos?page={page}&per_page={per_page}"
        headers = self._get_headers()

        logger.info(f"Iniciando solicitud a GitHub API para el usuario: {username}, página: {page}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
                
                # Extraer control de límite de consumo (Rate Limit) desde los headers
                rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
                logger.info(f"Límite de peticiones restantes en GitHub API: {rate_limit_remaining}")

                # Control de Errores de Autenticación
                if response.status_code == 401:
                    logger.error("Error 401: Token de autenticación de GitHub inválido o expirado.")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Autenticación fallida con la API de GitHub. Verifique el GITHUB_TOKEN."
                    )
                
                # Control de Recursos No Encontrados
                elif response.status_code == 404:
                    logger.warning(f"Error 404: El usuario '{username}' no fue encontrado en GitHub.")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"El usuario '{username}' no existe en la API externa."
                    )
                
                # Control de Rate Limiting
                elif response.status_code == 403:
                    logger.error("Error 403: Límite de consumo alcanzado en GitHub API.")
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Se ha superado el límite de peticiones de la API externa."
                    )
                
                elif response.status_code != 200:
                    logger.error(f"Error en GitHub API. Status Code: {response.status_code}")
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Error al comunicar con la API externa: status {response.status_code}"
                    )

                data = response.json()

                # Control de Respuestas Vacías
                if not data:
                    logger.info(f"La consulta para el usuario '{username}' retornó 0 repositorios.")
                    return {
                        "message": f"El usuario {username} no tiene repositorios públicos.",
                        "rate_limit_remaining": rate_limit_remaining,
                        "data": []
                    }

                # Transformación y filtrado de datos para el cliente
                cleaned_repos = [
                    {
                        "id": repo.get("id"),
                        "name": repo.get("name"),
                        "full_name": repo.get("full_name"),
                        "html_url": repo.get("html_url"),
                        "description": repo.get("description"),
                        "stars": repo.get("stargazers_count"),
                        "language": repo.get("language")
                    }
                    for repo in data
                ]

                return {
                    "source": "GitHub REST API v3",
                    "page": page,
                    "per_page": per_page,
                    "rate_limit_remaining": rate_limit_remaining,
                    "total_items": len(cleaned_repos),
                    "repositories": cleaned_repos
                }

            except httpx.RequestError as exc:
                logger.error(f"Error de conexión HTTP con GitHub: {str(exc)}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"No se pudo establecer conexión con la API externa: {str(exc)}"
                )

github_service = ExternalAPIService()