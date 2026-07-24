import requests
from sqlalchemy.orm import Session
from app.models.repository import Repository

def sync_github_repositories(username: str, db: Session):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {
            "message": f"Error al consultar GitHub para el usuario {username}",
            "synced_count": 0,
            "new_records": 0,
            "updated_records": 0
        }
        
    repos_data = response.json()
    new_count = 0
    updated_count = 0

    for item in repos_data:
        existing_repo = db.query(Repository).filter(Repository.github_id == item["id"]).first()
        
        if existing_repo:
            existing_repo.name = item["name"]
            existing_repo.full_name = item["full_name"]
            existing_repo.owner = item["owner"]["login"]
            existing_repo.html_url = item["html_url"]
            existing_repo.description = item.get("description")
            existing_repo.stars = item["stargazers_count"]
            existing_repo.language = item.get("language")
            updated_count += 1
        else:
            new_repo = Repository(
                github_id=item["id"],
                name=item["name"],
                full_name=item["full_name"],
                owner=item["owner"]["login"],
                html_url=item["html_url"],
                description=item.get("description"),
                stars=item["stargazers_count"],
                language=item.get("language")
            )
            db.add(new_repo)
            new_count += 1

    db.commit()
    return {
        "message": f"Sincronización completada exitosamente para {username}.",
        "synced_count": len(repos_data),
        "new_records": new_count,
        "updated_records": updated_count
    }