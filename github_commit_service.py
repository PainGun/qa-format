"""
Servicio para gestión de commits y diferencias en repositorios Git
Maneja operaciones de staging, commits y visualización de cambios
"""

import os
import subprocess
from typing import List, Dict, Optional, Tuple
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

class GitCommitService:
    """Servicio para operaciones de Git locales"""
    
    def __init__(self):
        self.current_repo_path = None
    
    def set_repository_path(self, repo_path: str) -> bool:
        """Establece la ruta del repositorio actual"""
        if os.path.exists(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
            self.current_repo_path = repo_path
            return True
        return False
    
    def get_changed_files(self) -> List[Dict]:
        """Obtiene la lista de archivos modificados"""
        if not self.current_repo_path:
            return []
        
        try:
            # Ejecutar git status --porcelain para obtener archivos modificados
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.current_repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    status = line[:2]
                    # El nombre del archivo empieza en la posición 3 (después del status y espacio)
                    filepath = line[3:]  # No usar strip() aquí para preservar espacios del nombre
                    
                    # Para archivos renombrados, el formato es "old_name -> new_name"
                    if ' -> ' in filepath:
                        # Usar el nuevo nombre del archivo
                        filepath = filepath.split(' -> ')[1]
                    
                    # Mapear estados de Git
                    file_info = {
                        'path': filepath,
                        'status': status,
                        'status_text': self._get_status_text(status),
                        'icon': self._get_status_icon(status)
                    }
                    files.append(file_info)
            
            return files
        except subprocess.CalledProcessError:
            return []
    
    def _get_status_text(self, status: str) -> str:
        """Convierte el estado de Git en texto legible"""
        status_map = {
            'M ': 'Modificado',
            ' M': 'Modificado',
            'MM': 'Modificado',
            'A ': 'Nuevo',
            ' A': 'Nuevo',
            'D ': 'Eliminado',
            ' D': 'Eliminado',
            'R ': 'Renombrado',
            ' R': 'Renombrado',
            'C ': 'Copiado',
            ' C': 'Copiado',
            '??': 'Sin seguimiento'
        }
        return status_map.get(status, 'Desconocido')
    
    def _get_status_icon(self, status: str) -> str:
        """Obtiene el icono según el estado del archivo"""
        if status.startswith('M') or status.endswith('M'):
            return '📝'
        elif status.startswith('A') or status.endswith('A'):
            return '➕'
        elif status.startswith('D') or status.endswith('D'):
            return '❌'
        elif status.startswith('R') or status.endswith('R'):
            return '🔄'
        elif status.startswith('C') or status.endswith('C'):
            return '📋'
        elif status == '??':
            return '❓'
        else:
            return '📄'
    
    def get_file_diff(self, filepath: str) -> str:
        """Obtiene las diferencias de un archivo específico"""
        if not self.current_repo_path:
            return "No hay repositorio seleccionado"
        
        try:
            # Primero verificar si es un archivo nuevo (untracked)
            status_result = subprocess.run(
                ['git', 'status', '--porcelain', '--', filepath],
                cwd=self.current_repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if status_result.stdout.strip():
                status = status_result.stdout.strip()[:2]
                
                # Archivo nuevo (untracked)
                if status == '??':
                    # Mostrar el contenido completo del archivo nuevo
                    try:
                        with open(os.path.join(self.current_repo_path, filepath), 'r', encoding='utf-8') as f:
                            content = f.read()
                        return f"📄 Archivo nuevo: {filepath}\n\n" + '\n'.join(f"+{line}" for line in content.split('\n'))
                    except Exception:
                        return f"📄 Archivo nuevo: {filepath}\n(No se puede leer el contenido)"
                
                # Archivo staged (en el índice)
                elif status.startswith('A') or status.endswith('A') or status.startswith('M'):
                    # Mostrar diff staged
                    result = subprocess.run(
                        ['git', 'diff', '--cached', '--', filepath],
                        cwd=self.current_repo_path,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if result.stdout.strip():
                        return result.stdout
                
                # Archivo modificado (working directory)
                if status.endswith('M') or status == ' M':
                    # Mostrar diff del working directory
                    result = subprocess.run(
                        ['git', 'diff', '--', filepath],
                        cwd=self.current_repo_path,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if result.stdout.strip():
                        return result.stdout
            
            # Si no hay cambios específicos, intentar diff general
            result = subprocess.run(
                ['git', 'diff', '--', filepath],
                cwd=self.current_repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout if result.stdout.strip() else "No hay cambios para mostrar"
            
        except subprocess.CalledProcessError as e:
            return f"Error al obtener diferencias: {e}"
        except Exception as e:
            return f"Error inesperado: {e}"
    
    def stage_file(self, filepath: str) -> bool:
        """Agrega un archivo al área de staging"""
        if not self.current_repo_path:
            return False
        
        try:
            subprocess.run(
                ['git', 'add', filepath],
                cwd=self.current_repo_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def unstage_file(self, filepath: str) -> bool:
        """Remueve un archivo del área de staging"""
        if not self.current_repo_path:
            return False
        
        try:
            subprocess.run(
                ['git', 'reset', 'HEAD', filepath],
                cwd=self.current_repo_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def commit_changes(self, message: str, files: List[str] = None) -> bool:
        """Crea un commit con los archivos especificados"""
        if not self.current_repo_path:
            return False
        
        try:
            # Si se especifican archivos, agregarlos al staging
            if files:
                for file in files:
                    self.stage_file(file)
            
            # Realizar commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.current_repo_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_current_branch(self) -> str:
        """Obtiene la rama actual"""
        if not self.current_repo_path:
            return "No disponible"
        
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.current_repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip() or "detached HEAD"
        except subprocess.CalledProcessError:
            return "Error"
    
    def is_git_repository(self, path: str) -> bool:
        """Verifica si la ruta es un repositorio Git"""
        return os.path.exists(os.path.join(path, '.git'))

class GitStatusWorker(QThread):
    """Worker para obtener el estado del repositorio de forma asíncrona"""
    
    status_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, git_service: GitCommitService):
        super().__init__()
        self.git_service = git_service
    
    def run(self):
        """Ejecuta la obtención del estado del repositorio"""
        try:
            files = self.git_service.get_changed_files()
            self.status_ready.emit(files)
        except Exception as e:
            self.error_occurred.emit(str(e))

class GitDiffWorker(QThread):
    """Worker para obtener las diferencias de un archivo de forma asíncrona"""
    
    diff_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, git_service: GitCommitService, filepath: str):
        super().__init__()
        self.git_service = git_service
        self.filepath = filepath
    
    def run(self):
        """Ejecuta la obtención de diferencias"""
        try:
            diff = self.git_service.get_file_diff(self.filepath)
            self.diff_ready.emit(diff)
        except Exception as e:
            self.error_occurred.emit(str(e))
