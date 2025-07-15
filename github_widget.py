"""
Widget de GitHub para la aplicación QA Generator
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QListWidget, QTextEdit,
                           QMessageBox, QFrame, QScrollArea, QListWidgetItem,
                           QTabWidget, QComboBox, QSplitter, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath
from github_service import GitHubService, GitHubAvatarWorker
from github_branch_service import GitHubBranchesWorker, GitHubCreateBranchWorker
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

class BranchManagerDialog(QDialog):
    """Diálogo para gestionar ramas de un repositorio"""
    
    def __init__(self, github_service, repo_full_name, repo_name, parent=None):
        super().__init__(parent)
        self.github_service = github_service
        self.repo_full_name = repo_full_name
        self.repo_name = repo_name
        self.current_branches = []
        self.active_workers = []  # Lista para rastrear workers activos
        self.setup_ui()
        self.load_branches()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setWindowTitle(f"🌿 Gestión de Ramas - {self.repo_name}")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"🌿 Ramas del repositorio: {self.repo_name}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3D3D3D; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.clicked.connect(self.load_branches)
        self.refresh_btn.setStyleSheet(DarkTheme.get_button_style())
        actions_layout.addWidget(self.refresh_btn)
        
        self.create_branch_btn = QPushButton("➕ Nueva Rama")
        self.create_branch_btn.clicked.connect(self.show_create_branch_dialog)
        self.create_branch_btn.setStyleSheet(DarkTheme.get_button_style())
        actions_layout.addWidget(self.create_branch_btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        # Lista de ramas
        self.branches_list = QListWidget()
        self.branches_list.setStyleSheet(DarkTheme.get_listwidget_style())
        self.branches_list.itemClicked.connect(self.on_branch_selected)
        layout.addWidget(self.branches_list)
        
        # Detalles de la rama seleccionada
        details_label = QLabel("📋 Detalles de la rama:")
        details_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(details_label)
        
        self.branch_details = QTextEdit()
        self.branch_details.setMaximumHeight(150)
        self.branch_details.setReadOnly(True)
        self.branch_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.branch_details.setPlaceholderText("Selecciona una rama para ver sus detalles...")
        layout.addWidget(self.branch_details)
        
        # Botones del diálogo
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)
    
    def load_branches(self):
        """Carga las ramas del repositorio"""
        self.branches_list.clear()
        self.branches_list.addItem("🔄 Cargando ramas...")
        self.refresh_btn.setEnabled(False)
        self.create_branch_btn.setEnabled(False)
        
        # Usar el worker del servicio de ramas
        worker = self.github_service.get_branches_async(self.repo_full_name)
        worker.branches_ready.connect(self.on_branches_loaded)
        worker.error_occurred.connect(self.on_branches_error)
        worker.finished.connect(lambda: self.active_workers.remove(worker) if worker in self.active_workers else None)
        self.active_workers.append(worker)  # Rastrear el worker
        worker.start()
    
    def on_branches_loaded(self, branches):
        """Maneja la carga exitosa de ramas"""
        self.current_branches = branches
        self.branches_list.clear()
        self.refresh_btn.setEnabled(True)
        self.create_branch_btn.setEnabled(True)
        
        if not branches:
            self.branches_list.addItem("📭 No se encontraron ramas")
            return
        
        for branch in branches:
            item = QListWidgetItem()
            
            # Información de la rama
            name = branch.get('name', 'Sin nombre')
            protected = "🛡️" if branch.get('protected', False) else "🌿"
            last_commit_author = branch.get('last_commit_author', 'Desconocido')
            last_commit_date = branch.get('last_commit_date', 'N/A')
            
            # Formatear fecha
            if last_commit_date != 'N/A':
                try:
                    from datetime import datetime
                    date_obj = datetime.fromisoformat(last_commit_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
                except:
                    formatted_date = last_commit_date[:10]
            else:
                formatted_date = 'N/A'
            
            # Texto del item
            item_text = f"{protected} {name}\n👤 {last_commit_author} • 📅 {formatted_date}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, branch)
            
            self.branches_list.addItem(item)
    
    def on_branches_error(self, error_msg):
        """Maneja errores al cargar ramas"""
        self.branches_list.clear()
        self.branches_list.addItem(f"❌ Error: {error_msg}")
        self.refresh_btn.setEnabled(True)
        self.create_branch_btn.setEnabled(True)
    
    def on_branch_selected(self, item):
        """Maneja la selección de una rama"""
        branch_data = item.data(Qt.ItemDataRole.UserRole)
        
        if not branch_data:
            return
        
        # Mostrar detalles de la rama
        name = branch_data.get('name', 'N/A')
        sha = branch_data.get('sha', 'N/A')
        protected = branch_data.get('protected', False)
        last_commit_sha = branch_data.get('last_commit_sha', 'N/A')
        last_commit_message = branch_data.get('last_commit_message', 'N/A')
        last_commit_author = branch_data.get('last_commit_author', 'N/A')
        last_commit_date = branch_data.get('last_commit_date', 'N/A')
        
        # Formatear fecha
        if last_commit_date != 'N/A':
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(last_commit_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%d de %B de 2023 a las %H:%M')
            except:
                formatted_date = last_commit_date
        else:
            formatted_date = 'N/A'
        
        details = f"""🌿 Rama: {name}
🛡️ Protegida: {'Sí' if protected else 'No'}
🔗 SHA: {sha[:12]}...

📝 Último commit:
• 🆔 {last_commit_sha}
• 💬 {last_commit_message}
• 👤 {last_commit_author}
• 📅 {formatted_date}"""
        
        self.branch_details.setText(details)
    
    def show_create_branch_dialog(self):
        """Muestra el diálogo para crear nueva rama"""
        dialog = CreateBranchDialog(self.github_service, self.repo_full_name, self.current_branches, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recargar ramas después de crear una nueva
            self.load_branches()

    def cleanup_threads(self):
        """Limpia todos los threads activos del diálogo"""
        for worker in self.active_workers[:]:  # Copiar lista para evitar modificación durante iteración
            if worker and worker.isRunning():
                try:
                    worker.quit()
                    if not worker.wait(2000):  # Esperar máximo 2 segundos
                        worker.terminate()
                        worker.wait()
                except:
                    pass  # Ignorar errores al cerrar threads
            if worker in self.active_workers:
                self.active_workers.remove(worker)
    
    def closeEvent(self, event):
        """Maneja el evento de cierre del diálogo"""
        self.cleanup_threads()
        super().closeEvent(event)

class CreateBranchDialog(QDialog):
    """Diálogo para crear una nueva rama"""
    
    def __init__(self, github_service, repo_full_name, current_branches, parent=None):
        super().__init__(parent)
        self.github_service = github_service
        self.repo_full_name = repo_full_name
        self.current_branches = current_branches
        self.active_workers = []  # Lista para rastrear workers activos
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setWindowTitle("➕ Crear Nueva Rama")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("➕ Crear Nueva Rama")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Nombre de la nueva rama
        name_label = QLabel("🏷️ Nombre de la nueva rama:")
        layout.addWidget(name_label)
        
        self.branch_name_input = QLineEdit()
        self.branch_name_input.setPlaceholderText("feature/nueva-funcionalidad")
        self.branch_name_input.setStyleSheet(DarkTheme.get_lineedit_style())
        self.branch_name_input.textChanged.connect(self.validate_branch_name)
        layout.addWidget(self.branch_name_input)
        
        # Validación del nombre
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("font-size: 12px; color: #ff6b6b;")
        layout.addWidget(self.validation_label)
        
        # Rama origen
        source_label = QLabel("🌱 Crear desde rama:")
        layout.addWidget(source_label)
        
        self.source_combo = QComboBox()
        self.source_combo.setStyleSheet(DarkTheme.get_lineedit_style())
        
        # Agregar ramas disponibles
        if self.current_branches:
            for branch in self.current_branches:
                branch_name = branch.get('name', '')
                if branch_name:
                    self.source_combo.addItem(f"🌿 {branch_name}", branch_name)
        
        layout.addWidget(self.source_combo)
        
        # Sugerencias
        suggestions_label = QLabel("💡 Sugerencias de nombres:")
        suggestions_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(suggestions_label)
        
        suggestions_text = QLabel("""• feature/nombre-funcionalidad
• hotfix/descripcion-bug
• release/version-numero
• bugfix/descripcion-arreglo""")
        suggestions_text.setStyleSheet("font-size: 11px; color: #6c757d; margin-left: 10px;")
        layout.addWidget(suggestions_text)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setText("✅ Crear Rama")
        self.ok_button.setEnabled(False)
        
        button_box.accepted.connect(self.create_branch)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def validate_branch_name(self):
        """Valida el nombre de la rama en tiempo real"""
        from github_branch_service import GitHubBranchValidator
        
        branch_name = self.branch_name_input.text().strip()
        
        if not branch_name:
            self.validation_label.setText("")
            self.ok_button.setEnabled(False)
            return
        
        # Validar con el validador
        validator = GitHubBranchValidator()
        is_valid, message = validator.validate_branch_name(branch_name)
        
        if is_valid:
            # Verificar si ya existe
            existing_names = [b.get('name', '') for b in self.current_branches]
            if branch_name in existing_names:
                self.validation_label.setText("⚠️ Esta rama ya existe")
                self.validation_label.setStyleSheet("font-size: 12px; color: #ffa500;")
                self.ok_button.setEnabled(False)
            else:
                self.validation_label.setText("✅ Nombre válido")
                self.validation_label.setStyleSheet("font-size: 12px; color: #50fa7b;")
                self.ok_button.setEnabled(True)
        else:
            self.validation_label.setText(f"❌ {message}")
            self.validation_label.setStyleSheet("font-size: 12px; color: #ff6b6b;")
            self.ok_button.setEnabled(False)
    
    def create_branch(self):
        """Crea la nueva rama"""
        branch_name = self.branch_name_input.text().strip()
        source_branch = self.source_combo.currentData()
        
        if not branch_name or not source_branch:
            QMessageBox.warning(self, "⚠️ Datos Incompletos", 
                              "Por favor completa todos los campos")
            return
        
        self.ok_button.setText("🔄 Creando...")
        self.ok_button.setEnabled(False)
        
        # Crear rama usando el worker asíncrono
        worker = self.github_service.create_branch_async(
            self.repo_full_name, 
            branch_name, 
            source_branch
        )
        worker.branch_created.connect(self.on_branch_created)
        worker.error_occurred.connect(self.on_branch_error)
        worker.finished.connect(lambda: self.active_workers.remove(worker) if worker in self.active_workers else None)
        self.active_workers.append(worker)  # Rastrear el worker
        worker.start()
    
    def on_branch_created(self, branch_name):
        """Maneja la creación exitosa de la rama"""
        QMessageBox.information(self, "✅ Rama Creada", 
                              f"La rama '{branch_name}' se creó exitosamente")
        self.accept()
    
    def on_branch_error(self, error_msg):
        """Maneja errores al crear la rama"""
        QMessageBox.critical(self, "❌ Error", 
                           f"No se pudo crear la rama:\n{error_msg}")
        self.ok_button.setText("✅ Crear Rama")
        self.ok_button.setEnabled(True)

    def cleanup_threads(self):
        """Limpia todos los threads activos del diálogo"""
        for worker in self.active_workers[:]:  # Copiar lista para evitar modificación durante iteración
            if worker and worker.isRunning():
                try:
                    worker.quit()
                    if not worker.wait(2000):  # Esperar máximo 2 segundos
                        worker.terminate()
                        worker.wait()
                except:
                    pass  # Ignorar errores al cerrar threads
            if worker in self.active_workers:
                self.active_workers.remove(worker)
    
    def closeEvent(self, event):
        """Maneja el evento de cierre del diálogo"""
        self.cleanup_threads()
        super().closeEvent(event)

class GitHubWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.github_service = GitHubService()
        self.worker = None
        self.avatar_worker = None
        self.selected_user_repo = None  # Almacenar repo seleccionado del usuario
        self.selected_org_repo = None   # Almacenar repo seleccionado de org
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Estado de conexión con avatar
        self.connection_frame = self.create_connection_frame()
        layout.addWidget(self.connection_frame)
        
        # Frame de login
        self.login_frame = self.create_login_frame()
        layout.addWidget(self.login_frame)
        
        # Frame de repositorios (inicialmente oculto)
        self.repos_frame = self.create_repos_frame()
        self.repos_frame.hide()
        layout.addWidget(self.repos_frame)
    
    def create_connection_frame(self):
        """Crea el frame que muestra el estado de conexión y avatar"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F7FA;
                border: 2px solid #A4B3DC;
                border-radius: 12px;
                padding: 8px;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(20)  # Más espacio entre elementos
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Avatar del usuario (inicialmente oculto)
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet("""
            QLabel {
                border: 4px solid #616DB3;
                border-radius: 40px;
                background-color: #FFFFFF;
                margin-right: 5px;
            }
            QLabel:hover {
                border: 4px solid #FACC53;
            }
        """)
        self.avatar_label.hide()
        layout.addWidget(self.avatar_label)
        
        # Contenedor para información del usuario
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(5)
        
        # Estado de conexión
        self.connection_status = QLabel("❌ No conectado a GitHub")
        self.connection_status.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.connection_status.setStyleSheet("color: #ff6b6b;")
        user_info_layout.addWidget(self.connection_status)
        
        # Label para información adicional del usuario (inicialmente oculto)
        self.user_info_label = QLabel()
        self.user_info_label.setFont(QFont("Arial", 10))
        self.user_info_label.setStyleSheet("color: #3D3D3D; margin-top: 2px;")
        self.user_info_label.hide()
        user_info_layout.addWidget(self.user_info_label)
        
        # Label para biografía del usuario (inicialmente oculto)
        self.user_bio_label = QLabel()
        self.user_bio_label.setFont(QFont("Arial", 9))
        self.user_bio_label.setStyleSheet("color: #616DB3; font-style: italic; margin-top: 1px;")
        self.user_bio_label.setWordWrap(True)  # Permitir que el texto se ajuste a múltiples líneas
        self.user_bio_label.hide()
        user_info_layout.addWidget(self.user_bio_label)
        
        layout.addLayout(user_info_layout)
        layout.addStretch()  # Para empujar el contenido hacia la izquierda
        
        return frame
        
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
        title.setStyleSheet("color: #3D3D3D; margin-bottom: 10px;")
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
        title.setStyleSheet("color: #3D3D3D; margin-bottom: 10px;")
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
        details_layout = QVBoxLayout()
        
        self.user_repo_details = QTextEdit()
        self.user_repo_details.setMaximumHeight(120)
        self.user_repo_details.setReadOnly(True)
        self.user_repo_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.user_repo_details.setPlaceholderText("Selecciona un repositorio para ver sus detalles...")
        details_layout.addWidget(self.user_repo_details)
        
        # Botón para ver ramas
        self.user_branches_btn = QPushButton("🌿 Ver Ramas")
        self.user_branches_btn.clicked.connect(self.show_user_repo_branches)
        self.user_branches_btn.setStyleSheet(DarkTheme.get_button_style())
        self.user_branches_btn.setEnabled(False)
        details_layout.addWidget(self.user_branches_btn)
        
        layout.addLayout(details_layout)
        
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
        org_details_layout = QVBoxLayout()
        
        self.org_repo_details = QTextEdit()
        self.org_repo_details.setMaximumHeight(120)
        self.org_repo_details.setReadOnly(True)
        self.org_repo_details.setStyleSheet(DarkTheme.get_textedit_style())
        self.org_repo_details.setPlaceholderText("Selecciona una organización y un repositorio...")
        org_details_layout.addWidget(self.org_repo_details)
        
        # Botón para ver ramas de org
        self.org_branches_btn = QPushButton("🌿 Ver Ramas")
        self.org_branches_btn.clicked.connect(self.show_org_repo_branches)
        self.org_branches_btn.setStyleSheet(DarkTheme.get_button_style())
        self.org_branches_btn.setEnabled(False)
        org_details_layout.addWidget(self.org_branches_btn)
        
        layout.addLayout(org_details_layout)
        
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
                username = user_info.get('login', 'Usuario')
                name = user_info.get('name', username)
                
                # Actualizar el estado de conexión
                self.connection_status.setText(f"✅ Conectado a GitHub")
                self.connection_status.setStyleSheet("color: #50fa7b; font-weight: bold;")
                
                # Mostrar información adicional del usuario
                public_repos = user_info.get('public_repos', 0)
                followers = user_info.get('followers', 0)
                self.user_info_label.setText(f"👤 {name} (@{username}) • {public_repos} repos • {followers} seguidores")
                self.user_info_label.show()
                
                # Mostrar biografía del usuario si existe
                bio = user_info.get('bio', '')
                if bio and bio.strip():
                    # Limitar la biografía a 100 caracteres para evitar que sea muy larga
                    bio_text = bio.strip()
                    if len(bio_text) > 100:
                        bio_text = bio_text[:97] + "..."
                    self.user_bio_label.setText(f"💬 \"{bio_text}\"")
                    self.user_bio_label.show()
                else:
                    self.user_bio_label.hide()
                
                # Mostrar avatar del usuario
                self.load_user_avatar(user_info.get('avatar_url'))
                
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
            self.selected_org_repo = None
            self.org_branches_btn.setEnabled(False)
            return
        
        # Almacenar repositorio seleccionado
        self.selected_org_repo = repo_data
        self.org_branches_btn.setEnabled(True)
            
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
            self.selected_user_repo = None
            self.user_branches_btn.setEnabled(False)
            return
        
        # Almacenar repositorio seleccionado
        self.selected_user_repo = repo_data
        self.user_branches_btn.setEnabled(True)
            
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
    
    def load_user_avatar(self, avatar_url):
        """Carga el avatar del usuario de forma asíncrona"""
        if not avatar_url:
            return
            
        # Detener worker anterior si existe
        if self.avatar_worker and self.avatar_worker.isRunning():
            self.avatar_worker.quit()
            self.avatar_worker.wait()
        
        # Crear nuevo worker para descargar avatar
        self.avatar_worker = GitHubAvatarWorker(avatar_url, size=80)
        self.avatar_worker.avatar_ready.connect(self.on_avatar_loaded)
        self.avatar_worker.error_occurred.connect(self.on_avatar_error)
        self.avatar_worker.start()
    
    def on_avatar_loaded(self, pixmap):
        """Callback cuando el avatar se carga exitosamente"""
        if pixmap and not pixmap.isNull():
            # Crear avatar circular perfecto
            avatar_size = 80
            circular_pixmap = self.create_circular_avatar(pixmap, avatar_size)
            
            # Mostrar el avatar
            self.avatar_label.setPixmap(circular_pixmap)
            self.avatar_label.show()
            
            # Actualizar el tooltip con información del usuario
            if hasattr(self, 'github_service') and self.github_service.is_authenticated():
                try:
                    user_info = self.github_service.get_user_info()
                    username = user_info.get('login', 'Usuario')
                    name = user_info.get('name', username)
                    self.avatar_label.setToolTip(f"👤 {name} (@{username})")
                except:
                    self.avatar_label.setToolTip("👤 Usuario de GitHub")
            else:
                self.avatar_label.setToolTip("👤 Usuario de GitHub")
    
    def create_circular_avatar(self, source_pixmap, size):
        """Crea un avatar circular perfecto a partir de una imagen"""
        # Crear pixmap de salida
        output = QPixmap(size, size)
        output.fill(Qt.GlobalColor.transparent)
        
        # Configurar painter con alta calidad
        painter = QPainter(output)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        
        # Escalar la imagen original para que llene completamente el círculo
        # Usamos KeepAspectRatioByExpanding para que no haya espacios vacíos
        scaled_pixmap = source_pixmap.scaled(
            size, size, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Crear máscara circular
        mask = QPixmap(size, size)
        mask.fill(Qt.GlobalColor.transparent)
        
        mask_painter = QPainter(mask)
        mask_painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        mask_painter.setBrush(Qt.GlobalColor.white)
        mask_painter.setPen(Qt.PenStyle.NoPen)
        mask_painter.drawEllipse(0, 0, size, size)
        mask_painter.end()
        
        # Aplicar la máscara circular
        circular_image = QPixmap(size, size)
        circular_image.fill(Qt.GlobalColor.transparent)
        
        circular_painter = QPainter(circular_image)
        circular_painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        circular_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
        # Centrar la imagen escalada
        x_offset = (size - scaled_pixmap.width()) // 2
        y_offset = (size - scaled_pixmap.height()) // 2
        
        # Dibujar la imagen centrada
        circular_painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        
        # Aplicar máscara circular
        circular_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        circular_painter.drawPixmap(0, 0, mask)
        circular_painter.end()
        
        # Dibujar en el pixmap final
        painter.drawPixmap(0, 0, circular_image)
        painter.end()
        
        return output
    
    def on_avatar_error(self, error_msg):
        """Callback cuando hay error cargando el avatar"""
        print(f"Error cargando avatar: {error_msg}")
        
        # Mostrar un placeholder elegante cuando no se puede cargar el avatar
        placeholder = QPixmap(80, 80)
        placeholder.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(placeholder)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        # Crear fondo circular para el placeholder
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.GlobalColor.darkGray)
        painter.drawEllipse(4, 4, 72, 72)
        
        # Dibujar icono de usuario simple
        painter.setPen(Qt.GlobalColor.gray)
        painter.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        painter.drawText(0, 0, 80, 80, Qt.AlignmentFlag.AlignCenter, "👤")
        
        painter.end()
        
        # Mostrar el placeholder
        self.avatar_label.setPixmap(placeholder)
        self.avatar_label.setToolTip("❌ Error al cargar avatar")
        self.avatar_label.show()
    
    def show_user_repo_branches(self):
        """Muestra el diálogo de gestión de ramas para el repositorio del usuario"""
        if not self.selected_user_repo:
            QMessageBox.warning(self, "⚠️ Sin Repositorio", 
                              "Por favor selecciona un repositorio primero")
            return
        
        repo_full_name = self.selected_user_repo.get('full_name')
        repo_name = self.selected_user_repo.get('name')
        
        if repo_full_name and repo_name:
            dialog = BranchManagerDialog(self.github_service, repo_full_name, repo_name, self)
            dialog.exec()
    
    def show_org_repo_branches(self):
        """Muestra el diálogo de gestión de ramas para el repositorio de organización"""
        if not self.selected_org_repo:
            QMessageBox.warning(self, "⚠️ Sin Repositorio", 
                              "Por favor selecciona un repositorio primero")
            return
        
        repo_full_name = self.selected_org_repo.get('full_name')
        repo_name = self.selected_org_repo.get('name')
        
        if repo_full_name and repo_name:
            dialog = BranchManagerDialog(self.github_service, repo_full_name, repo_name, self)
            dialog.exec()
    
    def logout(self):
        """Cierra la sesión de GitHub"""
        self.cleanup_threads()
        self.github_service.logout()
        
        # Resetear UI
        self.connection_status.setText("❌ No conectado a GitHub")
        self.connection_status.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        
        # Ocultar información adicional del usuario
        if hasattr(self, 'user_info_label'):
            self.user_info_label.hide()
            self.user_info_label.clear()
        
        # Ocultar biografía del usuario
        if hasattr(self, 'user_bio_label'):
            self.user_bio_label.hide()
            self.user_bio_label.clear()
        
        # Ocultar avatar
        self.avatar_label.hide()
        self.avatar_label.clear()
        
        self.repos_frame.hide()
        self.login_frame.show()
        
        self.token_input.clear()
        
        # Resetear repositorios seleccionados
        self.selected_user_repo = None
        self.selected_org_repo = None
        
        # Limpiar todos los widgets
        if hasattr(self, 'user_repos_list'):
            self.user_repos_list.clear()
        if hasattr(self, 'user_repo_details'):
            self.user_repo_details.clear()
        if hasattr(self, 'user_branches_btn'):
            self.user_branches_btn.setEnabled(False)
        if hasattr(self, 'org_combo'):
            self.org_combo.clear()
        if hasattr(self, 'org_repos_list'):
            self.org_repos_list.clear()
        if hasattr(self, 'org_repo_details'):
            self.org_repo_details.clear()
        if hasattr(self, 'org_branches_btn'):
            self.org_branches_btn.setEnabled(False)
        
        QMessageBox.information(self, "🚪 Sesión Cerrada", 
                              "Has cerrado sesión de GitHub exitosamente.")
    
    def cleanup_threads(self):
        """Limpia y cierra todos los threads activos"""
        threads_to_cleanup = []
        
        # Agregar todos los workers a la lista
        if hasattr(self, 'worker') and self.worker:
            threads_to_cleanup.append(self.worker)
        
        if hasattr(self, 'avatar_worker') and self.avatar_worker:
            threads_to_cleanup.append(self.avatar_worker)
        
        if hasattr(self, 'org_worker') and self.org_worker:
            threads_to_cleanup.append(self.org_worker)
        
        if hasattr(self, 'org_repos_worker') and self.org_repos_worker:
            threads_to_cleanup.append(self.org_repos_worker)
        
        # Cerrar todos los threads
        for thread in threads_to_cleanup:
            if thread and thread.isRunning():
                thread.quit()
                if not thread.wait(3000):  # Esperar máximo 3 segundos
                    thread.terminate()
                    thread.wait()
    
    def closeEvent(self, event):
        """Maneja el evento de cierre del widget"""
        self.cleanup_threads()
        super().closeEvent(event)
