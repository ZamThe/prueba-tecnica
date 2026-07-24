from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RepositoryBase(BaseModel):
    github_id: int
    name: str
    full_name: str
    owner: str
    html_url: str
    description: Optional[str] = None
    stars: int = 0
    language: Optional[str] = None

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stars: Optional[int] = None
    language: Optional[str] = None

class RepositoryResponse(RepositoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SyncResultSchema(BaseModel):
    message: str
    synced_count: int
    new_records: int
    updated_records: int