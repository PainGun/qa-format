"""
Widget de GitHub para la aplicación QA Generator
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QListWidget, QTextEdit,
                           QMessageBox, QFrame, QScrollArea, QListWidgetItem,
                           QTabWidget, QComboBox, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from github_service import GitHubService
from styles import DarkTheme

class GitHubWorker(QThread):
    """Worker thread para operaciones de GitHub"""
    repos_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, service):
        super().__init__()
        self.service = service
        
    def run(self):
        try:
            repos = self.service.get_user_repositories()
            self.repos_loaded.emit(repos)
        except Exception as e:
            self.error_occurred.emit(str(e))

class OrganizationsWorker(QThread):
    """Worker thread para obtener organizaciones"""
    orgs_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, service):
        super().__init__()
        self.service = service
        
    def run(self):
        try:
            orgs = self.service.get_user_organizations()
            self.orgs_loaded.emit(orgs)
        except Exception as e:
            self.error_occurred.emit(str(e))

class OrgReposWorker(QThread):
    """Worker thread para obtener repositorios de una organización"""
    repos_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, service, org_login):
        super().__init__()
        self.service = service
        self.org_login = org_login
        
    def run(self):
        try:
            repos = self.service.get_organization_repositories(self.org_login)
            self.repos_loaded.emit(repos)
        except Exception as e:
            self.error_occurred.emit(str(e))

class GitHubWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.github_service = GitHubService()
        self.worker = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Estado de conexión
        self.connection_status = QLabel("❌ No conectado a GitHub")
        self.connection_status.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.connection_status.setStyleSheet("color: #ff6b6b; padding: 10px;")
        layout.addWidget(self.connection_status)
        
        # Frame de login
        self.login_frame = self.create_login_frame()
        layout.addWidget(self.login_frame)
        
        # Frame de repositorios (inicialmente oculto)
        self.repos_frame = self.create_repos_frame()
        self.repos_frame.hide()
        layout.addWidget(self.repos_frame)
        
    def create_login_frame(self):
        """Crea el frame de login"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(DarkTheme.get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("🐙 GitHub Integration")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f8f8f2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Instrucciones COMPLETAS
        instructions = QLabel("""Para conectar con GitHub necesitas un Personal Access Token:

1. 🌐 Ve a GitHub.com → Settings → Developer Settings
2. 🔑 Personal Access Tokens → Tokens (classic)
3. ⚡ Generate new token (classic)
4. ✅ Selecciona permisos: repo, read:user, read:org
5. 📋 Copia el token generado

⚠️ Para ver organizaciones necesitas el permiso 'read:org'""")
        
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
        
        # Campo de token
        token_label = QLabel("🔑 Personal Access Token:")
        token_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(token_label)
        
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("ghp_...")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setStyleSheet(DarkTheme.get_lineedit_style())
        layout.addWidget(self.token_input)
        
        # Link para generar token
        link_label = QLabel('🔗 <a href="https://github.com/settings/tokens" style="color: #50fa7b;">Generar Token en GitHub</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(link_label)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("🔑 Iniciar Sesión")
        self.login_btn.clicked.connect(self.login_to_github)
        self.login_btn.setStyleSheet(DarkTheme.get_button_style())
        buttons_layout.addWidget(self.login_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.clear_token)
        cancel_btn.setStyleSheet(DarkTheme.get_button_style())
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        return frame
        
    def create_repos_frame(self):
        """Crea el frame de repositorios con pestañas para usuario y organizaciones"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(DarkTheme.get_frame_style())
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("📂 Repositorios de GitHub")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f8f8f2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Sistema de pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(DarkTheme.get_frame_style())
        
        # Pestaña de repositorios personales
        self.user_repos_tab = self.create_user_repos_tab()
        self.tabs.addTab(self.user_repos_tab, "👤 Mis Repos")
        
        # Pestaña de organizaciones
        self.orgs_tab = self.create_organizations_tab()
        self.tabs.addTab(self.orgs_tab, "🏢 Organizaciones")
        
        layout.addWidget(self.tabs)
        
        # Botón para desconectar
        disconnect_btn = QPushButton("🚪 Cerrar Sesión")
        disconnect_btn.clicked.connect(self.logout)
        disconnect_btn.setStyleSheet(DarkTheme.get_button_style())
        layout.addWidget(disconnect_btn)
        
        return frame
    
    def create_user_repos_tab(self):
        """Crea la pestaña de repositorios del usuario"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Lista de repositorios del usuario
        self.user_repos_list = QListWidget()
        self.user_repos_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.user_repos_list.itemClicked.connect(self.on_repo_selected)
        layout.addWidget(self.user_repos_list)
        
        # Área de detalles del repositorio
        self.user_repo_details = QTextEdit()
        self.user_repo_details.setMaximumHeight(150)
        self.user_repo_details.setReadOnly(True)
        self.user_repo_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.user_repo_details.setPlaceholderText("Selecciona un repositorio para ver sus detalles...")
        layout.addWidget(self.user_repo_details)
        
        return tab
    
    def create_organizations_tab(self):
        """Crea la pestaña de organizaciones"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Selector de organización
        org_label = QLabel("🏢 Selecciona una organización:")
        org_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(org_label)
        
        # Layout para combo y botón de recarga
        org_layout = QHBoxLayout()
        
        self.org_combo = QComboBox()
        self.org_combo.setStyleSheet(DarkTheme.get_lineedit_style())
        self.org_combo.currentTextChanged.connect(self.on_org_selected)
        org_layout.addWidget(self.org_combo)
        
        # Botón para recargar organizaciones
        reload_orgs_btn = QPushButton("🔄")
        reload_orgs_btn.setMaximumWidth(40)
        reload_orgs_btn.setToolTip("Recargar organizaciones")
        reload_orgs_btn.clicked.connect(self.load_organizations)
        reload_orgs_btn.setStyleSheet(DarkTheme.get_button_style())
        org_layout.addWidget(reload_orgs_btn)
        
        layout.addLayout(org_layout)
        
        # Lista de repositorios de la organización
        self.org_repos_list = QListWidget()
        self.org_repos_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.org_repos_list.itemClicked.connect(self.on_org_repo_selected)
        layout.addWidget(self.org_repos_list)
        
        # Área de detalles del repositorio de la organización
        self.org_repo_details = QTextEdit()
        self.org_repo_details.setMaximumHeight(150)
        self.org_repo_details.setReadOnly(True)
        self.org_repo_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.org_repo_details.setPlaceholderText("Selecciona una organización y un repositorio...")
        layout.addWidget(self.org_repo_details)
        
        return tab
    
    def login_to_github(self):
        """Intenta hacer login a GitHub"""
        token = self.token_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, "⚠️ Token Requerido", 
                              "Por favor ingresa tu Personal Access Token de GitHub")
            return
            
        self.login_btn.setText("🔄 Conectando...")
        self.login_btn.setEnabled(False)
        
        try:
            if self.github_service.authenticate(token):
                user_info = self.github_service.get_user_info()
                
                self.connection_status.setText(f"✅ Conectado como: {user_info.get('name', user_info.get('login', 'Usuario'))}")
                self.connection_status.setStyleSheet("color: #50fa7b; padding: 10px;")
                
                # Ocultar login y mostrar repositorios
                self.login_frame.hide()
                self.repos_frame.show()
                
                # Cargar repositorios del usuario y organizaciones
                self.load_repositories()
                self.load_organizations()
                
            else:
                QMessageBox.critical(self, "❌ Error de Autenticación", 
                                   "Token inválido. Verifica tu Personal Access Token.")
                
        except Exception as e:
            QMessageBox.critical(self, "❌ Error de Conexión", 
                               f"No se pudo conectar a GitHub:\n{str(e)}")
        finally:
            self.login_btn.setText("🔑 Iniciar Sesión")
            self.login_btn.setEnabled(True)
    
    def load_repositories(self):
        """Carga los repositorios del usuario"""
        if self.worker and self.worker.isRunning():
            return
            
        self.user_repos_list.clear()
        self.user_repos_list.addItem("🔄 Cargando repositorios...")
        
        self.worker = GitHubWorker(self.github_service)
        self.worker.repos_loaded.connect(self.on_user_repos_loaded)
        self.worker.error_occurred.connect(self.on_user_repos_error)
        self.worker.start()
    
    def load_organizations(self):
        """Carga las organizaciones del usuario"""
        self.org_combo.clear()
        self.org_combo.addItem("🔄 Cargando organizaciones...")
        
        self.org_worker = OrganizationsWorker(self.github_service)
        self.org_worker.orgs_loaded.connect(self.on_orgs_loaded)
        self.org_worker.error_occurred.connect(self.on_orgs_error)
        self.org_worker.start()
    
    def on_user_repos_loaded(self, repos):
        """Maneja la carga exitosa de repositorios del usuario"""
        self.user_repos_list.clear()
        
        if not repos:
            self.user_repos_list.addItem("📭 No se encontraron repositorios")
            return
            
        for repo in repos:
            item = QListWidgetItem()
            
            # Información básica del repositorio
            name = repo.get('name', 'Sin nombre')
            description = repo.get('description', 'Sin descripción')
            private = "🔒" if repo.get('private', False) else "🌐"
            language = repo.get('language', 'N/A')
            stars = repo.get('stargazers_count', 0)
            
            # Texto completo del item (sin truncar)
            item_text = f"{private} {name}\n💬 {description}\n🔤 {language} | ⭐ {stars}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, repo)
            
            self.user_repos_list.addItem(item)
    
    def on_user_repos_error(self, error_msg):
        """Maneja errores al cargar repositorios del usuario"""
        self.user_repos_list.clear()
        self.user_repos_list.addItem(f"❌ Error: {error_msg}")
    
    def on_orgs_loaded(self, orgs):
        """Maneja la carga exitosa de organizaciones"""
        self.org_combo.clear()
        
        if not orgs:
            self.org_combo.addItem("📭 No perteneces a organizaciones")
            return
        
        self.org_combo.addItem("Selecciona una organización...")
        for org in orgs:
            org_text = f"🏢 {org.get('name', org.get('login', 'Sin nombre'))}"
            self.org_combo.addItem(org_text)
            # Guardar datos de la org en el combo
            self.org_combo.setItemData(self.org_combo.count() - 1, org)
    
    def on_orgs_error(self, error_msg):
        """Maneja errores al cargar organizaciones"""
        self.org_combo.clear()
        print(f"Error cargando organizaciones: {error_msg}")
        
        if "403" in error_msg or "Forbidden" in error_msg:
            self.org_combo.addItem("❌ Token sin permisos para organizaciones")
        elif "organizations" in error_msg.lower():
            self.org_combo.addItem("📭 No perteneces a organizaciones")
        else:
            self.org_combo.addItem(f"❌ Error: {error_msg}")
    
    def on_org_selected(self, org_text):
        """Maneja la selección de una organización"""
        if org_text.startswith("🔄") or org_text.startswith("📭") or org_text.startswith("❌") or org_text.startswith("Selecciona"):
            return
        
        # Obtener datos de la organización
        current_index = self.org_combo.currentIndex()
        org_data = self.org_combo.itemData(current_index)
        
        if not org_data:
            return
        
        org_login = org_data.get('login')
        if org_login:
            self.load_org_repositories(org_login)
    
    def load_org_repositories(self, org_login):
        """Carga repositorios de una organización específica"""
        self.org_repos_list.clear()
        self.org_repos_list.addItem(f"🔄 Cargando repositorios de {org_login}...")
        
        self.org_repos_worker = OrgReposWorker(self.github_service, org_login)
        self.org_repos_worker.repos_loaded.connect(self.on_org_repos_loaded)
        self.org_repos_worker.error_occurred.connect(self.on_org_repos_error)
        self.org_repos_worker.start()
    
    def on_org_repos_loaded(self, repos):
        """Maneja la carga exitosa de repositorios de organización"""
        self.org_repos_list.clear()
        
        if not repos:
            self.org_repos_list.addItem("📭 No se encontraron repositorios en esta organización")
            return
            
        for repo in repos:
            item = QListWidgetItem()
            
            # Información básica del repositorio
            name = repo.get('name', 'Sin nombre')
            description = repo.get('description', 'Sin descripción')
            private = "🔒" if repo.get('private', False) else "🌐"
            language = repo.get('language', 'N/A')
            stars = repo.get('stargazers_count', 0)
            
            # Texto completo del item (sin truncar)
            item_text = f"{private} {name}\n💬 {description}\n🔤 {language} | ⭐ {stars}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, repo)
            
            self.org_repos_list.addItem(item)
    
    def on_org_repos_error(self, error_msg):
        """Maneja errores al cargar repositorios de organización"""
        self.org_repos_list.clear()
        self.org_repos_list.addItem(f"❌ Error: {error_msg}")
    
    def on_org_repo_selected(self, item):
        """Maneja la selección de un repositorio de organización"""
        repo_data = item.data(Qt.ItemDataRole.UserRole)
        
        if not repo_data:
            return
            
        # Mostrar detalles completos del repositorio
        details = f"""📂 {repo_data.get('name', 'N/A')} (🏢 {repo_data.get('organization', 'N/A')})
🔗 {repo_data.get('html_url', 'N/A')}

📝 Descripción:
{repo_data.get('description', 'Sin descripción disponible')}

📊 Estadísticas:
• 🔤 Lenguaje: {repo_data.get('language', 'N/A')}
• ⭐ Stars: {repo_data.get('stargazers_count', 0)}
• 🍴 Forks: {repo_data.get('forks_count', 0)}
• 👁️ Watchers: {repo_data.get('watchers_count', 0)}
• 📅 Creado: {repo_data.get('created_at', 'N/A')[:10]}
• 🔄 Actualizado: {repo_data.get('updated_at', 'N/A')[:10]}

🔒 Privado: {'Sí' if repo_data.get('private', False) else 'No'}
📋 Fork: {'Sí' if repo_data.get('fork', False) else 'No'}"""

        self.org_repo_details.setText(details)
    
    def on_repo_selected(self, item):
        """Maneja la selección de un repositorio del usuario"""
        repo_data = item.data(Qt.ItemDataRole.UserRole)
        
        if not repo_data:
            return
            
        # Mostrar detalles completos del repositorio
        details = f"""📂 {repo_data.get('name', 'N/A')}
🔗 {repo_data.get('html_url', 'N/A')}

📝 Descripción:
{repo_data.get('description', 'Sin descripción disponible')}

📊 Estadísticas:
• 🔤 Lenguaje: {repo_data.get('language', 'N/A')}
• ⭐ Stars: {repo_data.get('stargazers_count', 0)}
• 🍴 Forks: {repo_data.get('forks_count', 0)}
• 👁️ Watchers: {repo_data.get('watchers_count', 0)}
• 📅 Creado: {repo_data.get('created_at', 'N/A')[:10]}
• 🔄 Actualizado: {repo_data.get('updated_at', 'N/A')[:10]}

🔒 Privado: {'Sí' if repo_data.get('private', False) else 'No'}
📋 Fork: {'Sí' if repo_data.get('fork', False) else 'No'}"""

        self.user_repo_details.setText(details)
    
    def clear_token(self):
        """Limpia el campo de token"""
        self.token_input.clear()
    
    def logout(self):
        """Cierra la sesión de GitHub"""
        self.github_service.logout()
        
        # Resetear UI
        self.connection_status.setText("❌ No conectado a GitHub")
        self.connection_status.setStyleSheet("color: #ff6b6b; padding: 10px;")
        
        self.repos_frame.hide()
        self.login_frame.show()
        
        self.token_input.clear()
        
        # Limpiar todos los widgets
        if hasattr(self, 'user_repos_list'):
            self.user_repos_list.clear()
        if hasattr(self, 'user_repo_details'):
            self.user_repo_details.clear()
        if hasattr(self, 'org_combo'):
            self.org_combo.clear()
        if hasattr(self, 'org_repos_list'):
            self.org_repos_list.clear()
        if hasattr(self, 'org_repo_details'):
            self.org_repo_details.clear()
        
        QMessageBox.information(self, "🚪 Sesión Cerrada", 
                              "Has cerrado sesión de GitHub exitosamente.")
