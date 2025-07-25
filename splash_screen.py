"""
Pantalla de inicio (Splash Screen) para QA Generator
"""

from PyQt6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor, QLinearGradient
from styles import ThemeManager


class SplashScreen(QSplashScreen):
    """Pantalla de splash animada con tema"""
    
    splash_finished = pyqtSignal()
    
    def __init__(self):
        # Crear un pixmap transparente como base
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        
        self.progress_value = 0
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Configura la interfaz de la pantalla de splash"""
        # Obtener tema actual
        theme_class = ThemeManager.get_theme_class()
        
        # Definir colores según el tema
        if ThemeManager.get_current_theme() == 'dark':
            accent_color = '#6272a4'
            text_color = '#f8f8f2'
            secondary_text_color = '#9ca3af'
            background_color = '#282a36'
            secondary_background_color = '#44475a'
            selection_color = '#bd93f9'
        else:
            accent_color = '#616DB3'
            text_color = '#3D3D3D'
            secondary_text_color = '#6B7280'
            background_color = '#FFFFFF'
            secondary_background_color = '#F5F7FA'
            selection_color = '#A4B3DC'
        
        # Crear widget central
        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo/Título principal
        title_label = QLabel("🚀 QA Generator")
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {accent_color};
                background: transparent;
                padding: 10px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Generador Automático de QA")
        subtitle_font = QFont("Arial", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                background: transparent;
                opacity: 0.8;
            }}
        """)
        layout.addWidget(subtitle_label)
        
        # Descripción
        desc_label = QLabel("Integración con GitHub y Jira")
        desc_font = QFont("Arial", 10)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {secondary_text_color};
                background: transparent;
                padding: 5px;
            }}
        """)
        layout.addWidget(desc_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {secondary_background_color};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {accent_color},
                    stop:1 {selection_color});
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Estado de carga
        self.status_label = QLabel("Iniciando aplicación...")
        status_font = QFont("Arial", 9)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {secondary_text_color};
                background: transparent;
                padding: 5px;
            }}
        """)
        layout.addWidget(self.status_label)
        
        # Versión
        version_label = QLabel("v1.0.0")
        version_font = QFont("Arial", 8)
        version_label.setFont(version_font)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"""
            QLabel {{
                color: {secondary_text_color};
                background: transparent;
                opacity: 0.6;
                padding: 5px;
            }}
        """)
        layout.addWidget(version_label)
        
        # Aplicar el widget central (esto no funciona directamente en QSplashScreen)
        # En su lugar, vamos a dibujar todo manualmente
        
    def setup_animation(self):
        """Configura las animaciones y timers"""
        # Timer para actualizar progreso
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        
        # Timer para finalizar splash
        self.finish_timer = QTimer()
        self.finish_timer.timeout.connect(self.finish_splash)
        self.finish_timer.setSingleShot(True)
        
    def paintEvent(self, event):
        """Dibuja la pantalla de splash personalizada"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Definir colores según el tema
        if ThemeManager.get_current_theme() == 'dark':
            bg_color_1 = QColor("#44475a")
            bg_color_2 = QColor("#282a36")
            accent_color = QColor("#6272a4")
            text_color = QColor("#f8f8f2")
            secondary_text_color = QColor("#9ca3af")
        else:
            bg_color_1 = QColor("#f8f9fa")
            bg_color_2 = QColor("#e9ecef")
            accent_color = QColor("#616DB3")
            text_color = QColor("#3D3D3D")
            secondary_text_color = QColor("#6B7280")
        
        # Fondo con gradiente
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, bg_color_1)
        gradient.setColorAt(1, bg_color_2)
        
        painter.fillRect(rect, gradient)
        
        # Borde sutil
        border_color = QColor(accent_color)
        border_color.setAlpha(100)
        painter.setPen(border_color)
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        
        # Título principal
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(accent_color)
        
        title_rect = rect.adjusted(0, 80, 0, -180)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, "🚀 QA Generator")
        
        # Subtítulo
        subtitle_font = QFont("Arial", 12)
        painter.setFont(subtitle_font)
        painter.setPen(text_color)
        
        subtitle_rect = rect.adjusted(0, 120, 0, -140)
        painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignCenter, "Generador Automático de QA")
        
        # Descripción
        desc_font = QFont("Arial", 10)
        painter.setFont(desc_font)
        painter.setPen(secondary_text_color)
        
        desc_rect = rect.adjusted(0, 150, 0, -110)
        painter.drawText(desc_rect, Qt.AlignmentFlag.AlignCenter, "Integración con GitHub y Jira")
        
        # Barra de progreso
        progress_rect = rect.adjusted(80, 200, -80, -80)
        
        # Fondo de la barra de progreso
        if ThemeManager.get_current_theme() == 'dark':
            progress_bg = QColor("#44475a")
        else:
            progress_bg = QColor("#F5F7FA")
        
        painter.fillRect(progress_rect, progress_bg)
        
        # Progreso actual
        if self.progress_value > 0:
            progress_width = int((progress_rect.width() * self.progress_value) / 100)
            progress_fill_rect = progress_rect.adjusted(0, 0, -progress_rect.width() + progress_width, 0)
            
            # Crear gradiente usando coordenadas explícitas
            progress_gradient = QLinearGradient(
                progress_fill_rect.left(), progress_fill_rect.top(),
                progress_fill_rect.right(), progress_fill_rect.top()
            )
            progress_gradient.setColorAt(0, accent_color)
            
            if ThemeManager.get_current_theme() == 'dark':
                progress_gradient.setColorAt(1, QColor("#bd93f9"))
            else:
                progress_gradient.setColorAt(1, QColor("#A4B3DC"))
            
            painter.fillRect(progress_fill_rect, progress_gradient)
        
        # Estado
        status_font = QFont("Arial", 9)
        painter.setFont(status_font)
        painter.setPen(secondary_text_color)
        
        status_rect = rect.adjusted(0, 230, 0, -50)
        painter.drawText(status_rect, Qt.AlignmentFlag.AlignCenter, self.get_current_status())
        
        # Versión
        version_font = QFont("Arial", 8)
        painter.setFont(version_font)
        version_color = QColor(secondary_text_color)
        version_color.setAlpha(150)
        painter.setPen(version_color)
        
        version_rect = rect.adjusted(0, 260, 0, -20)
        painter.drawText(version_rect, Qt.AlignmentFlag.AlignCenter, "v1.0.0")
        
        # Cerrar el painter correctamente
        painter.end()
        
    def get_current_status(self):
        """Obtiene el mensaje de estado actual según el progreso"""
        if self.progress_value < 20:
            return "Iniciando aplicación..."
        elif self.progress_value < 40:
            return "Cargando configuración..."
        elif self.progress_value < 60:
            return "Inicializando temas..."
        elif self.progress_value < 80:
            return "Configurando servicios..."
        elif self.progress_value < 95:
            return "Preparando interfaz..."
        else:
            return "¡Listo!"
    
    def start_splash(self, duration_ms=3000):
        """Inicia la pantalla de splash"""
        self.show()
        
        # Iniciar animación de progreso
        self.progress_timer.start(50)  # Actualizar cada 50ms
        
        # Programar finalización
        self.finish_timer.start(duration_ms)
        
    def update_progress(self):
        """Actualiza el progreso de la barra"""
        if self.progress_value < 100:
            self.progress_value += 2
            self.update()  # Redibujar
        else:
            self.progress_timer.stop()
    
    def finish_splash(self):
        """Finaliza la pantalla de splash"""
        self.progress_timer.stop()
        self.progress_value = 100
        self.update()
        
        # Pequeña pausa antes de cerrar
        QTimer.singleShot(200, self._close_splash)
    
    def _close_splash(self):
        """Cierra la pantalla y emite señal"""
        self.splash_finished.emit()
        self.close()


class MinimalSplashScreen(QSplashScreen):
    """Versión minimalista de la pantalla de splash"""
    
    splash_finished = pyqtSignal()
    
    def __init__(self):
        pixmap = QPixmap(300, 200)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        
    def paintEvent(self, event):
        """Dibuja versión minimalista"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Colores según el tema
        if ThemeManager.get_current_theme() == 'dark':
            bg_color = QColor("#282a36")
            accent_color = QColor("#6272a4")
        else:
            bg_color = QColor("#FFFFFF")
            accent_color = QColor("#616DB3")
        
        # Fondo simple
        painter.fillRect(rect, bg_color)
        
        # Borde
        painter.setPen(accent_color)
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        
        # Título centrado
        font = QFont("Arial", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(accent_color)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "🚀 QA Generator")
        
        # Cerrar el painter correctamente
        painter.end()
    
    def start_splash(self, duration_ms=2000):
        """Inicia splash minimalista"""
        self.show()
        QTimer.singleShot(duration_ms, self._close_splash)
    
    def _close_splash(self):
        """Cierra splash minimalista"""
        self.splash_finished.emit()
        self.close()
