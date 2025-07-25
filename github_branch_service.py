"""
Servicio especializado para gestión de ramas en GitHub
"""

import re
import uuid
from typing import List, Dict, Optional, Tuple
from PyQt6.QtCore import QThread, pyqtSignal
from github import Github, GithubException


class GitHubBranchValidator:
    """Clase para validar nombres de ramas según las reglas de Git/GitHub"""
    
    @staticmethod
    def validate_branch_name(branch_name: str) -> Tuple[bool, str]:
        """Valida si el nombre de la rama es válido según las reglas de Git/GitHub"""
        
        # Verificar que no esté vacío
        if not branch_name or not branch_name.strip():
            return False, "El nombre de la rama no puede estar vacío"
        
        branch_name = branch_name.strip()
        
        # Verificar longitud
        if len(branch_name) > 250:
            return False, "El nombre de la rama no puede tener más de 250 caracteres"
        
        # Verificar caracteres prohibidos
        if re.search(r'[~^:?*\[\]\\]', branch_name):
            return False, "El nombre contiene caracteres no permitidos: ~ ^ : ? * [ ] \\"
        
        # No puede empezar o terminar con punto, slash o guión
        if branch_name.startswith('.') or branch_name.endswith('.'):
            return False, "El nombre no puede empezar o terminar con punto"
        
        if branch_name.startswith('/') or branch_name.endswith('/'):
            return False, "El nombre no puede empezar o terminar con slash"
        
        if branch_name.startswith('-') or branch_name.endswith('-'):
            return False, "El nombre no puede empezar o terminar con guión"
        
        # No puede contener espacios consecutivos o caracteres de control
        if '  ' in branch_name or any(ord(c) < 32 for c in branch_name):
            return False, "El nombre no puede contener espacios consecutivos o caracteres de control"
        
        # No puede ser solo puntos
        if branch_name.replace('.', '') == '':
            return False, "El nombre no puede ser solo puntos"
        
        # Verificar que no sea una referencia especial
        reserved_names = ['HEAD', 'refs', 'origin']
        if branch_name in reserved_names:
            return False, f"'{branch_name}' es un nombre reservado"
        
        return True, "Nombre válido"
    
    @staticmethod
    def sanitize_branch_name(base_name: str) -> str:
        """Limpia y sanitiza un nombre base para convertirlo en un nombre de rama válido"""
        # Limpiar el nombre base
        base_name = re.sub(r'[^a-zA-Z0-9\-_/]', '-', base_name)
        base_name = re.sub(r'-+', '-', base_name)  # Eliminar guiones consecutivos
        base_name = base_name.strip('-')  # Eliminar guiones al inicio y final
        
        if not base_name:
            base_name = "feature"
        
        return base_name


class GitHubBranchesWorker(QThread):
    """Worker thread para obtener ramas de un repositorio sin bloquear la UI"""
    
    branches_ready = pyqtSignal(list)  # Señal cuando las ramas están listas
    error_occurred = pyqtSignal(str)   # Señal cuando ocurre un error
    
    def __init__(self, branch_service, repo_full_name: str):
        super().__init__()
        self.branch_service = branch_service
        self.repo_full_name = repo_full_name
    
    def run(self):
        """Obtiene las ramas en un hilo separado"""
        try:
            branches = self.branch_service.get_repository_branches(self.repo_full_name)
            self.branches_ready.emit(branches)
        except Exception as e:
            self.error_occurred.emit(str(e))


class GitHubCreateBranchWorker(QThread):
    """Worker thread para crear una nueva rama sin bloquear la UI"""
    
    branch_created = pyqtSignal(str)   # Señal cuando la rama se crea exitosamente
    error_occurred = pyqtSignal(str)   # Señal cuando ocurre un error
    
    def __init__(self, branch_service, repo_full_name: str, branch_name: str, source_branch: str = None):
        super().__init__()
        self.branch_service = branch_service
        self.repo_full_name = repo_full_name
        self.branch_name = branch_name
        self.source_branch = source_branch
    
    def run(self):
        """Crea la rama en un hilo separado"""
        try:
            success = self.branch_service.create_branch_with_validation(
                self.repo_full_name, 
                self.branch_name, 
                self.source_branch
            )
            if success:
                self.branch_created.emit(self.branch_name)
            else:
                self.error_occurred.emit("No se pudo crear la rama")
        except Exception as e:
            self.error_occurred.emit(str(e))


class GitHubDeleteBranchWorker(QThread):
    """Worker thread para eliminar una rama sin bloquear la UI"""
    
    branch_deleted = pyqtSignal(str)   # Señal cuando la rama se elimina exitosamente
    error_occurred = pyqtSignal(str)   # Señal cuando ocurre un error
    
    def __init__(self, branch_service, repo_full_name: str, branch_name: str):
        super().__init__()
        self.branch_service = branch_service
        self.repo_full_name = repo_full_name
        self.branch_name = branch_name
    
    def run(self):
        """Elimina la rama en un hilo separado"""
        try:
            success = self.branch_service.delete_branch(self.repo_full_name, self.branch_name)
            if success:
                self.branch_deleted.emit(self.branch_name)
            else:
                self.error_occurred.emit("No se pudo eliminar la rama")
        except Exception as e:
            self.error_occurred.emit(str(e))


class GitHubBranchService:
    """Servicio especializado para gestión de ramas en GitHub"""
    
    def __init__(self, github_client: Github):
        self.github_client = github_client
        self.validator = GitHubBranchValidator()
    
    def is_authenticated(self) -> bool:
        """Verifica si el cliente de GitHub está autenticado"""
        return self.github_client is not None
    
    def get_repository_branches(self, repo_full_name: str) -> List[Dict]:
        """Obtiene las ramas de un repositorio específico"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            branches = repo.get_branches()
            
            branch_list = []
            for branch in branches:
                try:
                    # Obtener información del último commit
                    last_commit = branch.commit
                    commit_date = last_commit.commit.author.date if last_commit.commit.author else None
                    commit_author = last_commit.commit.author.name if last_commit.commit.author else "Desconocido"
                    commit_message = last_commit.commit.message[:100] + "..." if len(last_commit.commit.message) > 100 else last_commit.commit.message
                    
                    branch_info = {
                        'name': branch.name,
                        'sha': branch.commit.sha,
                        'protected': branch.protected if hasattr(branch, 'protected') else False,
                        'last_commit_date': commit_date.isoformat() if commit_date else "N/A",
                        'last_commit_author': commit_author,
                        'last_commit_message': commit_message,
                        'last_commit_sha': last_commit.sha[:7] if last_commit.sha else "N/A"
                    }
                    branch_list.append(branch_info)
                    
                except Exception as e:
                    # Si hay error obteniendo detalles de una rama, agregar info básica
                    branch_info = {
                        'name': branch.name,
                        'sha': branch.commit.sha if hasattr(branch.commit, 'sha') else "N/A",
                        'protected': False,
                        'last_commit_date': "N/A",
                        'last_commit_author': "N/A",
                        'last_commit_message': "Error obteniendo información",
                        'last_commit_sha': "N/A"
                    }
                    branch_list.append(branch_info)
                    print(f"Error obteniendo detalles de la rama {branch.name}: {e}")
            
            # Ordenar por fecha de último commit (más recientes primero)
            branch_list.sort(key=lambda x: x['last_commit_date'] if x['last_commit_date'] != "N/A" else "1970-01-01", reverse=True)
            
            return branch_list
            
        except Exception as e:
            raise Exception(f"Error obteniendo ramas del repositorio: {str(e)}")
    
    def branch_exists(self, repo_full_name: str, branch_name: str) -> bool:
        """Verifica si una rama ya existe en el repositorio"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            try:
                repo.get_branch(branch_name)
                return True
            except:
                return False
        except Exception as e:
            raise Exception(f"Error verificando si la rama existe: {str(e)}")
    
    def get_default_branch(self, repo_full_name: str) -> str:
        """Obtiene la rama por defecto del repositorio"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            return repo.default_branch
        except Exception as e:
            raise Exception(f"Error obteniendo la rama por defecto: {str(e)}")
    
    def create_branch(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> bool:
        """Crea una nueva rama en el repositorio (versión simple)"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            
            # Si no se especifica rama origen, usar la rama por defecto
            if not source_branch:
                source_branch = repo.default_branch
            
            # Obtener el SHA del último commit de la rama origen
            source_branch_obj = repo.get_branch(source_branch)
            source_sha = source_branch_obj.commit.sha
            
            # Crear la nueva rama
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_sha)
            
            return True
            
        except Exception as e:
            raise Exception(f"Error creando la rama: {str(e)}")
    
    def create_branch_with_validation(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> bool:
        """Crea una nueva rama con validaciones completas"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            # Validar nombre de rama
            is_valid, error_msg = self.validator.validate_branch_name(branch_name)
            if not is_valid:
                raise Exception(f"Nombre de rama inválido: {error_msg}")
            
            # Verificar que la rama no exista
            if self.branch_exists(repo_full_name, branch_name):
                raise Exception("La rama ya existe")
            
            repo = self.github_client.get_repo(repo_full_name)
            
            # Si no se especifica rama origen, usar la rama por defecto
            if not source_branch:
                source_branch = repo.default_branch
            
            # Verificar que la rama origen existe
            try:
                source_branch_obj = repo.get_branch(source_branch)
                source_sha = source_branch_obj.commit.sha
            except Exception:
                raise Exception(f"La rama origen '{source_branch}' no existe")
            
            # Crear la nueva rama
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_sha)
            
            return True
            
        except Exception as e:
            raise Exception(f"Error creando la rama: {str(e)}")
    
    def delete_branch(self, repo_full_name: str, branch_name: str) -> bool:
        """Elimina una rama del repositorio (solo si no es la rama por defecto)"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            
            # Verificar que no sea la rama por defecto
            if branch_name == repo.default_branch:
                raise Exception("No se puede eliminar la rama por defecto")
            
            # Verificar que la rama existe
            if not self.branch_exists(repo_full_name, branch_name):
                raise Exception("La rama no existe")
            
            # Eliminar la rama
            ref = repo.get_git_ref(f"heads/{branch_name}")
            ref.delete()
            
            return True
            
        except Exception as e:
            raise Exception(f"Error eliminando la rama: {str(e)}")
    
    def create_branch_from_commit(self, repo_full_name: str, branch_name: str, commit_sha: str) -> bool:
        """Crea una nueva rama desde un commit específico"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            # Validar nombre de rama
            is_valid, error_msg = self.validator.validate_branch_name(branch_name)
            if not is_valid:
                raise Exception(f"Nombre de rama inválido: {error_msg}")
            
            # Verificar que la rama no exista
            if self.branch_exists(repo_full_name, branch_name):
                raise Exception("La rama ya existe")
            
            repo = self.github_client.get_repo(repo_full_name)
            
            # Verificar que el commit existe
            try:
                commit = repo.get_commit(commit_sha)
                commit_sha = commit.sha  # Obtener SHA completo si se pasó uno abreviado
            except Exception:
                raise Exception("El commit especificado no existe")
            
            # Crear la nueva rama
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=commit_sha)
            
            return True
            
        except Exception as e:
            raise Exception(f"Error creando la rama desde commit: {str(e)}")
    
    def get_branch_protection_status(self, repo_full_name: str, branch_name: str) -> Dict:
        """Obtiene el estado de protección de una rama"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            branch = repo.get_branch(branch_name)
            
            protection_info = {
                'protected': branch.protected,
                'protection_details': None
            }
            
            if branch.protected:
                try:
                    protection = branch.get_protection()
                    protection_info['protection_details'] = {
                        'required_status_checks': protection.required_status_checks is not None,
                        'enforce_admins': protection.enforce_admins,
                        'required_pull_request_reviews': protection.required_pull_request_reviews is not None,
                        'restrictions': protection.restrictions is not None
                    }
                except Exception:
                    protection_info['protection_details'] = "No se pudo obtener detalles de protección"
            
            return protection_info
            
        except Exception as e:
            raise Exception(f"Error obteniendo estado de protección: {str(e)}")
    
    def get_branch_commits(self, repo_full_name: str, branch_name: str, limit: int = 10) -> List[Dict]:
        """Obtiene los commits de una rama específica"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            commits = repo.get_commits(sha=branch_name)
            
            commit_list = []
            for i, commit in enumerate(commits):
                if i >= limit:
                    break
                
                commit_info = {
                    'sha': commit.sha,
                    'sha_short': commit.sha[:7],
                    'message': commit.commit.message.split('\n')[0],  # Solo primera línea
                    'author': commit.commit.author.name if commit.commit.author else "Desconocido",
                    'author_email': commit.commit.author.email if commit.commit.author else "N/A",
                    'date': commit.commit.author.date.isoformat() if commit.commit.author and commit.commit.author.date else "N/A",
                    'html_url': commit.html_url
                }
                commit_list.append(commit_info)
            
            return commit_list
            
        except Exception as e:
            raise Exception(f"Error obteniendo commits de la rama: {str(e)}")
    
    def compare_branches(self, repo_full_name: str, base_branch: str, compare_branch: str) -> Dict:
        """Compara dos ramas y obtiene las diferencias"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        try:
            repo = self.github_client.get_repo(repo_full_name)
            comparison = repo.compare(base_branch, compare_branch)
            
            comparison_info = {
                'ahead_by': comparison.ahead_by,
                'behind_by': comparison.behind_by,
                'total_commits': comparison.total_commits,
                'status': comparison.status,  # 'ahead', 'behind', 'identical', 'diverged'
                'commits': []
            }
            
            # Obtener detalles de los commits únicos
            for commit in comparison.commits[:10]:  # Limitar a 10 commits
                commit_info = {
                    'sha': commit.sha[:7],
                    'message': commit.commit.message.split('\n')[0],
                    'author': commit.commit.author.name if commit.commit.author else "Desconocido",
                    'date': commit.commit.author.date.strftime("%Y-%m-%d %H:%M") if commit.commit.author and commit.commit.author.date else "N/A"
                }
                comparison_info['commits'].append(commit_info)
            
            return comparison_info
            
        except Exception as e:
            raise Exception(f"Error comparando ramas: {str(e)}")
    
    def suggest_branch_name(self, base_name: str, repo_full_name: str) -> str:
        """Sugiere un nombre de rama disponible basado en un nombre base"""
        if not self.is_authenticated():
            raise Exception("No está autenticado con GitHub")
        
        # Sanitizar el nombre base
        base_name = self.validator.sanitize_branch_name(base_name)
        
        # Verificar si el nombre base está disponible
        if not self.branch_exists(repo_full_name, base_name):
            return base_name
        
        # Si no está disponible, agregar sufijo numérico
        counter = 1
        while True:
            suggested_name = f"{base_name}-{counter}"
            if not self.branch_exists(repo_full_name, suggested_name):
                return suggested_name
            counter += 1
            
            # Evitar bucle infinito
            if counter > 100:
                return f"{base_name}-{str(uuid.uuid4())[:8]}"
    
    def get_branches_async(self, repo_full_name: str) -> GitHubBranchesWorker:
        """Obtiene ramas de forma asíncrona"""
        worker = GitHubBranchesWorker(self, repo_full_name)
        return worker
    
    def create_branch_async(self, repo_full_name: str, branch_name: str, source_branch: str = None) -> GitHubCreateBranchWorker:
        """Crea una rama de forma asíncrona"""
        worker = GitHubCreateBranchWorker(self, repo_full_name, branch_name, source_branch)
        return worker
    
    def delete_branch_async(self, repo_full_name: str, branch_name: str) -> GitHubDeleteBranchWorker:
        """Elimina una rama de forma asíncrona"""
        worker = GitHubDeleteBranchWorker(self, repo_full_name, branch_name)
        return worker
