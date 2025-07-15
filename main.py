import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTextEdit, QListWidget, QScrollArea, QFrame,
                           QMessageBox, QGroupBox, QGridLayout, QSizePolicy,
                           QTabWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QClipboard
from controllers import TareaQAController
from styles import DarkTheme
try:
    from github_widget import GitHubWidget
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    print("⚠️ GitHub widget no disponible - asegúrate de tener PyGithub instalado")

try:
    from jira_widget import JiraWidget
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False
    print("⚠️ Jira widget no disponible - asegúrate de tener jira instalado")

class QAGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 Generador Paso a QA - PyQt6 MVC")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(1000, 700)
        
        # Inicializar el controlador MVC
        self.controller = TareaQAController()
        
        # Lista de widgets para manejo de cierre
        self.widgets_with_threads = []
        
        # Aplicar tema oscuro
        self.setStyleSheet(DarkTheme.get_main_stylesheet())
        
        # Crear widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear sistema de pestañas
        self.tab_widget = QTabWidget()
        
        # Pestaña del generador QA
        self.create_qa_tab()
        
        # Pestaña de GitHub (si está disponible)
        if GITHUB_AVAILABLE:
            self.github_widget = self.create_github_tab()
            self.widgets_with_threads.append(self.github_widget)
        
        # Pestaña de Jira (si está disponible)
        if JIRA_AVAILABLE:
            self.jira_widget = self.create_jira_tab()
            self.widgets_with_threads.append(self.jira_widget)
        
        # Pestaña del chatbot RFlex (al final)
        self.create_rflex_chatbot_tab()
        
        main_layout.addWidget(self.tab_widget)
        
    def create_qa_tab(self):
        """Crea la pestaña del generador QA"""
        qa_tab = QWidget()
        
        # Layout principal con scroll para la pestaña QA
        qa_layout = QVBoxLayout(qa_tab)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title_label = QLabel("📋 FORMULARIO DE QA")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3D3D3D; background-color: #F5F7FA; padding: 15px; border-radius: 8px; border: 2px solid #616DB3; margin: 10px;")
        scroll_layout.addWidget(title_label)
        
        # Crear secciones
        self.create_basic_info_section(scroll_layout)
        self.create_environments_section(scroll_layout)
        self.create_comments_section(scroll_layout)
        self.create_qa_responsibles_section(scroll_layout)
        self.create_actions_section(scroll_layout)
        self.create_result_section(scroll_layout)
        
        # Configurar scroll
        scroll_area.setWidget(scroll_widget)
        qa_layout.addWidget(scroll_area)
        
        # Agregar pestaña al tab widget
        self.tab_widget.addTab(qa_tab, "📋 Generador QA")
        
    def create_rflex_chatbot_tab(self):
        """Crea la pestaña del chatbot RFlex"""
        chatbot_tab = QWidget()
        chatbot_layout = QVBoxLayout(chatbot_tab)
        chatbot_layout.setSpacing(30)
        chatbot_layout.setContentsMargins(50, 50, 50, 50)
        
        # Título de la pestaña
        chatbot_title = QLabel("🤖 CHATBOT RFLEX")
        chatbot_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        chatbot_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chatbot_title.setStyleSheet("color: #3D3D3D; background-color: #F5F7FA; padding: 15px; border-radius: 8px; border: 2px solid #616DB3; margin: 10px;")
        chatbot_layout.addWidget(chatbot_title)
        
        # Mensaje de desarrollo
        dev_message = QLabel("🚧 EN DESARROLLO 🚧")
        dev_message.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        dev_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_message.setStyleSheet("""
            QLabel {
                color: #FACC53;
                background-color: #F5F7FA;
                border: 2px dashed #FACC53;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
            }
        """)
        chatbot_layout.addWidget(dev_message)
        
        # Descripción
        description = QLabel("""
        Esta funcionalidad estará disponible próximamente.
        
        El chatbot RFlex te permitirá:
        • 💬 Chatear con IA especializada en QA
        • 🔍 Analizar código y documentación
        • 📝 Generar casos de prueba automáticamente
        • 🚀 Optimizar procesos de testing
        """)
        description.setFont(QFont("Arial", 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("""
            QLabel {
                color: #3D3D3D;
                background-color: #F5F7FA;
                border: 2px solid #A4B3DC;
                border-radius: 8px;
                padding: 20px;
                line-height: 1.6;
            }
        """)
        chatbot_layout.addWidget(description)
        
        # Espacio flexible
        chatbot_layout.addStretch()
        
        # Agregar pestaña al tab widget
        self.tab_widget.addTab(chatbot_tab, "🤖 Chat RFlex")
        
    def create_github_tab(self):
        """Crea la pestaña de GitHub"""
        github_tab = QWidget()
        github_layout = QVBoxLayout(github_tab)
        
        # Título de la pestaña
        github_title = QLabel("🐙 INTEGRACIÓN GITHUB")
        github_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        github_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_title.setStyleSheet("color: #3D3D3D; background-color: #F5F7FA; padding: 15px; border-radius: 8px; border: 2px solid #616DB3; margin: 10px;")
        github_layout.addWidget(github_title)
        
        # Widget de GitHub
        github_widget = GitHubWidget()
        github_layout.addWidget(github_widget)
        
        # Agregar pestaña al tab widget
        self.tab_widget.addTab(github_tab, "🐙 GitHub")
        
        return github_widget
        
    def create_jira_tab(self):
        """Crea la pestaña de Jira"""
        jira_tab = QWidget()
        jira_layout = QVBoxLayout(jira_tab)
        
        # Título de la pestaña
        jira_title = QLabel("🔧 INTEGRACIÓN JIRA")
        jira_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        jira_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        jira_title.setStyleSheet("color: #3D3D3D; background-color: #F5F7FA; padding: 15px; border-radius: 8px; border: 2px solid #616DB3; margin: 10px;")
        jira_layout.addWidget(jira_title)
        
        # Widget de Jira
        jira_widget = JiraWidget()
        jira_layout.addWidget(jira_widget)
        
        # Agregar pestaña al tab widget
        self.tab_widget.addTab(jira_tab, "🔧 Jira")
        
        return jira_widget

    def create_basic_info_section(self, layout):
        """Crea la sección de información básica"""
        group = QGroupBox("📌 INFORMACIÓN BÁSICA")
        group_layout = QVBoxLayout()
        
        # Título de la tarea
        title_layout = QHBoxLayout()
        titulo_label = QLabel("📝 Título de la Tarea:")
        titulo_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        title_layout.addWidget(titulo_label)
        self.entry_titulo = QLineEdit()
        self.entry_titulo.setPlaceholderText("Ingrese el título de la tarea")
        title_layout.addWidget(self.entry_titulo)
        group_layout.addLayout(title_layout)
        
        # Jira
        jira_layout = QHBoxLayout()
        jira_label = QLabel("🔗 Link Jira:")
        jira_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        jira_layout.addWidget(jira_label)
        self.entry_jira = QLineEdit()
        self.entry_jira.setPlaceholderText("https://jira.empresa.com/...")
        jira_layout.addWidget(self.entry_jira)
        group_layout.addLayout(jira_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def create_environments_section(self, layout):
        """Crea la sección de ambientes y PRs"""
        group = QGroupBox("🌐 AMBIENTES + PRs")
        group_layout = QVBoxLayout()
        
        # Inputs
        inputs_layout = QHBoxLayout()
        
        # Ambiente
        ambiente_layout = QVBoxLayout()
        ambiente_label = QLabel("🏢 Ambiente:")
        ambiente_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        ambiente_layout.addWidget(ambiente_label)
        self.entry_ambiente = QLineEdit()
        self.entry_ambiente.setPlaceholderText("dev, staging, prod...")
        ambiente_layout.addWidget(self.entry_ambiente)
        inputs_layout.addLayout(ambiente_layout)
        
        # PR
        pr_layout = QVBoxLayout()
        pr_label = QLabel("🔄 PR:")
        pr_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        pr_layout.addWidget(pr_label)
        self.entry_pr = QLineEdit()
        self.entry_pr.setPlaceholderText("Número o link del PR")
        pr_layout.addWidget(self.entry_pr)
        inputs_layout.addLayout(pr_layout)
        
        group_layout.addLayout(inputs_layout)
        
        # Botón agregar
        btn_agregar_amb = QPushButton("➕ Agregar Ambiente + PR")
        btn_agregar_amb.clicked.connect(self.agregar_ambiente_pr)
        group_layout.addWidget(btn_agregar_amb)
        
        # Lista y botón eliminar
        list_layout = QHBoxLayout()
        self.lista_ambientes_prs = QListWidget()
        self.lista_ambientes_prs.setMaximumHeight(100)
        list_layout.addWidget(self.lista_ambientes_prs)
        
        btn_eliminar_amb = QPushButton("🗑️")
        btn_eliminar_amb.setObjectName("deleteBtn")
        btn_eliminar_amb.clicked.connect(lambda: self.eliminar_seleccionado(self.lista_ambientes_prs))
        list_layout.addWidget(btn_eliminar_amb)
        
        group_layout.addLayout(list_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def create_comments_section(self, layout):
        """Crea la sección de comentarios"""
        group = QGroupBox("💬 COMENTARIOS DE PRUEBA")
        group_layout = QVBoxLayout()
        
        # Primera fila
        fila1_layout = QHBoxLayout()
        
        tipo_layout = QVBoxLayout()
        tipo_label = QLabel("🔍 Tipo QA:")
        tipo_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        tipo_layout.addWidget(tipo_label)
        self.entry_tipo_qa = QLineEdit()
        self.entry_tipo_qa.setPlaceholderText("Usabilidad / Código")
        tipo_layout.addWidget(self.entry_tipo_qa)
        fila1_layout.addLayout(tipo_layout)
        
        link_layout = QVBoxLayout()
        link_label = QLabel("🔗 Link para prueba:")
        link_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        link_layout.addWidget(link_label)
        self.entry_link_qa = QLineEdit()
        self.entry_link_qa.setPlaceholderText("URL de la aplicación")
        link_layout.addWidget(self.entry_link_qa)
        fila1_layout.addLayout(link_layout)
        
        group_layout.addLayout(fila1_layout)
        
        # Segunda fila
        ambiente_layout = QVBoxLayout()
        ambiente_qa_label = QLabel("🌐 Ambiente de prueba:")
        ambiente_qa_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        ambiente_layout.addWidget(ambiente_qa_label)
        self.entry_ambiente_qa = QLineEdit()
        self.entry_ambiente_qa.setPlaceholderText("Ambiente donde probar")
        ambiente_layout.addWidget(self.entry_ambiente_qa)
        group_layout.addLayout(ambiente_layout)
        
        # Instrucciones
        instr_layout = QVBoxLayout()
        instr_label = QLabel("📝 Instrucciones:")
        instr_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        instr_layout.addWidget(instr_label)
        self.txt_instruccion = QTextEdit()
        self.txt_instruccion.setPlaceholderText("Pasos detallados para realizar la prueba...")
        self.txt_instruccion.setMaximumHeight(80)
        instr_layout.addWidget(self.txt_instruccion)
        group_layout.addLayout(instr_layout)
        
        # Botón agregar
        btn_agregar_com = QPushButton("➕ Agregar Comentario")
        btn_agregar_com.clicked.connect(self.agregar_comentario)
        group_layout.addWidget(btn_agregar_com)
        
        # Lista y botón eliminar
        list_layout = QHBoxLayout()
        self.lista_comentarios = QListWidget()
        self.lista_comentarios.setMaximumHeight(100)
        list_layout.addWidget(self.lista_comentarios)
        
        btn_eliminar_com = QPushButton("🗑️")
        btn_eliminar_com.setObjectName("deleteBtn")
        btn_eliminar_com.clicked.connect(lambda: self.eliminar_seleccionado(self.lista_comentarios))
        list_layout.addWidget(btn_eliminar_com)
        
        group_layout.addLayout(list_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)

    
    def create_qa_responsibles_section(self, layout):
        """Crea la sección de responsables QA"""
        group = QGroupBox("👥 RESPONSABLES QA")
        group_layout = QVBoxLayout()
        
        # QA Usabilidad
        usu_layout = QVBoxLayout()
        usu_label = QLabel("🎨 QA Usabilidad:")
        usu_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        usu_layout.addWidget(usu_label)
        
        usu_input_layout = QHBoxLayout()
        self.entry_qa_usu = QLineEdit()
        self.entry_qa_usu.setPlaceholderText("Nombre del responsable de QA Usabilidad")
        usu_input_layout.addWidget(self.entry_qa_usu)
        
        btn_agregar_usu = QPushButton("➕")
        btn_agregar_usu.clicked.connect(self.agregar_qa_usu)
        usu_input_layout.addWidget(btn_agregar_usu)
        
        usu_layout.addLayout(usu_input_layout)
        
        usu_list_layout = QHBoxLayout()
        self.lista_qa_usu = QListWidget()
        self.lista_qa_usu.setMaximumHeight(60)
        usu_list_layout.addWidget(self.lista_qa_usu)
        
        btn_eliminar_usu = QPushButton("🗑️")
        btn_eliminar_usu.setObjectName("deleteBtn")
        btn_eliminar_usu.clicked.connect(lambda: self.eliminar_seleccionado(self.lista_qa_usu))
        usu_list_layout.addWidget(btn_eliminar_usu)
        
        usu_layout.addLayout(usu_list_layout)
        group_layout.addLayout(usu_layout)
        
        # QA Código
        cod_layout = QVBoxLayout()
        cod_label = QLabel("💻 QA Código:")
        cod_label.setStyleSheet("color: #3D3D3D; font-weight: bold;")
        cod_layout.addWidget(cod_label)
        
        cod_input_layout = QHBoxLayout()
        self.entry_qa_cod = QLineEdit()
        self.entry_qa_cod.setPlaceholderText("Nombre del responsable de QA Código")
        cod_input_layout.addWidget(self.entry_qa_cod)
        
        btn_agregar_cod = QPushButton("➕")
        btn_agregar_cod.clicked.connect(self.agregar_qa_cod)
        cod_input_layout.addWidget(btn_agregar_cod)
        
        cod_layout.addLayout(cod_input_layout)
        
        cod_list_layout = QHBoxLayout()
        self.lista_qa_cod = QListWidget()
        self.lista_qa_cod.setMaximumHeight(60)
        cod_list_layout.addWidget(self.lista_qa_cod)
        
        btn_eliminar_cod = QPushButton("🗑️")
        btn_eliminar_cod.setObjectName("deleteBtn")
        btn_eliminar_cod.clicked.connect(lambda: self.eliminar_seleccionado(self.lista_qa_cod))
        cod_list_layout.addWidget(btn_eliminar_cod)
        
        cod_layout.addLayout(cod_list_layout)
        group_layout.addLayout(cod_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def create_actions_section(self, layout):
        """Crea la sección de botones de acción"""
        group = QGroupBox("⚡ ACCIONES")
        group_layout = QHBoxLayout()
        
        btn_generar = QPushButton("🚀 Generar Texto")
        btn_generar.clicked.connect(self.generar_texto)
        group_layout.addWidget(btn_generar)
        
        btn_copiar = QPushButton("📋 Copiar al Portapapeles")
        btn_copiar.clicked.connect(self.copiar_texto)
        group_layout.addWidget(btn_copiar)
        
        btn_limpiar = QPushButton("🧹 Limpiar Todo")
        btn_limpiar.setObjectName("clearBtn")
        btn_limpiar.clicked.connect(self.limpiar_formulario)
        group_layout.addWidget(btn_limpiar)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def create_result_section(self, layout):
        """Crea la sección de resultado"""
        group = QGroupBox("📄 RESULTADO GENERADO")
        group_layout = QVBoxLayout()
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setMinimumHeight(300)
        self.resultado_text.setReadOnly(True)
        group_layout.addWidget(self.resultado_text)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def eliminar_seleccionado(self, listbox):
        """Elimina el elemento seleccionado de una lista usando el controlador"""
        current_row = listbox.currentRow()
        if current_row >= 0:
            # Determinar qué tipo de lista es y usar el controlador apropiado
            if listbox == self.lista_ambientes_prs:
                if self.controller.eliminar_ambiente_pr(current_row):
                    listbox.takeItem(current_row)
            elif listbox == self.lista_comentarios:
                if self.controller.eliminar_comentario(current_row):
                    listbox.takeItem(current_row)
            elif listbox == self.lista_qa_usu:
                if self.controller.eliminar_qa_usabilidad(current_row):
                    listbox.takeItem(current_row)
            elif listbox == self.lista_qa_cod:
                if self.controller.eliminar_qa_codigo(current_row):
                    listbox.takeItem(current_row)
    
    def agregar_ambiente_pr(self):
        """Agrega ambiente y PR usando el controlador"""
        ambiente = self.entry_ambiente.text().strip()
        pr = self.entry_pr.text().strip()
        
        if self.controller.agregar_ambiente_pr(ambiente, pr):
            # Usar el formateo del controlador
            item_texto = self.controller.formatear_ambiente_pr_para_ui(ambiente, pr)
            self.lista_ambientes_prs.addItem(item_texto)
            self.entry_ambiente.clear()
            self.entry_pr.clear()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete ambos campos.")
    
    def agregar_comentario(self):
        """Agrega comentario usando el controlador"""
        tipo = self.entry_tipo_qa.text().strip()
        link = self.entry_link_qa.text().strip()
        ambiente = self.entry_ambiente_qa.text().strip()
        instruccion = self.txt_instruccion.toPlainText().strip()
        
        if self.controller.agregar_comentario(tipo, link, ambiente, instruccion):
            # Usar el formateo del controlador
            comentario_texto = self.controller.formatear_comentario_para_ui(tipo, link, ambiente, instruccion)
            self.lista_comentarios.addItem(comentario_texto)
            self.entry_tipo_qa.clear()
            self.entry_link_qa.clear()
            self.entry_ambiente_qa.clear()
            self.txt_instruccion.clear()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos.")
    
    def agregar_qa_usu(self):
        """Agrega QA Usabilidad usando el controlador"""
        qa = self.entry_qa_usu.text().strip()
        if self.controller.agregar_qa_usabilidad(qa):
            self.lista_qa_usu.addItem(qa)
            self.entry_qa_usu.clear()
        else:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingrese un nombre.")
    
    def agregar_qa_cod(self):
        """Agrega QA Código usando el controlador"""
        qa = self.entry_qa_cod.text().strip()
        if self.controller.agregar_qa_codigo(qa):
            self.lista_qa_cod.addItem(qa)
            self.entry_qa_cod.clear()
        else:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingrese un nombre.")
    
    def generar_texto(self):
        """Genera el texto usando el controlador"""
        # Actualizar el controlador con los datos actuales de la UI
        self.controller.actualizar_titulo(self.entry_titulo.text())
        self.controller.actualizar_jira(self.entry_jira.text())
        
        # Generar el texto usando el controlador
        resultado = self.controller.generar_texto()
        self.resultado_text.setPlainText(resultado)
    
    def copiar_texto(self):
        """Copia el texto al portapapeles usando el controlador"""
        texto = self.resultado_text.toPlainText()
        if self.controller.copiar_al_portapapeles(texto):
            QMessageBox.information(self, "✅ Copiado", "Texto copiado al portapapeles exitosamente.")
        else:
            QMessageBox.warning(self, "❌ Error", "No se pudo copiar al portapapeles.")
    
    def limpiar_formulario(self):
        """Limpia todos los campos usando el controlador"""
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
    
    def sincronizar_ui_con_controlador(self):
        """Sincroniza toda la UI con los datos del controlador"""
        # Obtener todas las listas del controlador
        listas = self.controller.obtener_todas_las_listas_para_ui()
        
        # Limpiar listas UI
        self.lista_ambientes_prs.clear()
        self.lista_comentarios.clear()
        self.lista_qa_usu.clear()
        self.lista_qa_cod.clear()
        
        # Poblar listas UI con datos del controlador
        for item in listas['ambientes_prs']:
            self.lista_ambientes_prs.addItem(item)
        
        for item in listas['comentarios']:
            self.lista_comentarios.addItem(item)
            
        for item in listas['qa_usabilidad']:
            self.lista_qa_usu.addItem(item)
            
        for item in listas['qa_codigo']:
            self.lista_qa_cod.addItem(item)

    def cleanup_threads(self):
        """Limpia todos los threads activos antes del cierre"""
        print("🧹 Limpiando threads...")
        
        # Limpiar threads de widgets específicos
        for widget in self.widgets_with_threads:
            if hasattr(widget, 'cleanup_threads'):
                print(f"🧽 Limpiando threads de {widget.__class__.__name__}")
                widget.cleanup_threads()
        
        print("✅ Threads limpiados")
    
    def closeEvent(self, event):
        """Maneja el evento de cierre de la aplicación"""
        print("🚪 Cerrando aplicación...")
        self.cleanup_threads()
        super().closeEvent(event)
        print("👋 Aplicación cerrada correctamente")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = QAGenerator()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
