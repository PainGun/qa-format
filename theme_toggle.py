"""
Widget de toggle para cambiar entre temas claro/oscuro
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QTimer
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QIcon
from styles import ThemeManager

class ThemeToggleSwitch(QWidget):
    """Widget personalizado para toggle de tema con animación"""
    
    theme_changed = pyqtSignal(str)  # Emite el nombre del tema
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 40)
        self.setObjectName("themeToggle")
        
        # Estado del toggle
        self.is_dark = ThemeManager.get_current_theme() == 'dark'
        
        # Colores del toggle
        self.bg_color_light = QColor("#F5F7FA")
        self.bg_color_dark = QColor("#44475a")
        self.handle_color_light = QColor("#616DB3")
        self.handle_color_dark = QColor("#bd93f9")
        self.border_color = QColor("#6272a4")
        
        # Animación
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        
        # Configurar cursor (no clickeable por ahora)
        self.setCursor(Qt.CursorShape.ForbiddenCursor)
        
        # Tooltip
        self.update_tooltip()
        
        # Registrar callback para cambios de tema
        ThemeManager.register_theme_changed_callback(self.on_theme_changed)
    
    def update_tooltip(self):
        """Actualiza el tooltip según el tema actual"""
        self.setToolTip("🚧 Tema claro activado - Tema oscuro en desarrollo 🌙✨")
    
    def mousePressEvent(self, event):
        """Maneja el click en el toggle"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Tema oscuro en desarrollo - mostrar mensaje
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, 
                "🚧 En Desarrollo", 
                "El tema oscuro está actualmente en desarrollo.\n\n"
                "Por ahora solo está disponible el tema claro.\n"
                "¡Pronto estará disponible! 🌙✨"
            )
        super().mousePressEvent(event)
    
    def toggle_theme(self):
        """Alterna entre temas"""
        new_theme = ThemeManager.toggle_theme()
        self.is_dark = new_theme == 'dark'
        self.update_tooltip()
        self.update()
        self.theme_changed.emit(new_theme)
    
    def on_theme_changed(self, theme_name):
        """Callback cuando cambia el tema externamente"""
        self.is_dark = theme_name == 'dark'
        self.update_tooltip()
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el toggle personalizado"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Colores deshabilitados (gris) para indicar que está en desarrollo
        bg_color = QColor("#6c6c6c")  # Gris para fondo
        handle_color = QColor("#9e9e9e")  # Gris claro para handle
        border_color = QColor("#757575")  # Gris para borde
        
        # Dibujar fondo del toggle (siempre en posición "claro")
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(2, 2, self.width()-4, self.height()-4, 18, 18)
        
        # Posición del handle (siempre en lado izquierdo para tema claro)
        handle_x = 6
        
        # Dibujar handle
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(handle_color))
        painter.drawEllipse(handle_x, 6, 28, 28)
        
        # Dibujar iconos deshabilitados
        painter.setPen(QPen(QColor("#8a8a8a"), 2))
        painter.setFont(QFont("Arial", 12))
        
        # Icono de sol (activo pero deshabilitado)
        painter.drawText(50, 26, "☀️")
        # Icono de luna (deshabilitado)
        painter.setPen(QPen(QColor("#666666"), 1))
        painter.drawText(10, 26, "🌙")
        
        # Agregar texto "DEV" pequeño para indicar desarrollo
        painter.setPen(QPen(QColor("#ff6b6b"), 1))
        painter.setFont(QFont("Arial", 7, QFont.Weight.Bold))
        painter.drawText(self.width() - 25, self.height() - 5, "DEV")

class ThemeToggleWidget(QWidget):
    """Widget completo con etiqueta y toggle"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Registrar callback para cambios de tema
        ThemeManager.register_theme_changed_callback(self.update_styles)
        
        # Aplicar estilos iniciales
        self.update_styles(ThemeManager.get_current_theme())
    
    def setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Etiqueta
        self.label = QLabel("🎨 Tema:")
        self.label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(self.label)
        
        # Toggle switch
        self.toggle_switch = ThemeToggleSwitch()
        self.toggle_switch.theme_changed.connect(self.on_theme_changed)
        layout.addWidget(self.toggle_switch)
        
        # Etiqueta del tema actual
        self.theme_label = QLabel()
        self.theme_label.setFont(QFont("Arial", 9))
        self.update_theme_label()
        layout.addWidget(self.theme_label)
        
        layout.addStretch()
    
    def update_theme_label(self):
        """Actualiza la etiqueta del tema actual"""
        current_theme = ThemeManager.get_current_theme()
        if current_theme == 'dark':
            self.theme_label.setText("🌙 Oscuro")
        else:
            self.theme_label.setText("☀️ Claro")
    
    def on_theme_changed(self, theme_name):
        """Maneja el cambio de tema"""
        self.update_theme_label()
        self.theme_changed.emit(theme_name)
    
    def update_styles(self, theme_name):
        """Actualiza los estilos según el tema"""
        theme_class = ThemeManager.get_theme_class()
        
        if theme_name == 'dark':
            label_color = "#f8f8f2"
            theme_label_color = "#bd93f9"
        else:
            label_color = "#3D3D3D"
            theme_label_color = "#616DB3"
        
        self.label.setStyleSheet(f"color: {label_color}; background-color: transparent;")
        self.theme_label.setStyleSheet(f"color: {theme_label_color}; background-color: transparent;")
        
        # Actualizar la etiqueta del tema
        self.update_theme_label()

class ThemeToggleButton(QPushButton):
    """Botón simple para toggle de tema"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Registrar callback para cambios de tema
        ThemeManager.register_theme_changed_callback(self.update_button)
        
        # Configurar evento click
        self.clicked.connect(self.toggle_theme)
        
        # Aplicar estilos iniciales
        self.update_button(ThemeManager.get_current_theme())
    
    def setup_ui(self):
        """Configura la interfaz del botón"""
        self.setFixedSize(120, 35)
        self.setObjectName("themeToggleButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def update_button(self, theme_name):
        """Actualiza el botón según el tema"""
        theme_class = ThemeManager.get_theme_class()
        
        if theme_name == 'dark':
            self.setText("☀️ Tema Claro")
            self.setToolTip("Cambiar a tema claro")
            button_style = """
            QPushButton#themeToggleButton {
                background-color: #44475a;
                border: 2px solid #6272a4;
                border-radius: 8px;
                padding: 8px 12px;
                color: #f8f8f2;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton#themeToggleButton:hover {
                background-color: #6272a4;
                border-color: #bd93f9;
            }
            """
        else:
            self.setText("🌙 Tema Oscuro")
            self.setToolTip("Cambiar a tema oscuro")
            button_style = """
            QPushButton#themeToggleButton {
                background-color: #F5F7FA;
                border: 2px solid #616DB3;
                border-radius: 8px;
                padding: 8px 12px;
                color: #3D3D3D;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton#themeToggleButton:hover {
                background-color: #616DB3;
                color: #FFFFFF;
            }
            """
        
        self.setStyleSheet(button_style)
    
    def toggle_theme(self):
        """Alterna entre temas"""
        new_theme = ThemeManager.toggle_theme()
        self.theme_changed.emit(new_theme)
