"""
Widget de Jira para la aplicación QA Generator
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QListWidget, QTextEdit,
                           QMessageBox, QFrame, QScrollArea, QListWidgetItem,
                           QTabWidget, QComboBox, QSplitter, QTreeWidget,
                           QTreeWidgetItem, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from jira_service import JiraService
from styles import DarkTheme

class JiraWorker(QThread):
    """Worker thread para operaciones de Jira"""
    issues_loaded = pyqtSignal(list)
    projects_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, service, operation, **kwargs):
        super().__init__()
        self.service = service
        self.operation = operation
        self.kwargs = kwargs
        
    def run(self):
        try:
            if self.operation == "assigned_issues":
                issues = self.service.get_assigned_issues(self.kwargs.get('max_results', 50))
                self.issues_loaded.emit(issues)
            elif self.operation == "projects":
                projects = self.service.get_projects()
                self.projects_loaded.emit(projects)
            elif self.operation == "project_issues":
                issues = self.service.get_issues_by_project(
                    self.kwargs.get('project_key'), 
                    self.kwargs.get('max_results', 30)
                )
                self.issues_loaded.emit(issues)
            elif self.operation == "search":
                issues = self.service.search_issues(
                    self.kwargs.get('jql'), 
                    self.kwargs.get('max_results', 50)
                )
                self.issues_loaded.emit(issues)
        except Exception as e:
            self.error_occurred.emit(str(e))

class JiraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.jira_service = JiraService()
        self.worker = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Estado de conexión
        self.connection_status = QLabel("❌ No conectado a Jira")
        self.connection_status.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.connection_status.setStyleSheet("color: #ff6b6b; padding: 10px;")
        layout.addWidget(self.connection_status)
        
        # Frame de login
        self.login_frame = self.create_login_frame()
        layout.addWidget(self.login_frame)
        
        # Frame de issues (inicialmente oculto)
        self.issues_frame = self.create_issues_frame()
        self.issues_frame.hide()
        layout.addWidget(self.issues_frame)
        
    def create_login_frame(self):
        """Crea el frame de login"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(DarkTheme.get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("🔧 Jira Integration")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f8f8f2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Instrucciones
        instructions = QLabel("""Para conectar con Jira necesitas un API Token:

1. 🌐 Ve a tu perfil de Atlassian → Seguridad
2. 🔑 Crear y administrar tokens de API
3. ⚡ Crear token de API
4. 📋 Copia el token generado

Ejemplo de URL del servidor:
• https://tuempresa.atlassian.net
• https://jira.tuempresa.com""")
        
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        instructions.setStyleSheet("""
            color: #6272a4;
            font-size: 11px;
            padding: 15px;
            background-color: rgba(98, 114, 164, 0.1);
            border-radius: 8px;
            border: 1px solid #6272a4;
            line-height: 1.4;
        """)
        layout.addWidget(instructions)
        
        # Campo de servidor
        server_label = QLabel("🌐 URL del Servidor Jira:")
        server_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(server_label)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("https://tuempresa.atlassian.net")
        self.server_input.setStyleSheet(DarkTheme.get_lineedit_style())
        layout.addWidget(self.server_input)
        
        # Campo de usuario
        user_label = QLabel("👤 Email/Usuario:")
        user_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(user_label)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("tu.email@empresa.com")
        self.user_input.setStyleSheet(DarkTheme.get_lineedit_style())
        layout.addWidget(self.user_input)
        
        # Campo de token
        token_label = QLabel("🔑 API Token:")
        token_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(token_label)
        
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("API Token de Jira")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setStyleSheet(DarkTheme.get_lineedit_style())
        layout.addWidget(self.token_input)
        
        # Link para generar token
        link_label = QLabel('🔗 <a href="https://id.atlassian.com/manage-profile/security/api-tokens" style="color: #50fa7b;">Generar API Token</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(link_label)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("🔑 Conectar")
        self.login_btn.clicked.connect(self.connect_to_jira)
        self.login_btn.setStyleSheet(DarkTheme.get_button_style())
        buttons_layout.addWidget(self.login_btn)
        
        cancel_btn = QPushButton("❌ Limpiar")
        cancel_btn.clicked.connect(self.clear_fields)
        cancel_btn.setStyleSheet(DarkTheme.get_button_style())
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        return frame
        
    def create_issues_frame(self):
        """Crea el frame de issues con pestañas"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(DarkTheme.get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("🔧 Tareas de Jira")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f8f8f2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Sistema de pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(DarkTheme.get_frame_style())
        
        # Pestaña de mis issues
        self.my_issues_tab = self.create_my_issues_tab()
        self.tabs.addTab(self.my_issues_tab, "👤 Mis Tareas")
        
        # Pestaña de proyectos
        self.projects_tab = self.create_projects_tab()
        self.tabs.addTab(self.projects_tab, "📁 Proyectos")
        
        # Pestaña de búsqueda
        self.search_tab = self.create_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Búsqueda")
        
        layout.addWidget(self.tabs)
        
        # Botón para desconectar
        disconnect_btn = QPushButton("🚪 Desconectar")
        disconnect_btn.clicked.connect(self.disconnect)
        disconnect_btn.setStyleSheet(DarkTheme.get_button_style())
        layout.addWidget(disconnect_btn)
        
        return frame
    
    def create_my_issues_tab(self):
        """Crea la pestaña de mis issues"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Botón para cargar mis issues
        refresh_btn = QPushButton("🔄 Cargar Mis Tareas Asignadas")
        refresh_btn.clicked.connect(self.load_my_issues)
        refresh_btn.setStyleSheet(DarkTheme.get_button_style())
        layout.addWidget(refresh_btn)
        
        # Lista de mis issues
        self.my_issues_list = QListWidget()
        self.my_issues_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.my_issues_list.itemClicked.connect(self.on_issue_selected)
        layout.addWidget(self.my_issues_list)
        
        # Área de detalles del issue
        self.my_issue_details = QTextEdit()
        self.my_issue_details.setMaximumHeight(150)
        self.my_issue_details.setReadOnly(True)
        self.my_issue_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.my_issue_details.setPlaceholderText("Selecciona una tarea para ver sus detalles...")
        layout.addWidget(self.my_issue_details)
        
        return tab
    
    def create_projects_tab(self):
        """Crea la pestaña de proyectos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Botón para cargar proyectos
        refresh_projects_btn = QPushButton("🔄 Cargar Proyectos")
        refresh_projects_btn.clicked.connect(self.load_projects)
        refresh_projects_btn.setStyleSheet(DarkTheme.get_button_style())
        layout.addWidget(refresh_projects_btn)
        
        # Selector de proyecto
        project_label = QLabel("📁 Selecciona un proyecto:")
        project_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(project_label)
        
        self.project_combo = QComboBox()
        self.project_combo.setStyleSheet(DarkTheme.get_lineedit_style())
        self.project_combo.currentTextChanged.connect(self.on_project_selected)
        layout.addWidget(self.project_combo)
        
        # Lista de issues del proyecto
        self.project_issues_list = QListWidget()
        self.project_issues_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.project_issues_list.itemClicked.connect(self.on_project_issue_selected)
        layout.addWidget(self.project_issues_list)
        
        # Área de detalles del issue del proyecto
        self.project_issue_details = QTextEdit()
        self.project_issue_details.setMaximumHeight(150)
        self.project_issue_details.setReadOnly(True)
        self.project_issue_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.project_issue_details.setPlaceholderText("Selecciona un proyecto y una tarea...")
        layout.addWidget(self.project_issue_details)
        
        return tab
    
    def create_search_tab(self):
        """Crea la pestaña de búsqueda"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Campo de búsqueda JQL
        search_label = QLabel("🔍 Búsqueda JQL:")
        search_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Ejemplo: project = "PROJ" AND status = "In Progress"')
        self.search_input.setStyleSheet(DarkTheme.get_lineedit_style())
        layout.addWidget(self.search_input)
        
        # Botón de búsqueda
        search_btn = QPushButton("🔍 Buscar")
        search_btn.clicked.connect(self.search_issues)
        search_btn.setStyleSheet(DarkTheme.get_button_style())
        layout.addWidget(search_btn)
        
        # Lista de resultados de búsqueda
        self.search_results_list = QListWidget()
        self.search_results_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.search_results_list.itemClicked.connect(self.on_search_result_selected)
        layout.addWidget(self.search_results_list)
        
        # Área de detalles del resultado
        self.search_result_details = QTextEdit()
        self.search_result_details.setMaximumHeight(150)
        self.search_result_details.setReadOnly(True)
        self.search_result_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.search_result_details.setPlaceholderText("Realiza una búsqueda para ver resultados...")
        layout.addWidget(self.search_result_details)
        
        return tab
    
    def connect_to_jira(self):
        """Intenta conectar con Jira"""
        server_url = self.server_input.text().strip()
        username = self.user_input.text().strip()
        api_token = self.token_input.text().strip()
        
        if not all([server_url, username, api_token]):
            QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                              "Por favor completa todos los campos")
            return
            
        self.login_btn.setText("🔄 Conectando...")
        self.login_btn.setEnabled(False)
        
        try:
            if self.jira_service.connect(server_url, username, api_token):
                user_info = self.jira_service.get_user_info()
                
                self.connection_status.setText(f"✅ Conectado como: {user_info.get('name', 'Usuario')}")
                self.connection_status.setStyleSheet("color: #50fa7b; padding: 10px;")
                
                # Ocultar login y mostrar issues
                self.login_frame.hide()
                self.issues_frame.show()
                
                # Cargar datos iniciales
                self.load_my_issues()
                self.load_projects()
                
            else:
                QMessageBox.critical(self, "❌ Error de Conexión", 
                                   "No se pudo conectar a Jira. Verifica tus credenciales.")
                
        except Exception as e:
            QMessageBox.critical(self, "❌ Error de Conexión", 
                               f"Error al conectar con Jira:\n{str(e)}")
        finally:
            self.login_btn.setText("🔑 Conectar")
            self.login_btn.setEnabled(True)
    
    def load_my_issues(self):
        """Carga las issues asignadas al usuario"""
        if self.worker and self.worker.isRunning():
            return
            
        self.my_issues_list.clear()
        self.my_issues_list.addItem("🔄 Cargando tareas asignadas...")
        
        self.worker = JiraWorker(self.jira_service, "assigned_issues")
        self.worker.issues_loaded.connect(self.on_my_issues_loaded)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()
    
    def load_projects(self):
        """Carga los proyectos disponibles"""
        self.project_combo.clear()
        self.project_combo.addItem("🔄 Cargando proyectos...")
        
        self.projects_worker = JiraWorker(self.jira_service, "projects")
        self.projects_worker.projects_loaded.connect(self.on_projects_loaded)
        self.projects_worker.error_occurred.connect(self.on_error)
        self.projects_worker.start()
    
    def on_my_issues_loaded(self, issues):
        """Maneja la carga exitosa de mis issues"""
        self.my_issues_list.clear()
        
        if not issues:
            self.my_issues_list.addItem("📭 No tienes tareas asignadas")
            return
            
        for issue in issues:
            item = QListWidgetItem()
            
            # Información del issue
            key = issue.get('key', 'N/A')
            summary = issue.get('summary', 'Sin título')
            status = issue.get('status', 'N/A')
            priority = issue.get('priority', 'N/A')
            project = issue.get('project', 'N/A')
            
            # Texto del item
            item_text = f"🔧 {key} - {summary}\n📊 {status} | ⚡ {priority} | 📁 {project}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, issue)
            
            self.my_issues_list.addItem(item)
    
    def on_projects_loaded(self, projects):
        """Maneja la carga exitosa de proyectos"""
        self.project_combo.clear()
        
        if not projects:
            self.project_combo.addItem("📭 No hay proyectos disponibles")
            return
        
        self.project_combo.addItem("Selecciona un proyecto...")
        for project in projects:
            project_text = f"📁 {project.get('name', project.get('key', 'Sin nombre'))}"
            self.project_combo.addItem(project_text)
            # Guardar datos del proyecto en el combo
            self.project_combo.setItemData(self.project_combo.count() - 1, project)
    
    def on_project_selected(self, project_text):
        """Maneja la selección de un proyecto"""
        if project_text.startswith("🔄") or project_text.startswith("📭") or project_text.startswith("Selecciona"):
            return
        
        # Obtener datos del proyecto
        current_index = self.project_combo.currentIndex()
        project_data = self.project_combo.itemData(current_index)
        
        if not project_data:
            return
        
        project_key = project_data.get('key')
        if project_key:
            self.load_project_issues(project_key)
    
    def load_project_issues(self, project_key):
        """Carga issues de un proyecto específico"""
        self.project_issues_list.clear()
        self.project_issues_list.addItem(f"🔄 Cargando issues de {project_key}...")
        
        self.project_worker = JiraWorker(self.jira_service, "project_issues", project_key=project_key)
        self.project_worker.issues_loaded.connect(self.on_project_issues_loaded)
        self.project_worker.error_occurred.connect(self.on_error)
        self.project_worker.start()
    
    def on_project_issues_loaded(self, issues):
        """Maneja la carga exitosa de issues del proyecto"""
        self.project_issues_list.clear()
        
        if not issues:
            self.project_issues_list.addItem("📭 No hay issues en este proyecto")
            return
            
        for issue in issues:
            item = QListWidgetItem()
            
            # Información del issue
            key = issue.get('key', 'N/A')
            summary = issue.get('summary', 'Sin título')
            status = issue.get('status', 'N/A')
            assignee = issue.get('assignee', 'Sin asignar')
            
            # Texto del item
            item_text = f"🔧 {key} - {summary}\n📊 {status} | 👤 {assignee}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, issue)
            
            self.project_issues_list.addItem(item)
    
    def search_issues(self):
        """Busca issues usando JQL"""
        jql = self.search_input.text().strip()
        
        if not jql:
            QMessageBox.warning(self, "⚠️ JQL Requerido", 
                              "Por favor ingresa una consulta JQL")
            return
        
        self.search_results_list.clear()
        self.search_results_list.addItem("🔄 Buscando...")
        
        self.search_worker = JiraWorker(self.jira_service, "search", jql=jql)
        self.search_worker.issues_loaded.connect(self.on_search_results_loaded)
        self.search_worker.error_occurred.connect(self.on_error)
        self.search_worker.start()
    
    def on_search_results_loaded(self, issues):
        """Maneja los resultados de búsqueda"""
        self.search_results_list.clear()
        
        if not issues:
            self.search_results_list.addItem("📭 No se encontraron resultados")
            return
            
        for issue in issues:
            item = QListWidgetItem()
            
            # Información del issue
            key = issue.get('key', 'N/A')
            summary = issue.get('summary', 'Sin título')
            status = issue.get('status', 'N/A')
            assignee = issue.get('assignee', 'Sin asignar')
            
            # Texto del item
            item_text = f"🔧 {key} - {summary}\n📊 {status} | 👤 {assignee}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, issue)
            
            self.search_results_list.addItem(item)
    
    def on_issue_selected(self, item):
        """Maneja la selección de un issue en mis tareas"""
        self.show_issue_details(item, self.my_issue_details)
    
    def on_project_issue_selected(self, item):
        """Maneja la selección de un issue en proyectos"""
        self.show_issue_details(item, self.project_issue_details)
    
    def on_search_result_selected(self, item):
        """Maneja la selección de un resultado de búsqueda"""
        self.show_issue_details(item, self.search_result_details)
    
    def show_issue_details(self, item, details_widget):
        """Muestra los detalles de un issue"""
        issue_data = item.data(Qt.ItemDataRole.UserRole)
        
        if not issue_data:
            return
            
        # Mostrar detalles completos del issue
        details = f"""🔧 {issue_data.get('key', 'N/A')} - {issue_data.get('issue_type', 'N/A')}
🔗 {issue_data.get('url', 'N/A')}

📝 Título:
{issue_data.get('summary', 'Sin título')}

📄 Descripción:
{issue_data.get('description', 'Sin descripción')[:200]}{'...' if len(issue_data.get('description', '')) > 200 else ''}

📊 Estado: {issue_data.get('status', 'N/A')}
⚡ Prioridad: {issue_data.get('priority', 'N/A')}
📁 Proyecto: {issue_data.get('project_name', issue_data.get('project', 'N/A'))}
👤 Asignado a: {issue_data.get('assignee', 'Sin asignar')}
📝 Reportado por: {issue_data.get('reporter', 'Desconocido')}
📅 Creado: {issue_data.get('created', 'N/A')}
🔄 Actualizado: {issue_data.get('updated', 'N/A')}"""

        details_widget.setText(details)
    
    def on_error(self, error_msg):
        """Maneja errores generales"""
        QMessageBox.critical(self, "❌ Error", f"Error en Jira:\n{error_msg}")
    
    def clear_fields(self):
        """Limpia los campos de entrada"""
        self.server_input.clear()
        self.user_input.clear()
        self.token_input.clear()
    
    def disconnect(self):
        """Desconecta de Jira"""
        self.jira_service.disconnect()
        
        # Resetear UI
        self.connection_status.setText("❌ No conectado a Jira")
        self.connection_status.setStyleSheet("color: #ff6b6b; padding: 10px;")
        
        self.issues_frame.hide()
        self.login_frame.show()
        
        # Limpiar todos los widgets
        self.clear_fields()
        if hasattr(self, 'my_issues_list'):
            self.my_issues_list.clear()
        if hasattr(self, 'my_issue_details'):
            self.my_issue_details.clear()
        if hasattr(self, 'project_combo'):
            self.project_combo.clear()
        if hasattr(self, 'project_issues_list'):
            self.project_issues_list.clear()
        if hasattr(self, 'project_issue_details'):
            self.project_issue_details.clear()
        if hasattr(self, 'search_input'):
            self.search_input.clear()
        if hasattr(self, 'search_results_list'):
            self.search_results_list.clear()
        if hasattr(self, 'search_result_details'):
            self.search_result_details.clear()
        
        QMessageBox.information(self, "🚪 Desconectado", 
                              "Te has desconectado de Jira exitosamente.")
