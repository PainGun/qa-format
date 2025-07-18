"""
Widget de Jira para la aplicación QA Generator
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QListWidget, QTextEdit,
                           QMessageBox, QFrame, QScrollArea, QListWidgetItem,
                           QTabWidget, QComboBox, QSplitter, QTreeWidget,
                           QTreeWidgetItem, QProgressBar, QMenu)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QAction
from jira_service import JiraService
from jira_status_dialog import JiraStatusDialog
from styles import ThemeManager

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
        
        # Registrar para cambios de tema
        ThemeManager.register_theme_changed_callback(self.on_theme_changed)
        
        self.setup_ui()
        
    def on_theme_changed(self, theme_name):
        """Callback cuando cambia el tema"""
        self.apply_theme_to_widgets()
        
    def apply_theme_to_widgets(self):
        """Aplica el tema actual a todos los widgets"""
        theme_class = ThemeManager.get_theme_class()
        
        # Aplicar tema a widgets existentes
        widgets_to_update = [
            # Frame principales
            (getattr(self, 'login_frame', None), 'frame'),
            (getattr(self, 'issues_frame', None), 'frame'),
            (getattr(self, 'tabs', None), 'frame'),
            
            # Inputs y campos
            (getattr(self, 'server_input', None), 'lineedit'),
            (getattr(self, 'username_input', None), 'lineedit'),
            (getattr(self, 'token_input', None), 'lineedit'),
            (getattr(self, 'search_input', None), 'lineedit'),
            
            # Botones
            (getattr(self, 'login_btn', None), 'button'),
            (getattr(self, 'refresh_btn', None), 'button'),
            (getattr(self, 'search_btn', None), 'button'),
            
            # Listas
            (getattr(self, 'issues_list', None), 'listwidget'),
            (getattr(self, 'projects_list', None), 'listwidget'),
            
            # Áreas de texto
            (getattr(self, 'issue_details', None), 'textedit'),
            
            # Labels
            (getattr(self, 'connection_status', None), 'label'),
        ]
        
        for widget, widget_type in widgets_to_update:
            if widget:
                style_method = getattr(theme_class, f'get_{widget_type}_style', None)
                if style_method:
                    widget.setStyleSheet(style_method())
        
        # Aplicar colores específicos al connection_status
        if hasattr(self, 'connection_status'):
            if ThemeManager.get_current_theme() == 'dark':
                if "No conectado" in self.connection_status.text():
                    self.connection_status.setStyleSheet("color: #ff5555; padding: 10px; background-color: transparent;")
                else:
                    self.connection_status.setStyleSheet("color: #50fa7b; padding: 10px; background-color: transparent;")
            else:
                if "No conectado" in self.connection_status.text():
                    self.connection_status.setStyleSheet("color: #ff6b6b; padding: 10px; background-color: transparent;")
                else:
                    self.connection_status.setStyleSheet("color: #28A745; padding: 10px; background-color: transparent;")
        
        # Forzar actualización visual
        self.update()
        
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
        frame.setStyleSheet(ThemeManager.get_theme_class().get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("🔧 Jira Integration")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3D3D3D; margin-bottom: 10px;")
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
        server_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        layout.addWidget(server_label)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("https://tuempresa.atlassian.net")
        self.server_input.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        layout.addWidget(self.server_input)
        
        # Campo de usuario
        user_label = QLabel("👤 Email/Usuario:")
        user_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        layout.addWidget(user_label)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("tu.email@empresa.com")
        self.user_input.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        layout.addWidget(self.user_input)
        
        # Campo de token
        token_label = QLabel("🔑 API Token:")
        token_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        layout.addWidget(token_label)
        
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("API Token de Jira")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
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
        self.login_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        buttons_layout.addWidget(self.login_btn)
        
        cancel_btn = QPushButton("❌ Limpiar")
        cancel_btn.clicked.connect(self.clear_fields)
        cancel_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        return frame
        
    def create_issues_frame(self):
        """Crea el frame de issues con pestañas"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(ThemeManager.get_theme_class().get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("🔧 Tareas de Jira")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3D3D3D; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Sistema de pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(ThemeManager.get_theme_class().get_frame_style())
        
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
        disconnect_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
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
        refresh_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        layout.addWidget(refresh_btn)
        
        # Filtro por estado
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("🏷️ Filtrar por estado:")
        filter_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        filter_layout.addWidget(filter_label)
        
        self.status_filter = QComboBox()
        self.status_filter.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        self.status_filter.addItem("🔎 Todos los estados")
        self.status_filter.addItem("📋 To Do")
        self.status_filter.addItem("⚡ In Progress")
        self.status_filter.addItem("👀 In Review")
        self.status_filter.addItem("🧪 Testing")
        self.status_filter.addItem("✅ Done")
        self.status_filter.addItem("❌ Cancelled")
        self.status_filter.addItem("🔄 Reopened")
        self.status_filter.addItem("📝 Ready for Review")
        self.status_filter.addItem("🚀 Ready for Deploy")
        self.status_filter.currentTextChanged.connect(self.filter_issues_by_status)
        filter_layout.addWidget(self.status_filter)
        
        # Botón para limpiar filtro
        clear_filter_btn = QPushButton("🗑️ Limpiar")
        clear_filter_btn.clicked.connect(self.clear_status_filter)
        clear_filter_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        filter_layout.addWidget(clear_filter_btn)
        
        filter_layout.addStretch()  # Empujar hacia la izquierda
        layout.addLayout(filter_layout)
        
        # Lista de mis issues
        self.my_issues_list = QListWidget()
        self.my_issues_list.setStyleSheet(ThemeManager.get_theme_class().get_listwidget_style())
        self.my_issues_list.itemClicked.connect(self.on_issue_selected)
        self.my_issues_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.my_issues_list.customContextMenuRequested.connect(self.show_issue_context_menu)
        layout.addWidget(self.my_issues_list)
        
        # Área de detalles del issue
        self.my_issue_details = QTextEdit()
        self.my_issue_details.setMaximumHeight(150)
        self.my_issue_details.setReadOnly(True)
        self.my_issue_details.setStyleSheet(ThemeManager.get_theme_class().get_textedit_style())
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
        refresh_projects_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        layout.addWidget(refresh_projects_btn)
        
        # Selector de proyecto
        project_label = QLabel("📁 Selecciona un proyecto:")
        project_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        layout.addWidget(project_label)
        
        self.project_combo = QComboBox()
        self.project_combo.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        self.project_combo.currentTextChanged.connect(self.on_project_selected)
        layout.addWidget(self.project_combo)
        
        # Lista de issues del proyecto
        self.project_issues_list = QListWidget()
        self.project_issues_list.setStyleSheet(ThemeManager.get_theme_class().get_listwidget_style())
        self.project_issues_list.itemClicked.connect(self.on_project_issue_selected)
        self.project_issues_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.project_issues_list.customContextMenuRequested.connect(self.show_project_issue_context_menu)
        layout.addWidget(self.project_issues_list)
        
        # Área de detalles del issue del proyecto
        self.project_issue_details = QTextEdit()
        self.project_issue_details.setMaximumHeight(150)
        self.project_issue_details.setReadOnly(True)
        self.project_issue_details.setStyleSheet(ThemeManager.get_theme_class().get_textedit_style())
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
        search_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Ejemplo: project = "PROJ" AND status = "In Progress"')
        self.search_input.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        layout.addWidget(self.search_input)
        
        # Botón de búsqueda
        search_btn = QPushButton("🔍 Buscar")
        search_btn.clicked.connect(self.search_issues)
        search_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        layout.addWidget(search_btn)
        
        # Lista de resultados de búsqueda
        self.search_results_list = QListWidget()
        self.search_results_list.setStyleSheet(ThemeManager.get_theme_class().get_listwidget_style())
        self.search_results_list.itemClicked.connect(self.on_search_result_selected)
        layout.addWidget(self.search_results_list)
        
        # Área de detalles del resultado
        self.search_result_details = QTextEdit()
        self.search_result_details.setMaximumHeight(150)
        self.search_result_details.setReadOnly(True)
        self.search_result_details.setStyleSheet(ThemeManager.get_theme_class().get_textedit_style())
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
            self.all_issues = []
            return
        
        # Guardar todos los issues para el filtrado
        self.all_issues = issues
        
        # Actualizar opciones de filtro con estados únicos encontrados
        if hasattr(self, 'status_filter'):
            current_text = self.status_filter.currentText()
            self.status_filter.clear()
            self.status_filter.addItem("Todos los estados")
            
            # Obtener estados únicos
            unique_statuses = set(issue.get('status', '') for issue in issues if issue.get('status'))
            for status in sorted(unique_statuses):
                self.status_filter.addItem(status)
            
            # Restaurar selección anterior si existe
            index = self.status_filter.findText(current_text)
            if index >= 0:
                self.status_filter.setCurrentIndex(index)
        
        # Aplicar filtro actual
        self.filter_issues_by_status()
    
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
    
    def show_issue_context_menu(self, position):
        """Muestra el menú contextual para los issues asignados"""
        item = self.my_issues_list.itemAt(position)
        if not item:
            return
            
        issue_data = item.data(Qt.ItemDataRole.UserRole)
        if not issue_data:
            return
        
        menu = QMenu(self)
        menu.setStyleSheet(ThemeManager.get_theme_class().get_frame_style())
        
        # Acción para cambiar estado
        change_status_action = QAction("🔄 Cambiar Estado", self)
        change_status_action.triggered.connect(lambda: self.change_issue_status(issue_data))
        menu.addAction(change_status_action)
        
        # Acción para abrir en navegador
        open_action = QAction("🌐 Abrir en Jira", self)
        open_action.triggered.connect(lambda: self.open_issue_in_browser(issue_data))
        menu.addAction(open_action)
        
        # Acción para copiar URL
        copy_url_action = QAction("📋 Copiar URL", self)
        copy_url_action.triggered.connect(lambda: self.copy_issue_url(issue_data))
        menu.addAction(copy_url_action)
        
        # Acción para refrescar
        menu.addSeparator()
        refresh_action = QAction("🔄 Refrescar", self)
        refresh_action.triggered.connect(self.load_my_issues)
        menu.addAction(refresh_action)
        
        menu.exec(self.my_issues_list.mapToGlobal(position))
    
    def show_project_issue_context_menu(self, position):
        """Muestra el menú contextual para los issues de proyecto"""
        item = self.project_issues_list.itemAt(position)
        if not item:
            return
            
        issue_data = item.data(Qt.ItemDataRole.UserRole)
        if not issue_data:
            return
        
        menu = QMenu(self)
        menu.setStyleSheet(ThemeManager.get_theme_class().get_frame_style())
        
        # Acción para cambiar estado
        change_status_action = QAction("🔄 Cambiar Estado", self)
        change_status_action.triggered.connect(lambda: self.change_issue_status(issue_data))
        menu.addAction(change_status_action)
        
        # Acción para abrir en navegador
        open_action = QAction("🌐 Abrir en Jira", self)
        open_action.triggered.connect(lambda: self.open_issue_in_browser(issue_data))
        menu.addAction(open_action)
        
        # Acción para copiar URL
        copy_url_action = QAction("📋 Copiar URL", self)
        copy_url_action.triggered.connect(lambda: self.copy_issue_url(issue_data))
        menu.addAction(copy_url_action)
        
        menu.exec(self.project_issues_list.mapToGlobal(position))
    
    def change_issue_status(self, issue_data):
        """Abre el diálogo para cambiar el estado del issue"""
        try:
            dialog = JiraStatusDialog(self, self.jira_service, issue_data)
            dialog.status_changed.connect(self.on_issue_status_changed)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error abriendo diálogo de estado:\n{str(e)}")
    
    def on_issue_status_changed(self, issue_key, new_status):
        """Maneja el cambio de estado exitoso"""
        # Actualizar el estado en las listas
        self.update_issue_status_in_lists(issue_key, new_status)
        
        # Recargar las listas para obtener datos actualizados
        self.load_my_issues()
        
        # Si hay un proyecto seleccionado, recargar también
        current_project = self.projects_combo.currentText()
        if current_project and not current_project.startswith(("Selecciona", "🔄", "📭", "❌")):
            project_data = self.projects_combo.itemData(self.projects_combo.currentIndex())
            if project_data:
                self.load_project_issues(project_data['key'])
    
    def update_issue_status_in_lists(self, issue_key, new_status):
        """Actualiza el estado del issue en las listas sin recargar"""
        # Actualizar en my_issues_list
        for i in range(self.my_issues_list.count()):
            item = self.my_issues_list.item(i)
            issue_data = item.data(Qt.ItemDataRole.UserRole)
            if issue_data and issue_data['key'] == issue_key:
                issue_data['status'] = new_status
                # Actualizar el texto del item
                priority_icon = self.get_priority_icon(issue_data.get('priority', ''))
                status_icon = self.get_status_icon(new_status)
                item_text = f"{priority_icon} {issue_data['key']} - {issue_data['summary']}\n🏷️ {new_status} | 📋 {issue_data['issue_type']}"
                item.setText(item_text)
                break
        
        # Actualizar en project_issues_list
        for i in range(self.project_issues_list.count()):
            item = self.project_issues_list.item(i)
            issue_data = item.data(Qt.ItemDataRole.UserRole)
            if issue_data and issue_data['key'] == issue_key:
                issue_data['status'] = new_status
                # Actualizar el texto del item
                status_icon = self.get_status_icon(new_status)
                assignee = issue_data.get('assignee', 'Sin asignar')
                item_text = f"{status_icon} {issue_data['key']} - {issue_data['summary']}\n👤 {assignee} | 🏷️ {new_status}"
                item.setText(item_text)
                break
    
    def open_issue_in_browser(self, issue_data):
        """Abre el issue en el navegador"""
        import webbrowser
        try:
            webbrowser.open(issue_data['url'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el navegador:\n{str(e)}")
    
    def copy_issue_url(self, issue_data):
        """Copia la URL del issue al portapapeles"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(issue_data['url'])
        QMessageBox.information(self, "Copiado", f"URL del issue {issue_data['key']} copiada al portapapeles")
    
    def get_priority_icon(self, priority):
        """Obtiene el icono según la prioridad"""
        priority_icons = {
            'Highest': '🔥',
            'High': '⚡',
            'Medium': '📋',
            'Low': '📝',
            'Lowest': '💤'
        }
        return priority_icons.get(priority, '📋')
    
    def get_status_icon(self, status):
        """Obtiene el icono según el estado"""
        status_icons = {
            'To Do': '📝',
            'In Progress': '🔄',
            'Done': '✅',
            'Closed': '🔒',
            'Open': '📂',
            'Resolved': '✔️',
            'Reopened': '🔄'
        }
        return status_icons.get(status, '📋')

    def filter_issues_by_status(self):
        """Filtra los issues por el estado seleccionado"""
        if not hasattr(self, 'all_issues'):
            return
            
        selected_status = self.status_filter.currentText()
        
        # Limpiar lista actual
        self.my_issues_list.clear()
        
        # Si es "Todos los estados", mostrar todos
        if selected_status == "Todos los estados":
            issues_to_show = self.all_issues
        else:
            # Filtrar por estado
            issues_to_show = [issue for issue in self.all_issues 
                            if issue.get('status', '') == selected_status]
        
        # Agregar issues filtrados a la lista
        for issue in issues_to_show:
            status_icon = self.get_status_icon(issue.get('status', ''))
            priority_icon = self.get_priority_icon(issue.get('priority', ''))
            
            item_text = f"{status_icon} {priority_icon} {issue['key']}: {issue['summary']}"
            item = QListWidgetItem(item_text)
            item.setData(256, issue)  # Guardamos los datos del issue
            
            # Aplicar estilos según el tema actual
            if hasattr(self, 'theme_manager') and self.theme_manager:
                current_theme = self.theme_manager.get_current_theme()
                item.setBackground(QColor(current_theme.list_item_background))
                item.setForeground(QColor(current_theme.text_color))
            
            self.my_issues_list.addItem(item)
    
    def clear_status_filter(self):
        """Limpia el filtro de estado y muestra todos los issues"""
        self.status_filter.setCurrentText("Todos los estados")
        self.filter_issues_by_status()
