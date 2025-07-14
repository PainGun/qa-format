"""
Servicio de GitHub para integración con la aplicación QA
"""

import json
import webbrowser
from typing import List, Dict, Optional, Callable
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QMessageBox
from github import Github, GithubException
import requests

class GitHubAuthService:
    """Servicio de autenticación con GitHub usando Personal Access Token"""
    
    def __init__(self):
        self.github_client: Optional[Github] = None
        self.user_info: Optional[Dict] = None
        self.access_token: Optional[str] = None
    
    def authenticate_with_token(self, token: str) -> bool:
        """Autentica con un Personal Access Token"""
        try:
            self.access_token = token
            self.github_client = Github(token)
            
            # Verificar que el token funciona obteniendo info del usuario
            user = self.github_client.get_user()
            self.user_info = {
                'login': user.login,
                'name': user.name or user.login,
                'email': user.email or 'No disponible',
                'avatar_url': user.avatar_url,
                'public_repos': user.public_repos,
                'followers': user.followers,
                'following': user.following
            }
            return True
            
        except GithubException as e:
            print(f"Error de autenticación GitHub: {e}")
            self.github_client = None
            self.user_info = None
            self.access_token = None
            return False
    
    def is_authenticated(self) -> bool:
        """Verifica si está autenticado"""
        return self.github_client is not None and self.user_info is not None
    
    def get_user_info(self) -> Optional[Dict]:
        """Obtiene información del usuario autenticado"""
        return self.user_info
    
    def logout(self):
        """Cierra la sesión"""
        self.github_client = None
        self.user_info = None
        self.access_token = None

class GitHubRepositoryWorker(QThread):
    """Worker thread para obtener repositorios sin bloquear la UI"""
    
    repositories_ready = pyqtSignal(list)  # Señal cuando los repos están listos
    error_occurred = pyqtSignal(str)       # Señal cuando ocurre un error
    
    def __init__(self, github_client: Github, repo_type: str = "all"):
        super().__init__()
        self.github_client = github_client
        self.repo_type = repo_type  # "all", "owner", "public", "private"
    
    def run(self):
        """Obtiene los repositorios en un hilo separado"""
        try:
            user = self.github_client.get_user()
            
            if self.repo_type == "owner":
                repos = user.get_repos(type="owner", sort="updated")
            elif self.repo_type == "public":
                repos = user.get_repos(type="public", sort="updated")
            elif self.repo_type == "private":
                repos = user.get_repos(type="private", sort="updated")
            else:  # "all"
                repos = user.get_repos(sort="updated")
            
            repo_list = []
            # Limitar a los primeros 50 repos para no sobrecargar
            for i, repo in enumerate(repos):
                if i >= 50:  # Límite de 50 repos
                    break
                    
                repo_info = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description or "Sin descripción",
                    'private': repo.private,
                    'language': repo.language or "No especificado",
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'updated_at': repo.updated_at.strftime("%Y-%m-%d %H:%M"),
                    'html_url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'default_branch': repo.default_branch
                }
                repo_list.append(repo_info)
            
            self.repositories_ready.emit(repo_list)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class GitHubService:
    """Servicio principal de GitHub"""
    
    def __init__(self):
        self.auth_service = GitHubAuthService()
        self.current_repositories: List[Dict] = []
    
    def authenticate(self, token: str) -> bool:
        """Autentica con GitHub"""
        return self.auth_service.authenticate_with_token(token)
    
    def is_authenticated(self) -> bool:
        """Verifica si está autenticado"""
        return self.auth_service.is_authenticated()
    
    def get_user_info(self) -> Optional[Dict]:
        """Obtiene información del usuario"""
        return self.auth_service.get_user_info()
    
    def logout(self):
        """Cierra sesión"""
        self.auth_service.logout()
        self.current_repositories = []
    
    def get_repositories_async(self, repo_type: str = "all", 
                              callback: Optional[Callable[[List[Dict]], None]] = None,
                              error_callback: Optional[Callable[[str], None]] = None) -> GitHubRepositoryWorker:
        """Obtiene repositorios de forma asíncrona"""
        if not self.is_authenticated():
            if error_callback:
                error_callback("No está autenticado con GitHub")
            return None
        
        worker = GitHubRepositoryWorker(self.auth_service.github_client, repo_type)
        
        if callback:
            worker.repositories_ready.connect(callback)
        
        if error_callback:
            worker.error_occurred.connect(error_callback)
        
        # Guardar referencia para evitar que se recolecte
        worker.repositories_ready.connect(lambda repos: setattr(self, 'current_repositories', repos))
        
        worker.start()
        return worker
    
    def get_repository_details(self, repo_full_name: str) -> Optional[Dict]:
        """Obtiene detalles específicos de un repositorio"""
        if not self.is_authenticated():
            return None
        
        try:
            repo = self.auth_service.github_client.get_repo(repo_full_name)
            
            # Obtener branches
            branches = [branch.name for branch in repo.get_branches()]
            
            # Obtener último commit
            commits = repo.get_commits()
            latest_commit = None
            if commits.totalCount > 0:
                commit = commits[0]
                latest_commit = {
                    'sha': commit.sha[:7],
                    'message': commit.commit.message.split('\n')[0],  # Solo primera línea
                    'author': commit.commit.author.name,
                    'date': commit.commit.author.date.strftime("%Y-%m-%d %H:%M")
                }
            
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description or "Sin descripción",
                'language': repo.language or "No especificado",
                'branches': branches,
                'default_branch': repo.default_branch,
                'latest_commit': latest_commit,
                'issues_count': repo.open_issues_count,
                'watchers': repo.watchers_count,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'size': repo.size,
                'created_at': repo.created_at.strftime("%Y-%m-%d"),
                'updated_at': repo.updated_at.strftime("%Y-%m-%d %H:%M"),
                'html_url': repo.html_url,
                'clone_url': repo.clone_url
            }
            
        except Exception as e:
            print(f"Error obteniendo detalles del repo: {e}")
            return None
    
    def open_repository_in_browser(self, repo_url: str):
        """Abre el repositorio en el navegador"""
        try:
            webbrowser.open(repo_url)
        except Exception as e:
            print(f"Error abriendo navegador: {e}")
    
    def get_repo_issues(self, repo_full_name: str) -> List[Dict]:
        """Obtiene los issues de un repositorio"""
        if not self.is_authenticated():
            return []
        
        try:
            repo = self.auth_service.github_client.get_repo(repo_full_name)
            issues = repo.get_issues(state="open")
            
            issue_list = []
            for issue in issues[:10]:  # Limitar a 10 issues
                issue_info = {
                    'number': issue.number,
                    'title': issue.title,
                    'state': issue.state,
                    'created_at': issue.created_at.strftime("%Y-%m-%d"),
                    'author': issue.user.login,
                    'html_url': issue.html_url
                }
                issue_list.append(issue_info)
            
            return issue_list
            
        except Exception as e:
            print(f"Error obteniendo issues: {e}")
            return []
    
    def get_user_repositories(self) -> List[Dict]:
        """Obtiene repositorios del usuario de forma síncrona"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            user = self.auth_service.github_client.get_user()
            repos = user.get_repos(sort="updated")
            
            repo_list = []
            # Limitar a los primeros 30 repos para no sobrecargar
            for i, repo in enumerate(repos):
                if i >= 30:  # Límite de 30 repos
                    break
                    
                repo_info = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description or "Sin descripción",
                    'private': repo.private,
                    'language': repo.language or "No especificado",
                    'stargazers_count': repo.stargazers_count,
                    'forks_count': repo.forks_count,
                    'watchers_count': repo.watchers_count,
                    'created_at': repo.created_at.isoformat() if repo.created_at else "N/A",
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else "N/A",
                    'html_url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'default_branch': repo.default_branch,
                    'fork': repo.fork
                }
                repo_list.append(repo_info)
            
            return repo_list
            
        except Exception as e:
            raise Exception(f"Error obteniendo repositorios: {str(e)}")
    
    def get_user_organizations(self) -> List[Dict]:
        """Obtiene las organizaciones del usuario"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            user = self.auth_service.github_client.get_user()
            orgs = user.get_orgs()
            
            org_list = []
            for org in orgs:
                org_info = {
                    'login': org.login,
                    'name': org.name or org.login,
                    'description': org.description or "Sin descripción",
                    'avatar_url': org.avatar_url,
                    'html_url': org.html_url,
                    'public_repos': org.public_repos,
                    'type': 'Organization'
                }
                org_list.append(org_info)
            
            return org_list
            
        except Exception as e:
            raise Exception(f"Error obteniendo organizaciones: {str(e)}")
    
    def get_organization_repositories(self, org_login: str) -> List[Dict]:
        """Obtiene repositorios de una organización específica"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            org = self.auth_service.github_client.get_organization(org_login)
            repos = org.get_repos(sort="updated")
            
            repo_list = []
            # Limitar a los primeros 30 repos para no sobrecargar
            for i, repo in enumerate(repos):
                if i >= 30:  # Límite de 30 repos
                    break
                    
                repo_info = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description or "Sin descripción",
                    'private': repo.private,
                    'language': repo.language or "No especificado",
                    'stargazers_count': repo.stargazers_count,
                    'forks_count': repo.forks_count,
                    'watchers_count': repo.watchers_count,
                    'created_at': repo.created_at.isoformat() if repo.created_at else "N/A",
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else "N/A",
                    'html_url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'default_branch': repo.default_branch,
                    'fork': repo.fork,
                    'organization': org_login,
                    'type': 'OrgRepo'
                }
                repo_list.append(repo_info)
            
            return repo_list
            
        except Exception as e:
            raise Exception(f"Error obteniendo repositorios de la organización: {str(e)}")
