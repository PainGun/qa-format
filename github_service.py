"""
Servicio de GitHub para integración con la aplicación QA
"""

import json
import webbrowser
from typing import List, Dict, Optional, Callable
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
from github import Github, GithubException
import requests
import io

# Importar el servicio especializado de ramas
from github_branch_service import GitHubBranchService, GitHubBranchesWorker, GitHubCreateBranchWorker

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
                'bio': user.bio or '',  # Biografía del usuario
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
    
    def download_user_avatar(self, size: int = 80) -> Optional[QPixmap]:
        """Descarga el avatar del usuario y retorna un QPixmap"""
        if not self.user_info or not self.user_info.get('avatar_url'):
            return None
        
        try:
            # Agregar parámetro de tamaño a la URL del avatar
            avatar_url = f"{self.user_info['avatar_url']}&s={size}"
            
            # Descargar la imagen
            response = requests.get(avatar_url, timeout=10)
            response.raise_for_status()
            
            # Crear QPixmap desde los datos de la imagen
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                return pixmap
            else:
                print("Error al cargar la imagen del avatar")
                return None
                
        except requests.RequestException as e:
            print(f"Error al descargar avatar: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al procesar avatar: {e}")
            return None
    
    def logout(self):
        """Cierra la sesión"""
        self.github_client = None
        self.user_info = None
        self.access_token = None

class GitHubAvatarWorker(QThread):
    """Worker thread para descargar avatar del usuario sin bloquear la UI"""
    
    avatar_ready = pyqtSignal(object)  # Señal cuando el avatar está listo (QPixmap)
    error_occurred = pyqtSignal(str)   # Señal cuando ocurre un error
    
    def __init__(self, avatar_url: str, size: int = 80):
        super().__init__()
        self.avatar_url = avatar_url
        self.size = size
    
    def run(self):
        """Descarga el avatar en un hilo separado"""
        try:
            # Agregar parámetro de tamaño a la URL del avatar
            avatar_url = f"{self.avatar_url}&s={self.size}"
            
            # Descargar la imagen
            response = requests.get(avatar_url, timeout=10)
            response.raise_for_status()
            
            # Crear QPixmap desde los datos de la imagen
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                self.avatar_ready.emit(pixmap)
            else:
                self.error_occurred.emit("Error al cargar la imagen del avatar")
                
        except requests.RequestException as e:
            self.error_occurred.emit(f"Error al descargar avatar: {e}")
        except Exception as e:
            self.error_occurred.emit(f"Error inesperado al procesar avatar: {e}")

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
        self.branch_service: Optional[GitHubBranchService] = None
    
    def _initialize_branch_service(self):
        """Inicializa el servicio de ramas si está autenticado"""
        if self.is_authenticated() and not self.branch_service:
            self.branch_service = GitHubBranchService(self.auth_service.github_client)
    
    def authenticate(self, token: str) -> bool:
        """Autentica con GitHub"""
        success = self.auth_service.authenticate_with_token(token)
        if success:
            self._initialize_branch_service()
        return success
    
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
        self.branch_service = None
    
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
    
    def download_avatar(self, avatar_url: str) -> Optional[QPixmap]:
        """Descarga el avatar del usuario"""
        try:
            response = requests.get(avatar_url)
            if response.status_code == 200:
                image_data = response.content
                image = QPixmap()
                image.loadFromData(image_data)
                return image
            else:
                print(f"Error al descargar el avatar: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error inesperado al descargar el avatar: {e}")
            return None
    
    def get_repository_branches(self, repo_full_name: str) -> List[Dict]:
        """Obtiene las ramas de un repositorio específico"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.get_repository_branches(repo_full_name)
    
    def create_branch(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> bool:
        """Crea una nueva rama en el repositorio"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.create_branch(repo_full_name, branch_name, source_branch)
    
    def create_branch_with_validation(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> bool:
        """Crea una nueva rama con validaciones completas"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.create_branch_with_validation(repo_full_name, branch_name, source_branch)
    
    def delete_branch(self, repo_full_name: str, branch_name: str) -> bool:
        """Elimina una rama del repositorio"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.delete_branch(repo_full_name, branch_name)
    
    def branch_exists(self, repo_full_name: str, branch_name: str) -> bool:
        """Verifica si una rama existe"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.branch_exists(repo_full_name, branch_name)
    
    def suggest_branch_name(self, base_name: str, repo_full_name: str) -> str:
        """Sugiere un nombre de rama disponible"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.suggest_branch_name(base_name, repo_full_name)
    
    def get_branches_async(self, repo_full_name: str) -> GitHubBranchesWorker:
        """Obtiene ramas de forma asíncrona"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.get_branches_async(repo_full_name)
    
    def create_branch_async(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> GitHubCreateBranchWorker:
        """Crea una rama de forma asíncrona"""
        self._initialize_branch_service()
        if not self.branch_service:
            raise Exception("Servicio de ramas no disponible")
        return self.branch_service.create_branch_async(repo_full_name, branch_name, source_branch)
    
    def get_repository_info(self, repo_full_name: str) -> Dict:
        """Obtiene información detallada de un repositorio"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.auth_service.github_client.get_repo(repo_full_name)
            
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
                'has_issues': repo.has_issues,
                'has_projects': repo.has_projects,
                'has_wiki': repo.has_wiki,
                'open_issues_count': repo.open_issues_count,
                'size': repo.size
            }
            
            return repo_info
            
        except Exception as e:
            raise Exception(f"Error obteniendo información del repositorio: {str(e)}")
