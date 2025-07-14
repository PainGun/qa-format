#!/usr/bin/env python3
"""
Generador de QA - Aplicación Principal
======================================

Aplicación de escritorio moderna para generar tareas de QA de manera eficiente.
Construida con PyQt6 siguiendo principios de Clean Architecture.

Autor: Developer Full Stack
Versión: 2.0.0
"""

import sys
from typing import Optional, Dict, Any
from dataclasses import dataclass

# ============================================================================
# IMPORTS DE PYQT6
# ============================================================================

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, 
    QScrollArea, QFrame, QMessageBox, QGroupBox, QGridLayout, 
    QSizePolicy, QSplitter, QTabWidget, QComboBox, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon, QClipboard, QPalette, QColor
import json

# ============================================================================
# IMPORTS LOCALES
# ============================================================================

from controllers import TareaQAController
from generador_qa.src.infrastructure.external.slack_notification_service import SlackNotificationService
from generador_qa.src.application.use_cases.enviar_notificacion_slack import EnviarNotificacionSlackUseCase
from generador_qa.src.shared.utils import db
import datetime
from generador_qa.src.domain.entities.tarea import TareaQA as DomainTareaQA, AmbientePR as DomainAmbientePR, ComentarioQA as DomainComentarioQA
from generador_qa.src.domain.value_objects.tipos_qa import TipoQA as DomainTipoQA

# ============================================================================
# DOMAIN LAYER - ENTITIES AND VALUE OBJECTS
# ============================================================================

@dataclass
class ThemeColors:
    """Value Object para colores del tema"""
    background: str = '#282a36'
    current_line: str = '#44475a'
    selection: str = '#44475a'
    foreground: str = '#f8f8f2'
    comment: str = '#6272a4'
    cyan: str = '#8be9fd'
    green: str = '#50fa7b'
    orange: str = '#ffb86c'
    pink: str = '#ff79c6'
    purple: str = '#bd93f9'
    red: str = '#ff5555'
    yellow: str = '#f1fa8c'

@dataclass
class UIConfig:
    """Value Object para configuración de la UI"""
    window_title: str = "📋 Generador Paso a QA - Clean Architecture"
    window_width: int = 1200
    window_height: int = 900
    min_width: int = 1000
    min_height: int = 700
    scroll_spacing: int = 15
    scroll_margins: int = 20

# ============================================================================
# INFRASTRUCTURE LAYER - PRESENTATION
# ============================================================================

class ThemeManager:
    """Gestor de temas de la aplicación"""
    
    def __init__(self, colors: ThemeColors):
        self.colors = colors
    
    def get_main_stylesheet(self) -> str:
        """Retorna el stylesheet principal para la aplicación"""
        return f"""
        QMainWindow {{
            background-color: {self.colors.background};
            color: {self.colors.foreground};
        }}
        QWidget {{
            background-color: {self.colors.background};
            color: {self.colors.foreground};
            font-family: 'Arial', sans-serif;
        }}
        {self._get_groupbox_style()}
        {self._get_label_style()}
        {self._get_lineedit_style()}
        {self._get_button_style()}
        {self._get_textedit_style()}
        {self._get_listwidget_style()}
        {self._get_scrollbar_style()}
        {self._get_scrollarea_style()}
        {self._get_frame_style()}
        """
    
    def _get_groupbox_style(self) -> str:
        """Estilos para QGroupBox (secciones)"""
        return f"""
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {self.colors.current_line};
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: {self.colors.current_line};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 8px 15px 8px 15px;
            color: {self.colors.foreground};
            font-size: 14px;
            font-weight: bold;
            background-color: {self.colors.purple};
            border-radius: 6px;
            border: 1px solid #9580e0;
        }}
        """
    
    def _get_label_style(self) -> str:
        """Estilos para QLabel"""
        return f"""
        QLabel {{
            color: {self.colors.foreground};
            font-weight: bold;
        }}
        """
    
    def _get_lineedit_style(self) -> str:
        """Estilos para QLineEdit (campos de texto)"""
        return f"""
        QLineEdit {{
            background-color: {self.colors.comment};
            border: 2px solid #565b5e;
            border-radius: 6px;
            padding: 8px;
            color: {self.colors.foreground};
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: {self.colors.purple};
        }}
        QLineEdit::placeholder {{
            color: {self.colors.cyan};
        }}
        """
    
    def _get_button_style(self) -> str:
        """Estilos para QPushButton"""
        return f"""
        QPushButton {{
            background-color: {self.colors.comment};
            border: 2px solid {self.colors.purple};
            border-radius: 8px;
            padding: 12px 18px;
            color: {self.colors.foreground};
            font-weight: bold;
            font-size: 13px;
            min-height: 20px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: {self.colors.green};
            border-color: #45d668;
            color: {self.colors.background};
        }}
        QPushButton:pressed {{
            background-color: #45d668;
            border-color: #3bc95a;
        }}
        QPushButton#deleteBtn {{
            background-color: {self.colors.red};
            max-width: 40px;
            padding: 8px;
        }}
        QPushButton#deleteBtn:hover {{
            background-color: #ff6e6e;
        }}
        QPushButton#clearBtn {{
            background-color: {self.colors.red};
        }}
        QPushButton#clearBtn:hover {{
            background-color: #ff6e6e;
        }}
        """
    
    def _get_textedit_style(self) -> str:
        """Estilos para QTextEdit (áreas de texto)"""
        return f"""
        QTextEdit {{
            background-color: {self.colors.current_line};
            border: 2px solid #565b5e;
            border-radius: 6px;
            padding: 8px;
            color: {self.colors.foreground};
            font-size: 12px;
        }}
        QTextEdit:focus {{
            border-color: {self.colors.purple};
        }}
        """
    
    def _get_listwidget_style(self) -> str:
        """Estilos para QListWidget (listas)"""
        return f"""
        QListWidget {{
            background-color: {self.colors.current_line};
            border: 2px solid #565b5e;
            border-radius: 6px;
            color: {self.colors.foreground};
            font-size: 11px;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 5px;
            border-bottom: 1px solid {self.colors.comment};
        }}
        QListWidget::item:selected {{
            background-color: {self.colors.purple};
            color: {self.colors.background};
        }}
        """
    
    def _get_scrollbar_style(self) -> str:
        """Estilos para las barras de desplazamiento"""
        return f"""
        QScrollBar:vertical {{
            background-color: {self.colors.current_line};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {self.colors.comment};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors.green};
        }}
        """
    
    def _get_scrollarea_style(self) -> str:
        """Estilos para QScrollArea"""
        return f"""
        QScrollArea {{
            border: none;
            background-color: {self.colors.background};
        }}
        """
    
    def _get_frame_style(self) -> str:
        """Estilos para QFrame"""
        return f"""
        QFrame {{
            background-color: transparent;
        }}
        """
    
    def get_title_label_style(self) -> str:
        """Estilo especial para el título principal"""
        return f"""
            color: {self.colors.foreground}; 
            background-color: {self.colors.comment};
            padding: 15px;
            border-radius: 8px;
            border: 2px solid {self.colors.purple};
            margin: 10px;
        """

# ============================================================================
# APPLICATION LAYER - USE CASES
# ============================================================================

class UIComponentFactory:
    """Factory para crear componentes de UI reutilizables"""
    
    @staticmethod
    def create_title_label(text: str, theme_manager: ThemeManager) -> QLabel:
        """Crea un título principal con estilo"""
        title_label = QLabel(text)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(theme_manager.get_title_label_style())
        return title_label
    
    @staticmethod
    def create_input_field(placeholder: str = "") -> QLineEdit:
        """Crea un campo de entrada con placeholder"""
        field = QLineEdit()
        if placeholder:
            field.setPlaceholderText(placeholder)
        return field
    
    @staticmethod
    def create_button(text: str, object_name: str = "") -> QPushButton:
        """Crea un botón con texto y opcional object_name"""
        button = QPushButton(text)
        if object_name:
            button.setObjectName(object_name)
        return button
    
    @staticmethod
    def create_list_with_delete(max_height: int = 100) -> QListWidget:
        """Crea una lista con altura máxima configurable"""
        list_widget = QListWidget()
        list_widget.setMaximumHeight(max_height)
        return list_widget

class SlackPanel(QWidget):
    canales_actualizados = pyqtSignal()
    def __init__(self, parent=None, get_tarea_fn=None):
        super().__init__(parent)
        self.get_tarea_fn = get_tarea_fn  # función para obtener la tarea actual
        self.slack_service = None
        self.use_case = None
        self.canales = []
        self.usuarios = []
        self._setup_ui()
        db.init_db()
        self._load_config()
        self._load_historial()
        # Conexión automática si hay config
        if self.token_input.text().strip() and self.usuario_input.text().strip():
            self._probar_conexion()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        # --- Tab Configuración ---
        tab_config = QWidget()
        config_layout = QVBoxLayout(tab_config)
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText('Token de Bot (xoxb-...)')
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText('Usuario Slack (sin @)')
        self.workspace_input = QLineEdit()
        self.workspace_input.setPlaceholderText('Workspace (ej: tu-workspace.slack.com)')
        self.btn_probar = QPushButton('🧪 Probar Conexión')
        self.lbl_status = QLabel('Estado: ❌ No conectado')
        config_layout.addWidget(QLabel('Token Slack:'))
        config_layout.addWidget(self.token_input)
        config_layout.addWidget(QLabel('Usuario Slack:'))
        config_layout.addWidget(self.usuario_input)
        config_layout.addWidget(QLabel('Workspace:'))
        config_layout.addWidget(self.workspace_input)
        config_layout.addWidget(self.btn_probar)
        config_layout.addWidget(self.lbl_status)
        self.btn_probar.clicked.connect(self._probar_conexion)
        self.tabs.addTab(tab_config, '🔗 Configuración')
        # --- Tab Enviar ---
        tab_enviar = QWidget()
        enviar_layout = QVBoxLayout(tab_enviar)
        self.combo_destino = QComboBox()
        self.combo_destino.setEditable(True)
        self.combo_destino.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.combo_destino.setMaxVisibleItems(15)  # scroll
        self.completer = QCompleter()
        self.combo_destino.setCompleter(self.completer)
        self.btn_cargar_canales = QPushButton('🔄 Cargar Canales/Usuarios')
        self.btn_enviar = QPushButton('📤 Enviar a Slack')
        self.btn_enviar.setEnabled(False)
        enviar_layout.addWidget(QLabel('Destino Slack:'))
        enviar_layout.addWidget(self.combo_destino)
        enviar_layout.addWidget(self.btn_cargar_canales)
        enviar_layout.addWidget(self.btn_enviar)
        self.lbl_envio = QLabel('')
        enviar_layout.addWidget(self.lbl_envio)
        self.btn_cargar_canales.clicked.connect(self._cargar_canales)
        self.btn_enviar.clicked.connect(self._enviar_a_slack)
        self.btn_mensaje_prueba = QPushButton('🧪 Mensaje de Prueba')
        enviar_layout.addWidget(self.btn_mensaje_prueba)
        self.btn_mensaje_prueba.clicked.connect(self._enviar_mensaje_prueba)
        self.tabs.addTab(tab_enviar, '�� Enviar')
        # --- Tab Historial ---
        tab_hist = QWidget()
        hist_layout = QVBoxLayout(tab_hist)
        self.historial_list = QListWidget()
        self.detalle_text = QTextEdit()
        self.detalle_text.setReadOnly(True)
        hist_layout.addWidget(self.historial_list)
        hist_layout.addWidget(QLabel('Detalle:'))
        hist_layout.addWidget(self.detalle_text)
        self.historial_list.currentRowChanged.connect(self._mostrar_detalle_historial)
        self.tabs.addTab(tab_hist, '🕓 Historial')

    def _persistir_canales_usuarios(self):
        # Guardar en config como JSON
        db.set_config('slack_canales', json.dumps(self.canales))
        db.set_config('slack_usuarios', json.dumps(self.usuarios))

    def _cargar_canales_usuarios_guardados(self):
        canales_json = db.get_config('slack_canales')
        usuarios_json = db.get_config('slack_usuarios')
        self.canales = json.loads(canales_json) if canales_json else []
        self.usuarios = json.loads(usuarios_json) if usuarios_json else []
        self._actualizar_selector_destino()

    def _actualizar_selector_destino(self):
        self.combo_destino.clear()
        items = []
        for c in self.canales:
            self.combo_destino.addItem(f"#{c['name']}", c['id'])
            items.append(f"#{c['name']}")
        for u in self.usuarios:
            self.combo_destino.addItem(f"@{u['name']}", u['id'])
            items.append(f"@{u['name']}")
        self.completer.setModel(self.combo_destino.model())
        self.lbl_envio.setText('✅ Canales y usuarios listos')
        self.canales_actualizados.emit()

    def _cargar_canales(self):
        if not self.slack_service:
            self.lbl_envio.setText('❌ Slack no está configurado')
            return
        try:
            self.canales = self.slack_service.obtener_canales_disponibles()
            self.usuarios = self.slack_service.obtener_usuarios_disponibles()
            self._persistir_canales_usuarios()
            self._actualizar_selector_destino()
        except Exception as e:
            self.lbl_envio.setText(f'❌ Error: {e}')

    def _load_config(self):
        token = db.get_config('slack_token')
        usuario = db.get_config('slack_user')
        workspace = db.get_config('slack_workspace') or 'slack.com'
        if token:
            self.token_input.setText(token)
        if usuario:
            self.usuario_input.setText(usuario)
        if workspace:
            self.workspace_input.setText(workspace)
        self._cargar_canales_usuarios_guardados()

    def _save_config(self):
        db.set_config('slack_token', self.token_input.text().strip())
        db.set_config('slack_user', self.usuario_input.text().strip())
        db.set_config('slack_workspace', self.workspace_input.text().strip())

    def _probar_conexion(self):
        token = self.token_input.text().strip()
        usuario = self.usuario_input.text().strip()
        workspace = self.workspace_input.text().strip() or 'slack.com'
        if not token or not usuario:
            self.lbl_status.setText('Estado: ❌ Faltan datos')
            return
        try:
            self.slack_service = SlackNotificationService(token, workspace)
            if self.slack_service.verificar_conexion():
                self.lbl_status.setText('Estado: ✅ Conectado')
                self._save_config()
                self.use_case = EnviarNotificacionSlackUseCase(self.slack_service)
                self.btn_enviar.setEnabled(True)
            else:
                self.lbl_status.setText('Estado: ❌ Error de conexión')
                self.btn_enviar.setEnabled(False)
        except Exception as e:
            self.lbl_status.setText(f'Estado: ❌ {e}')
            self.btn_enviar.setEnabled(False)

    def _enviar_a_slack(self):
        if not self.use_case:
            self.lbl_envio.setText('❌ Slack no está configurado')
            return
        idx = self.combo_destino.currentIndex()
        if idx < 0:
            self.lbl_envio.setText('❌ Selecciona un canal o usuario')
            return
        canal_id = self.combo_destino.currentData()
        tarea = self.get_tarea_fn() if self.get_tarea_fn else None
        if not tarea:
            self.lbl_envio.setText('❌ No hay tarea para enviar')
            return
        try:
            resultado = self.use_case.enviar_reporte_qa(tarea, canal_id)
            estado = 'Éxito' if resultado else 'Error'
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            usuario = self.usuario_input.text().strip() or 'desconocido'
            mensaje = tarea.generar_texto()
            destino = self.combo_destino.currentText()
            db.save_historial_envio(fecha, destino, mensaje, estado, usuario)
            self._load_historial()
            self.lbl_envio.setText(f'✅ Enviado a {destino}')
        except Exception as e:
            self.lbl_envio.setText(f'❌ Error: {e}')

    def _enviar_mensaje_prueba(self):
        if not self.use_case:
            self.lbl_envio.setText('❌ Slack no está configurado')
            return
        idx = self.combo_destino.currentIndex()
        if idx < 0:
            self.lbl_envio.setText('❌ Selecciona un canal o usuario')
            return
        canal_id = self.combo_destino.currentData()
        try:
            resultado = self.use_case.execute('🧪 Mensaje de prueba desde Generador QA', canal_id)
            estado = 'Éxito' if resultado else 'Error'
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            usuario = self.usuario_input.text().strip() or 'desconocido'
            mensaje = '🧪 Mensaje de prueba desde Generador QA'
            destino = self.combo_destino.currentText()
            db.save_historial_envio(fecha, destino, mensaje, estado, usuario)
            self._load_historial()
            if resultado:
                self.lbl_envio.setText(f'✅ Mensaje de prueba enviado a {destino}')
            else:
                self.lbl_envio.setText(f'❌ Error al enviar mensaje de prueba a {destino}')
        except Exception as e:
            self.lbl_envio.setText(f'❌ Error: {e}')

    def _load_historial(self):
        self.historial_list.clear()
        self.historial = db.get_historial_envios()
        for envio in self.historial:
            resumen = envio['mensaje'][:60].replace('\n', ' ') + ('...' if len(envio['mensaje']) > 60 else '')
            item = f"[{envio['fecha']}] → {envio['destino']} | {envio['estado']} | Remitente: @{envio['usuario']} | {resumen}"
            self.historial_list.addItem(item)
        self.detalle_text.clear()

    def _mostrar_detalle_historial(self, idx):
        if idx < 0 or idx >= len(self.historial):
            self.detalle_text.clear()
            return
        envio = self.historial[idx]
        detalle = f"Fecha: {envio['fecha']}\nDestino: {envio['destino']}\nEstado: {envio['estado']}\nRemitente: @{envio['usuario']}\n\nMensaje:\n{envio['mensaje']}"
        self.detalle_text.setPlainText(detalle)

    def enviar_reporte_desde_main(self):
        # Usar la configuración y canal seleccionados actualmente
        if not self.use_case:
            return False, 'Slack no está configurado. Ve a la pestaña Slack.'
        idx = self.combo_destino.currentIndex()
        if idx < 0:
            return False, 'Selecciona un canal o usuario en la pestaña Slack.'
        canal_id = self.combo_destino.currentData()
        tarea = self.get_tarea_fn() if self.get_tarea_fn else None
        if not tarea:
            return False, 'No hay tarea para enviar.'
        try:
            resultado = self.use_case.enviar_reporte_qa(tarea, canal_id)
            estado = 'Éxito' if resultado else 'Error'
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            usuario = self.usuario_input.text().strip() or 'desconocido'
            mensaje = tarea.generar_texto()
            destino = self.combo_destino.currentText()
            db.save_historial_envio(fecha, destino, mensaje, estado, usuario)
            self._load_historial()
            if resultado:
                self.lbl_envio.setText(f'✅ Enviado a {destino}')
                return True, f'Enviado a {destino}'
            else:
                self.lbl_envio.setText(f'❌ Error al enviar a {destino}')
                return False, f'Error al enviar a {destino}'
        except Exception as e:
            self.lbl_envio.setText(f'❌ Error: {e}')
            return False, f'Error: {e}'

# ============================================================================
# PRESENTATION LAYER - VIEWS
# ============================================================================

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, controller: TareaQAController, config: UIConfig):
        super().__init__()
        self.controller = controller
        self.config = config
        self.theme_manager = ThemeManager(ThemeColors())
        self.factory = UIComponentFactory()
        
        self._setup_window()
        self._setup_ui()
        self._setup_theme()
        self._setup_connections()
    
    def _setup_window(self):
        """Configura la ventana principal"""
        self.setWindowTitle(self.config.window_title)
        self.setGeometry(100, 100, self.config.window_width, self.config.window_height)
        self.setMinimumSize(self.config.min_width, self.config.min_height)
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal con scroll
        main_layout = QVBoxLayout(central_widget)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        # Crear área de scroll para la app principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(self.config.scroll_spacing)
        scroll_layout.setContentsMargins(
            self.config.scroll_margins, 
            self.config.scroll_margins, 
            self.config.scroll_margins, 
            self.config.scroll_margins
        )
        title_label = self.factory.create_title_label(
            "📋 FORMULARIO DE QA", 
            self.theme_manager
        )
        scroll_layout.addWidget(title_label)
        self._create_sections(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        self.tabs.addTab(scroll_area, '📝 QA')
        # --- Integrar SlackPanel ---
        self.slack_panel = SlackPanel(get_tarea_fn=self._get_tarea_actual)
        self.tabs.addTab(self.slack_panel, '🔗 Slack')
        self.slack_panel.canales_actualizados.connect(self.sincronizar_destinos_slack)
        self.sincronizar_destinos_slack()  # inicial

    def _create_sections(self, layout: QVBoxLayout):
        """Crea todas las secciones de la aplicación"""
        # Información básica
        self._create_basic_info_section(layout)
        
        # Ambientes y PRs
        self._create_environments_section(layout)
        
        # Comentarios
        self._create_comments_section(layout)
        
        # Responsables QA
        self._create_qa_responsibles_section(layout)
        
        # Acciones
        self._create_actions_section(layout)
        
        # Resultado
        self._create_result_section(layout)
    
    def _create_basic_info_section(self, layout: QVBoxLayout):
        """Crea la sección de información básica"""
        group = QGroupBox("📌 INFORMACIÓN BÁSICA")
        group_layout = QVBoxLayout()
        
        # Título de la tarea
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("📝 Título de la Tarea:"))
        self.entry_titulo = self.factory.create_input_field("Ingrese el título de la tarea")
        title_layout.addWidget(self.entry_titulo)
        group_layout.addLayout(title_layout)
        
        # Jira
        jira_layout = QHBoxLayout()
        jira_layout.addWidget(QLabel("🔗 Link Jira:"))
        self.entry_jira = self.factory.create_input_field("https://jira.empresa.com/...")
        jira_layout.addWidget(self.entry_jira)
        group_layout.addLayout(jira_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _create_environments_section(self, layout: QVBoxLayout):
        """Crea la sección de ambientes y PRs"""
        group = QGroupBox("🌐 AMBIENTES + PRs")
        group_layout = QVBoxLayout()
        
        # Inputs
        inputs_layout = QHBoxLayout()
        
        # Ambiente
        ambiente_layout = QVBoxLayout()
        ambiente_layout.addWidget(QLabel("🏢 Ambiente:"))
        self.entry_ambiente = self.factory.create_input_field("dev, staging, prod...")
        ambiente_layout.addWidget(self.entry_ambiente)
        inputs_layout.addLayout(ambiente_layout)
        
        # PR
        pr_layout = QVBoxLayout()
        pr_layout.addWidget(QLabel("🔄 PR:"))
        self.entry_pr = self.factory.create_input_field("Número o link del PR")
        pr_layout.addWidget(self.entry_pr)
        inputs_layout.addLayout(pr_layout)
        
        group_layout.addLayout(inputs_layout)
        
        # Botón agregar
        self.btn_agregar_amb = self.factory.create_button("➕ Agregar Ambiente + PR")
        group_layout.addWidget(self.btn_agregar_amb)
        
        # Lista y botón eliminar
        list_layout = QHBoxLayout()
        self.lista_ambientes_prs = self.factory.create_list_with_delete(100)
        list_layout.addWidget(self.lista_ambientes_prs)
        
        self.btn_eliminar_amb = self.factory.create_button("🗑️", "deleteBtn")
        list_layout.addWidget(self.btn_eliminar_amb)
        
        group_layout.addLayout(list_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _create_comments_section(self, layout: QVBoxLayout):
        """Crea la sección de comentarios"""
        group = QGroupBox("💬 COMENTARIOS DE PRUEBA")
        group_layout = QVBoxLayout()
        
        # Primera fila
        fila1_layout = QHBoxLayout()
        
        tipo_layout = QVBoxLayout()
        tipo_layout.addWidget(QLabel("🔍 Tipo QA:"))
        self.entry_tipo_qa = self.factory.create_input_field("Usabilidad / Código")
        tipo_layout.addWidget(self.entry_tipo_qa)
        fila1_layout.addLayout(tipo_layout)
        
        link_layout = QVBoxLayout()
        link_layout.addWidget(QLabel("🔗 Link para prueba:"))
        self.entry_link_qa = self.factory.create_input_field("URL de la aplicación")
        link_layout.addWidget(self.entry_link_qa)
        fila1_layout.addLayout(link_layout)
        
        group_layout.addLayout(fila1_layout)
        
        # Segunda fila
        ambiente_layout = QVBoxLayout()
        ambiente_layout.addWidget(QLabel("🌐 Ambiente de prueba:"))
        self.entry_ambiente_qa = self.factory.create_input_field("Ambiente donde probar")
        ambiente_layout.addWidget(self.entry_ambiente_qa)
        group_layout.addLayout(ambiente_layout)
        
        # Instrucciones
        instr_layout = QVBoxLayout()
        instr_layout.addWidget(QLabel("📝 Instrucciones:"))
        self.txt_instruccion = QTextEdit()
        self.txt_instruccion.setPlaceholderText("Pasos detallados para realizar la prueba...")
        self.txt_instruccion.setMaximumHeight(80)
        instr_layout.addWidget(self.txt_instruccion)
        group_layout.addLayout(instr_layout)
        
        # Botón agregar
        self.btn_agregar_com = self.factory.create_button("➕ Agregar Comentario")
        group_layout.addWidget(self.btn_agregar_com)
        
        # Lista y botón eliminar
        list_layout = QHBoxLayout()
        self.lista_comentarios = self.factory.create_list_with_delete(100)
        list_layout.addWidget(self.lista_comentarios)
        
        self.btn_eliminar_com = self.factory.create_button("🗑️", "deleteBtn")
        list_layout.addWidget(self.btn_eliminar_com)
        
        group_layout.addLayout(list_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _create_qa_responsibles_section(self, layout: QVBoxLayout):
        """Crea la sección de responsables QA"""
        group = QGroupBox("👥 RESPONSABLES QA")
        group_layout = QVBoxLayout()
        
        # QA Usabilidad
        usu_layout = QVBoxLayout()
        usu_layout.addWidget(QLabel("🎨 QA Usabilidad:"))
        
        usu_input_layout = QHBoxLayout()
        self.entry_qa_usu = self.factory.create_input_field("Nombre del responsable de QA Usabilidad")
        usu_input_layout.addWidget(self.entry_qa_usu)
        
        self.btn_agregar_usu = self.factory.create_button("➕")
        usu_input_layout.addWidget(self.btn_agregar_usu)
        
        usu_layout.addLayout(usu_input_layout)
        
        usu_list_layout = QHBoxLayout()
        self.lista_qa_usu = self.factory.create_list_with_delete(60)
        usu_list_layout.addWidget(self.lista_qa_usu)
        
        self.btn_eliminar_usu = self.factory.create_button("🗑️", "deleteBtn")
        usu_list_layout.addWidget(self.btn_eliminar_usu)
        
        usu_layout.addLayout(usu_list_layout)
        group_layout.addLayout(usu_layout)
        
        # QA Código
        cod_layout = QVBoxLayout()
        cod_layout.addWidget(QLabel("💻 QA Código:"))
        
        cod_input_layout = QHBoxLayout()
        self.entry_qa_cod = self.factory.create_input_field("Nombre del responsable de QA Código")
        cod_input_layout.addWidget(self.entry_qa_cod)
        
        self.btn_agregar_cod = self.factory.create_button("➕")
        cod_input_layout.addWidget(self.btn_agregar_cod)
        
        cod_layout.addLayout(cod_input_layout)
        
        cod_list_layout = QHBoxLayout()
        self.lista_qa_cod = self.factory.create_list_with_delete(60)
        cod_list_layout.addWidget(self.lista_qa_cod)
        
        self.btn_eliminar_cod = self.factory.create_button("🗑️", "deleteBtn")
        cod_list_layout.addWidget(self.btn_eliminar_cod)
        
        cod_layout.addLayout(cod_list_layout)
        group_layout.addLayout(cod_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _create_actions_section(self, layout: QVBoxLayout):
        group = QGroupBox("⚡ ACCIONES")
        group_layout = QHBoxLayout()
        # Selector de canal/usuario Slack
        self.combo_destino_main = QComboBox()
        self.combo_destino_main.setEditable(True)
        self.combo_destino_main.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.combo_destino_main.setMaxVisibleItems(15)
        self.completer_main = QCompleter()
        self.combo_destino_main.setCompleter(self.completer_main)
        group_layout.addWidget(QLabel('Destino Slack:'))
        group_layout.addWidget(self.combo_destino_main)
        self.btn_enviar_slack = self.factory.create_button("📤 Enviar a Slack")
        self.btn_enviar_slack.setEnabled(False)
        group_layout.addWidget(self.btn_enviar_slack)
        self.btn_generar = self.factory.create_button("🚀 Generar Texto")
        group_layout.addWidget(self.btn_generar)
        self.btn_copiar = self.factory.create_button("📋 Copiar al Portapapeles")
        group_layout.addWidget(self.btn_copiar)
        self.btn_limpiar = self.factory.create_button("🧹 Limpiar Todo", "clearBtn")
        group_layout.addWidget(self.btn_limpiar)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _create_result_section(self, layout: QVBoxLayout):
        """Crea la sección de resultado"""
        group = QGroupBox("📄 RESULTADO GENERADO")
        group_layout = QVBoxLayout()
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setMinimumHeight(300)
        self.resultado_text.setReadOnly(True)
        group_layout.addWidget(self.resultado_text)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _setup_theme(self):
        """Aplica el tema a la aplicación"""
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
    
    def _setup_connections(self):
        """Configura las conexiones de señales"""
        # Conectar botones de ambientes
        self.btn_agregar_amb.clicked.connect(self._on_agregar_ambiente_pr)
        self.btn_eliminar_amb.clicked.connect(lambda: self._on_eliminar_seleccionado(self.lista_ambientes_prs, "ambiente"))
        
        # Conectar botones de comentarios
        self.btn_agregar_com.clicked.connect(self._on_agregar_comentario)
        self.btn_eliminar_com.clicked.connect(lambda: self._on_eliminar_seleccionado(self.lista_comentarios, "comentario"))
        
        # Conectar botones de QA
        self.btn_agregar_usu.clicked.connect(self._on_agregar_qa_usu)
        self.btn_eliminar_usu.clicked.connect(lambda: self._on_eliminar_seleccionado(self.lista_qa_usu, "qa_usu"))
        self.btn_agregar_cod.clicked.connect(self._on_agregar_qa_cod)
        self.btn_eliminar_cod.clicked.connect(lambda: self._on_eliminar_seleccionado(self.lista_qa_cod, "qa_cod"))
        
        # Conectar botones de acciones
        self.btn_generar.clicked.connect(self._on_generar_texto)
        self.btn_copiar.clicked.connect(self._on_copiar_texto)
        self.btn_limpiar.clicked.connect(self._on_limpiar_formulario)
        self.btn_enviar_slack.clicked.connect(self._on_enviar_a_slack_desde_acciones)
        self.combo_destino_main.currentIndexChanged.connect(self._habilitar_envio_si_listo)
        
        # Conectar campos de texto
        self.entry_titulo.textChanged.connect(self._on_titulo_changed)
        self.entry_jira.textChanged.connect(self._on_jira_changed)
    
    def _on_agregar_ambiente_pr(self):
        """Maneja el evento de agregar ambiente y PR"""
        ambiente = self.entry_ambiente.text().strip()
        pr = self.entry_pr.text().strip()
        
        if self.controller.agregar_ambiente_pr(ambiente, pr):
            item_texto = self.controller.formatear_ambiente_pr_para_ui(ambiente, pr)
            self.lista_ambientes_prs.addItem(item_texto)
            self.entry_ambiente.clear()
            self.entry_pr.clear()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete ambos campos.")
    
    def _on_agregar_comentario(self):
        """Maneja el evento de agregar comentario"""
        tipo = self.entry_tipo_qa.text().strip()
        link = self.entry_link_qa.text().strip()
        ambiente = self.entry_ambiente_qa.text().strip()
        instruccion = self.txt_instruccion.toPlainText().strip()
        
        if self.controller.agregar_comentario(tipo, link, ambiente, instruccion):
            comentario_texto = self.controller.formatear_comentario_para_ui(tipo, link, ambiente, instruccion)
            self.lista_comentarios.addItem(comentario_texto)
            self.entry_tipo_qa.clear()
            self.entry_link_qa.clear()
            self.entry_ambiente_qa.clear()
            self.txt_instruccion.clear()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos.")
    
    def _on_agregar_qa_usu(self):
        """Maneja el evento de agregar QA Usabilidad"""
        qa = self.entry_qa_usu.text().strip()
        if self.controller.agregar_qa_usabilidad(qa):
            self.lista_qa_usu.addItem(qa)
            self.entry_qa_usu.clear()
        else:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingrese un nombre.")
    
    def _on_agregar_qa_cod(self):
        """Maneja el evento de agregar QA Código"""
        qa = self.entry_qa_cod.text().strip()
        if self.controller.agregar_qa_codigo(qa):
            self.lista_qa_cod.addItem(qa)
            self.entry_qa_cod.clear()
        else:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingrese un nombre.")
    
    def _on_eliminar_seleccionado(self, listbox: QListWidget, tipo: str):
        """Maneja el evento de eliminar elemento seleccionado"""
        current_row = listbox.currentRow()
        if current_row >= 0:
            success = False
            if tipo == "ambiente":
                success = self.controller.eliminar_ambiente_pr(current_row)
            elif tipo == "comentario":
                success = self.controller.eliminar_comentario(current_row)
            elif tipo == "qa_usu":
                success = self.controller.eliminar_qa_usabilidad(current_row)
            elif tipo == "qa_cod":
                success = self.controller.eliminar_qa_codigo(current_row)
            
            if success:
                listbox.takeItem(current_row)
    
    def _on_generar_texto(self):
        """Maneja el evento de generar texto"""
        # Actualizar el controlador con los datos actuales de la UI
        self.controller.actualizar_titulo(self.entry_titulo.text())
        self.controller.actualizar_jira(self.entry_jira.text())
        
        # Generar el texto usando el controlador
        resultado = self.controller.generar_texto()
        self.resultado_text.setPlainText(resultado)
    
    def _on_copiar_texto(self):
        """Maneja el evento de copiar texto"""
        texto = self.resultado_text.toPlainText()
        if self.controller.copiar_al_portapapeles(texto):
            QMessageBox.information(self, "✅ Copiado", "Texto copiado al portapapeles exitosamente.")
        else:
            QMessageBox.warning(self, "❌ Error", "No se pudo copiar al portapapeles.")
    
    def _on_limpiar_formulario(self):
        """Maneja el evento de limpiar formulario"""
        # Limpiar datos del controlador
        self.controller.limpiar_datos()
        
        # Limpiar UI
        self.entry_titulo.clear()
        self.entry_jira.clear()
        self.entry_ambiente.clear()
        self.entry_pr.clear()
        self.entry_tipo_qa.clear()
        self.entry_link_qa.clear()
        self.entry_ambiente_qa.clear()
        self.txt_instruccion.clear()
        self.entry_qa_usu.clear()
        self.entry_qa_cod.clear()
        self.lista_ambientes_prs.clear()
        self.lista_comentarios.clear()
        self.lista_qa_usu.clear()
        self.lista_qa_cod.clear()
        self.resultado_text.clear()
    
    def _on_titulo_changed(self, text: str):
        """Maneja cambios en el título"""
        self.controller.actualizar_titulo(text)
    
    def _on_jira_changed(self, text: str):
        """Maneja cambios en el link de Jira"""
        self.controller.actualizar_jira(text)

    def _habilitar_envio_si_listo(self):
        # Habilita el botón solo si hay conexión y destino
        if self.slack_panel.use_case and self.combo_destino_main.currentIndex() >= 0:
            self.btn_enviar_slack.setEnabled(True)
        else:
            self.btn_enviar_slack.setEnabled(False)

    def sincronizar_destinos_slack(self):
        # Llama esto después de cargar canales/usuarios en SlackPanel
        self.combo_destino_main.clear()
        items = []
        for c in self.slack_panel.canales:
            self.combo_destino_main.addItem(f"#{c['name']}", c['id'])
            items.append(f"#{c['name']}")
        for u in self.slack_panel.usuarios:
            self.combo_destino_main.addItem(f"@{u['name']}", u['id'])
            items.append(f"@{u['name']}")
        self.completer_main.setModel(self.combo_destino_main.model())
        self._habilitar_envio_si_listo()

    def _on_enviar_a_slack_desde_acciones(self):
        # Usar el destino seleccionado en la pestaña principal
        if not self.slack_panel.use_case:
            QMessageBox.warning(self, "Slack", "❌ Slack no está configurado. Ve a la pestaña Slack.")
            return
        idx = self.combo_destino_main.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Slack", "❌ Selecciona un canal o usuario.")
            return
        canal_id = self.combo_destino_main.currentData()
        tarea = self._get_tarea_actual_dominio()
        if not tarea:
            QMessageBox.warning(self, "Slack", "❌ No hay tarea para enviar.")
            return
        try:
            resultado = self.slack_panel.use_case.enviar_reporte_qa(tarea, canal_id)
            estado = 'Éxito' if resultado else 'Error'
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            usuario = self.slack_panel.usuario_input.text().strip() or 'desconocido'
            mensaje = formatear_tarea_qa_para_historial(tarea)
            destino = self.combo_destino_main.currentText()
            db.save_historial_envio(fecha, destino, mensaje, estado, usuario)
            self.slack_panel._load_historial()
            if resultado:
                QMessageBox.information(self, "Slack", f"✅ Enviado a {destino}")
            else:
                QMessageBox.warning(self, "Slack", f"❌ Error al enviar a {destino}")
        except Exception as e:
            QMessageBox.warning(self, "Slack", f"❌ Error: {e}")

    def _get_tarea_actual(self):
        return self.controller.tarea

    def _get_tarea_actual_dominio(self):
        # Convierte el modelo local a la entidad de dominio
        tarea = self.controller.tarea
        ambientes = [DomainAmbientePR(a.ambiente, a.pr) for a in tarea.ambientes_prs]
        comentarios = [DomainComentarioQA(DomainTipoQA.from_string(c.tipo), c.link, c.ambiente, c.instruccion) for c in tarea.comentarios]
        return DomainTareaQA(
            titulo=tarea.titulo,
            jira=tarea.jira,
            ambientes_prs=ambientes,
            comentarios=comentarios,
            qa_usabilidad=list(tarea.qa_usabilidad),
            qa_codigo=list(tarea.qa_codigo)
        )

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

class QAGeneratorApp:
    """Clase principal de la aplicación siguiendo Clean Architecture"""
    
    def __init__(self):
        self.config = UIConfig()
        self.controller = TareaQAController()
        self.app = None
        self.window = None
    
    def initialize(self):
        """Inicializa la aplicación"""
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        self.window = MainWindow(self.controller, self.config)
        self.window.show()
    
    def run(self):
        """Ejecuta la aplicación"""
        if not self.app:
            self.initialize()
        
        if self.app:
            return self.app.exec()
        return 1
    
    def cleanup(self):
        """Limpia recursos de la aplicación"""
        if self.app:
            self.app.quit()

def formatear_tarea_qa_para_historial(tarea):
    ambientes_prs_text = "\n".join(f"- {item}" for item in tarea.ambientes_prs)
    comentarios_text = "\n\n".join(str(comentario) for comentario in tarea.comentarios)
    qa_usu_text = "\n".join(f"- {item}" for item in tarea.qa_usabilidad)
    qa_cod_text = "\n".join(f"- {item}" for item in tarea.qa_codigo)
    return f"""*Tarea:* {tarea.titulo}
*Jira:* {tarea.jira}

*Ambientes + PRs:*
{ambientes_prs_text if ambientes_prs_text else '- Sin registros agregados'}

*Comentarios:*
{comentarios_text if comentarios_text else '- Sin comentarios agregados'}

*Responsables:*
*QA Usabilidad:*
{qa_usu_text if qa_usu_text else '- Ninguno'}
*QA Código:*
{qa_cod_text if qa_cod_text else '- Ninguno'}
"""

def main():
    """Función principal de la aplicación"""
    try:
        app = QAGeneratorApp()
        return app.run()
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")
        return 1
    finally:
        if 'app' in locals():
            app.cleanup()

if __name__ == "__main__":
    sys.exit(main()) 