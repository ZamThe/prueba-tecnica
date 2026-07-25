from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.repository import Repository
from app.schemas.repository import (
    RepositoryResponse, 
    RepositoryCreate, 
    RepositoryUpdate, 
    SyncResultSchema
)
from app.services.external_api import sync_github_repositories


router = APIRouter(tags=["Repositories & System"])


@router.get(
    "/health", 
    status_code=status.HTTP_200_OK,
    summary="Estado de la aplicación",
    description="Verifica que el servicio esté activo y respondiendo."
)
def health_check():
    return {"status": "healthy", "database": "connected"}


@router.post(
    "/sync/{username}", 
    response_model=SyncResultSchema,
    summary="Sincronizar repositorios de GitHub",
    description="Consume la API de GitHub para el usuario dado y actualiza/crea los registros en PostgreSQL."
)
def sync_user_repos(username: str, db: Session = Depends(get_db)):
    result = sync_github_repositories(username, db)
    return result


@router.get(
    "/repositories", 
    response_model=List[RepositoryResponse],
    summary="Consultar todos los repositorios",
    description="Obtiene el listado de repositorios almacenados localmente. Soporta filtros por lenguaje, estrellas y paginación."
)
def get_repositories(
    language: Optional[str] = Query(None, description="Filtrar por lenguaje de programación (ej: Python)"),
    min_stars: Optional[int] = Query(None, ge=0, description="Filtrar por número mínimo de estrellas"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de registros a retornar"),
    db: Session = Depends(get_db)
):
    query = db.query(Repository)
    if language:
        query = query.filter(Repository.language.ilike(f"%{language}%"))
    if min_stars is not None:
        query = query.filter(Repository.stars >= min_stars)
    
    return query.offset(skip).limit(limit).all()


@router.get(
    "/repositories/{repo_id}", 
    response_model=RepositoryResponse,
    summary="Consultar repositorio por ID",
    description="Obtiene los detalles de un único repositorio mediante su ID interno en la base de datos."
)
def get_repository_by_id(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Repositorio con ID {repo_id} no encontrado."
        )
    return repo


@router.post(
    "/repositories", 
    response_model=RepositoryResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo repositorio manualmente",
    description="Permite registrar manualmente un repositorio en la base de datos local."
)
def create_repository(repo_data: RepositoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Repository).filter(Repository.github_id == repo_data.github_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ya existe un repositorio registrado con ese github_id."
        )
    
    new_repo = Repository(**repo_data.model_dump())
    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)
    return new_repo

@router.put(
    "/repositories/{repo_id}", 
    response_model=RepositoryResponse,
    summary="Actualizar un repositorio",
    description="Actualiza los datos de un repositorio existente por su ID."
)
def update_repository(repo_id: int, repo_data: RepositoryUpdate, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Repositorio con ID {repo_id} no encontrado."
        )
    
    update_dict = repo_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(repo, key, value)
        
    db.commit()
    db.refresh(repo)
    return repo


@router.delete(
    "/repositories/{repo_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un repositorio",
    description="Elimina permanentemente un registro de la base de datos local."
)
def delete_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Repositorio con ID {repo_id} no encontrado."
        )
    
    db.delete(repo)
    db.commit()
    return None