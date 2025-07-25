"""
Servicio para integración con Jira
"""

from jira import JIRA
from typing import List, Dict, Optional

class JiraService:
    def __init__(self):
        self.jira = None
        self.server_url = None
        self.username = None
        self.is_connected = False
        
    def connect(self, server_url: str, username: str, api_token: str) -> bool:
        """
        Conecta con Jira usando API Token
        
        Args:
            server_url: URL del servidor Jira (ej: https://tuempresa.atlassian.net)
            username: Tu email de Jira
            api_token: Token de API de Jira
            
        Returns:
            bool: True si la conexión fue exitosa
        """
        try:
            # Limpiar URL si tiene barra al final
            if server_url.endswith('/'):
                server_url = server_url[:-1]
                
            self.jira = JIRA(
                server=server_url,
                basic_auth=(username, api_token)
            )
            
            # Verificar conexión obteniendo info del usuario
            user = self.jira.myself()
            self.server_url = server_url
            self.username = username
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"Error conectando a Jira: {e}")
            self.is_connected = False
            return False
    
    def get_assigned_issues(self, max_results: int = 50) -> List[Dict]:
        """
        Obtiene las tareas asignadas al usuario actual
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de issues asignadas
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            # JQL para obtener issues asignadas al usuario actual
            jql = f'assignee = currentUser() AND resolution = Unresolved ORDER BY updated DESC'
            
            issues = self.jira.search_issues(jql, maxResults=max_results)
            
            result = []
            for issue in issues:
                issue_data = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'description': getattr(issue.fields, 'description', '') or '',
                    'status': issue.fields.status.name,
                    'priority': getattr(issue.fields.priority, 'name', 'No Priority') if hasattr(issue.fields, 'priority') and issue.fields.priority else 'No Priority',
                    'issue_type': issue.fields.issuetype.name,
                    'project': issue.fields.project.key,
                    'project_name': issue.fields.project.name,
                    'assignee': getattr(issue.fields.assignee, 'displayName', 'Unassigned') if issue.fields.assignee else 'Unassigned',
                    'reporter': getattr(issue.fields.reporter, 'displayName', 'Unknown') if issue.fields.reporter else 'Unknown',
                    'created': str(issue.fields.created)[:10] if issue.fields.created else 'N/A',
                    'updated': str(issue.fields.updated)[:10] if issue.fields.updated else 'N/A',
                    'url': f"{self.server_url}/browse/{issue.key}"
                }
                result.append(issue_data)
                
            return result
            
        except Exception as e:
            raise Exception(f"Error obteniendo issues: {e}")
    
    def get_projects(self) -> List[Dict]:
        """
        Obtiene todos los proyectos accesibles
        
        Returns:
            List[Dict]: Lista de proyectos
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            projects = self.jira.projects()
            
            result = []
            for project in projects:
                project_data = {
                    'key': project.key,
                    'name': project.name,
                    'description': getattr(project, 'description', '') or 'Sin descripción',
                    'lead': getattr(project.lead, 'displayName', 'Unknown') if hasattr(project, 'lead') and project.lead else 'Unknown',
                    'project_type': getattr(project, 'projectTypeKey', 'Unknown'),
                    'url': f"{self.server_url}/browse/{project.key}"
                }
                result.append(project_data)
                
            return result
            
        except Exception as e:
            raise Exception(f"Error obteniendo proyectos: {e}")
    
    def get_issues_by_project(self, project_key: str, max_results: int = 30) -> List[Dict]:
        """
        Obtiene issues de un proyecto específico
        
        Args:
            project_key: Clave del proyecto
            max_results: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de issues del proyecto
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            jql = f'project = "{project_key}" ORDER BY updated DESC'
            
            issues = self.jira.search_issues(jql, maxResults=max_results)
            
            result = []
            for issue in issues:
                issue_data = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'priority': getattr(issue.fields.priority, 'name', 'No Priority') if hasattr(issue.fields, 'priority') and issue.fields.priority else 'No Priority',
                    'issue_type': issue.fields.issuetype.name,
                    'assignee': getattr(issue.fields.assignee, 'displayName', 'Unassigned') if issue.fields.assignee else 'Unassigned',
                    'updated': str(issue.fields.updated)[:10] if issue.fields.updated else 'N/A',
                    'url': f"{self.server_url}/browse/{issue.key}"
                }
                result.append(issue_data)
                
            return result
            
        except Exception as e:
            raise Exception(f"Error obteniendo issues del proyecto: {e}")
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """
        Busca issues usando JQL personalizado
        
        Args:
            jql: Query JQL
            max_results: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de issues encontradas
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            issues = self.jira.search_issues(jql, maxResults=max_results)
            
            result = []
            for issue in issues:
                issue_data = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'priority': getattr(issue.fields.priority, 'name', 'No Priority') if hasattr(issue.fields, 'priority') and issue.fields.priority else 'No Priority',
                    'issue_type': issue.fields.issuetype.name,
                    'assignee': getattr(issue.fields.assignee, 'displayName', 'Unassigned') if issue.fields.assignee else 'Unassigned',
                    'url': f"{self.server_url}/browse/{issue.key}"
                }
                result.append(issue_data)
                
            return result
            
        except Exception as e:
            raise Exception(f"Error en búsqueda JQL: {e}")
    
    def get_user_info(self) -> Dict:
        """
        Obtiene información del usuario actual
        
        Returns:
            Dict: Información del usuario
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            user = self.jira.myself()
            return {
                'name': user['displayName'],
                'email': user['emailAddress'],
                'account_id': user['accountId'],
                'active': user['active'],
                'timezone': user.get('timeZone', 'Unknown')
            }
            
        except Exception as e:
            raise Exception(f"Error obteniendo info del usuario: {e}")
    
    def disconnect(self):
        """Desconecta de Jira"""
        self.jira = None
        self.server_url = None
        self.username = None
        self.is_connected = False
    
    def get_issue_transitions(self, issue_key: str) -> List[Dict]:
        """
        Obtiene las transiciones disponibles para un issue
        
        Args:
            issue_key: Clave del issue (ej: PROJ-123)
            
        Returns:
            List[Dict]: Lista de transiciones disponibles
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            issue = self.jira.issue(issue_key)
            transitions = self.jira.transitions(issue)
            
            result = []
            for transition in transitions:
                transition_data = {
                    'id': transition['id'],
                    'name': transition['name'],
                    'to_status': transition['to']['name']
                }
                result.append(transition_data)
                
            return result
            
        except Exception as e:
            raise Exception(f"Error obteniendo transiciones: {e}")
    
    def transition_issue(self, issue_key: str, transition_id: str, comment: str = None) -> bool:
        """
        Realiza una transición de estado en un issue
        
        Args:
            issue_key: Clave del issue (ej: PROJ-123)
            transition_id: ID de la transición a realizar
            comment: Comentario opcional para la transición
            
        Returns:
            bool: True si la transición fue exitosa
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            issue = self.jira.issue(issue_key)
            
            # Preparar datos de la transición
            transition_data = {}
            
            # Agregar comentario si se proporciona
            if comment:
                transition_data['comment'] = [{'body': comment}]
            
            # Realizar la transición
            self.jira.transition_issue(issue, transition_id, **transition_data)
            return True
            
        except Exception as e:
            raise Exception(f"Error realizando transición: {e}")
    
    def add_comment_to_issue(self, issue_key: str, comment: str) -> bool:
        """
        Agrega un comentario a un issue
        
        Args:
            issue_key: Clave del issue
            comment: Texto del comentario
            
        Returns:
            bool: True si el comentario fue agregado exitosamente
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            issue = self.jira.issue(issue_key)
            self.jira.add_comment(issue, comment)
            return True
            
        except Exception as e:
            raise Exception(f"Error agregando comentario: {e}")
    
    def update_issue_status_by_name(self, issue_key: str, target_status: str, comment: str = None) -> bool:
        """
        Cambia el estado de un issue usando el nombre del estado
        
        Args:
            issue_key: Clave del issue
            target_status: Nombre del estado objetivo (ej: "Done", "In Progress")
            comment: Comentario opcional
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        if not self.is_connected:
            raise Exception("No conectado a Jira")
        
        try:
            # Obtener transiciones disponibles
            transitions = self.get_issue_transitions(issue_key)
            
            # Buscar la transición que lleva al estado objetivo
            target_transition = None
            for transition in transitions:
                if transition['to_status'].lower() == target_status.lower():
                    target_transition = transition
                    break
            
            if not target_transition:
                raise Exception(f"No se encontró transición al estado '{target_status}'. Estados disponibles: {[t['to_status'] for t in transitions]}")
            
            # Realizar la transición
            return self.transition_issue(issue_key, target_transition['id'], comment)
            
        except Exception as e:
            raise Exception(f"Error cambiando estado: {e}")
