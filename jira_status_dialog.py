"""
Diálogo para cambiar el estado de un issue de Jira
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QComboBox, QTextEdit, QMessageBox,
                           QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from styles import ThemeManager

class TransitionWorker(QThread):
    """Worker para realizar transiciones en background"""
    transition_completed = pyqtSignal(bool, str)
    
    def __init__(self, jira_service, issue_key, transition_id, comment):
        super().__init__()
        self.jira_service = jira_service
        self.issue_key = issue_key
        self.transition_id = transition_id
        self.comment = comment
        
    def run(self):
        try:
            success = self.jira_service.transition_issue(
                self.issue_key, 
                self.transition_id, 
                self.comment if self.comment.strip() else None
            )
            self.transition_completed.emit(success, "Transición realizada exitosamente")
        except Exception as e:
            self.transition_completed.emit(False, str(e))

class JiraStatusDialog(QDialog):
    """Diálogo para cambiar el estado de un issue"""
    
    status_changed = pyqtSignal(str, str)  # issue_key, new_status
    
    def __init__(self, parent, jira_service, issue_data):
        super().__init__(parent)
        self.jira_service = jira_service
        self.issue_data = issue_data
        self.transitions = []
        self.worker = None
        
        self.setWindowTitle(f"🔄 Cambiar Estado - {issue_data['key']}")
        self.setModal(True)
        self.setFixedSize(500, 400)
        self.setup_ui()
        self.load_transitions()
        
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Aplicar estilos
        self.setStyleSheet(ThemeManager.get_theme_class().get_main_stylesheet())
        
        # Información del issue
        info_label = QLabel(f"📋 {self.issue_data['key']}: {self.issue_data['summary']}")
        info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #f8f8f2; background-color: #44475a; padding: 10px; border-radius: 6px;")
        layout.addWidget(info_label)
        
        # Estado actual
        current_status = QLabel(f"🏷️ Estado Actual: {self.issue_data['status']}")
        current_status.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        current_status.setStyleSheet("color: #50fa7b; padding: 5px;")
        layout.addWidget(current_status)
        
        # Selector de nuevo estado
        status_label = QLabel("🎯 Cambiar a:")
        status_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(status_label)
        
        self.status_combo = QComboBox()
        self.status_combo.setStyleSheet(ThemeManager.get_theme_class().get_lineedit_style())
        self.status_combo.addItem("🔄 Cargando estados disponibles...")
        layout.addWidget(self.status_combo)
        
        # Comentario
        comment_label = QLabel("💬 Comentario (opcional):")
        comment_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(comment_label)
        
        self.comment_text = QTextEdit()
        self.comment_text.setMaximumHeight(100)
        self.comment_text.setPlaceholderText("Agregar un comentario sobre el cambio de estado...")
        self.comment_text.setStyleSheet(ThemeManager.get_theme_class().get_textedit_style())
        layout.addWidget(self.comment_text)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #6272a4;
                border-radius: 6px;
                background-color: #44475a;
                color: #f8f8f2;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: #50fa7b;
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.change_btn = QPushButton("🔄 Cambiar Estado")
        self.change_btn.clicked.connect(self.change_status)
        self.change_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        self.change_btn.setEnabled(False)
        buttons_layout.addWidget(self.change_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(ThemeManager.get_theme_class().get_button_style())
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_transitions(self):
        """Carga las transiciones disponibles para el issue"""
        try:
            self.transitions = self.jira_service.get_issue_transitions(self.issue_data['key'])
            
            self.status_combo.clear()
            if not self.transitions:
                self.status_combo.addItem("❌ No hay transiciones disponibles")
                return
            
            self.status_combo.addItem("Selecciona un nuevo estado...")
            for transition in self.transitions:
                self.status_combo.addItem(f"➡️ {transition['to_status']}")
                self.status_combo.setItemData(self.status_combo.count() - 1, transition)
            
            self.status_combo.currentIndexChanged.connect(self.on_status_selected)
            
        except Exception as e:
            self.status_combo.clear()
            self.status_combo.addItem(f"❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los estados disponibles:\n{str(e)}")
    
    def on_status_selected(self, index):
        """Maneja la selección de un nuevo estado"""
        if index > 0 and index <= len(self.transitions):
            self.change_btn.setEnabled(True)
        else:
            self.change_btn.setEnabled(False)
    
    def change_status(self):
        """Cambia el estado del issue"""
        current_index = self.status_combo.currentIndex()
        if current_index <= 0:
            return
            
        transition_data = self.status_combo.itemData(current_index)
        if not transition_data:
            return
        
        # Confirmar el cambio
        reply = QMessageBox.question(
            self, 
            "Confirmar Cambio",
            f"¿Estás seguro de cambiar el estado de {self.issue_data['key']} a '{transition_data['to_status']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Deshabilitar botones y mostrar progreso
        self.change_btn.setEnabled(False)
        self.status_combo.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Realizar la transición en un hilo separado
        comment = self.comment_text.toPlainText().strip()
        self.worker = TransitionWorker(
            self.jira_service,
            self.issue_data['key'],
            transition_data['id'],
            comment
        )
        self.worker.transition_completed.connect(self.on_transition_completed)
        self.worker.start()
    
    def on_transition_completed(self, success, message):
        """Maneja el resultado de la transición"""
        self.progress_bar.setVisible(False)
        self.change_btn.setEnabled(True)
        self.status_combo.setEnabled(True)
        
        if success:
            # Emitir señal de cambio exitoso
            new_status = self.status_combo.itemData(self.status_combo.currentIndex())['to_status']
            self.status_changed.emit(self.issue_data['key'], new_status)
            
            QMessageBox.information(self, "✅ Éxito", f"Estado cambiado exitosamente a '{new_status}'")
            self.accept()
        else:
            QMessageBox.critical(self, "❌ Error", f"Error al cambiar estado:\n{message}")
