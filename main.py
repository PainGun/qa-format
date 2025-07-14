import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTextEdit, QListWidget, QScrollArea, QFrame,
                           QMessageBox, QGroupBox, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QClipboard
from controllers import TareaQAController
from styles import DarkTheme

class QAGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 Generador Paso a QA - PyQt6 MVC")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(1000, 700)
        
        # Inicializar el controlador MVC
        self.controller = TareaQAController()
        
        # Aplicar tema oscuro
        self.setStyleSheet(DarkTheme.get_main_stylesheet())
        
        # Crear widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal con scroll
        main_layout = QVBoxLayout(central_widget)
        
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
        title_label.setStyleSheet(DarkTheme.get_title_label_style())
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
        main_layout.addWidget(scroll_area)
        
    def create_basic_info_section(self, layout):
        """Crea la sección de información básica"""
        group = QGroupBox("📌 INFORMACIÓN BÁSICA")
        group_layout = QVBoxLayout()
        
        # Título de la tarea
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("📝 Título de la Tarea:"))
        self.entry_titulo = QLineEdit()
        self.entry_titulo.setPlaceholderText("Ingrese el título de la tarea")
        title_layout.addWidget(self.entry_titulo)
        group_layout.addLayout(title_layout)
        
        # Jira
        jira_layout = QHBoxLayout()
        jira_layout.addWidget(QLabel("🔗 Link Jira:"))
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
        ambiente_layout.addWidget(QLabel("🏢 Ambiente:"))
        self.entry_ambiente = QLineEdit()
        self.entry_ambiente.setPlaceholderText("dev, staging, prod...")
        ambiente_layout.addWidget(self.entry_ambiente)
        inputs_layout.addLayout(ambiente_layout)
        
        # PR
        pr_layout = QVBoxLayout()
        pr_layout.addWidget(QLabel("🔄 PR:"))
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
        tipo_layout.addWidget(QLabel("🔍 Tipo QA:"))
        self.entry_tipo_qa = QLineEdit()
        self.entry_tipo_qa.setPlaceholderText("Usabilidad / Código")
        tipo_layout.addWidget(self.entry_tipo_qa)
        fila1_layout.addLayout(tipo_layout)
        
        link_layout = QVBoxLayout()
        link_layout.addWidget(QLabel("🔗 Link para prueba:"))
        self.entry_link_qa = QLineEdit()
        self.entry_link_qa.setPlaceholderText("URL de la aplicación")
        link_layout.addWidget(self.entry_link_qa)
        fila1_layout.addLayout(link_layout)
        
        group_layout.addLayout(fila1_layout)
        
        # Segunda fila
        ambiente_layout = QVBoxLayout()
        ambiente_layout.addWidget(QLabel("🌐 Ambiente de prueba:"))
        self.entry_ambiente_qa = QLineEdit()
        self.entry_ambiente_qa.setPlaceholderText("Ambiente donde probar")
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
        usu_layout.addWidget(QLabel("🎨 QA Usabilidad:"))
        
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
        cod_layout.addWidget(QLabel("💻 QA Código:"))
        
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

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = QAGenerator()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
