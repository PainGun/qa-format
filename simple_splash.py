"""
Pantalla de inicio con imagen de fondo para QA Generator
"""

import os
from PyQt6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor
from styles import ThemeManager


class SimpleSplashScreen(QSplashScreen):
    """Pantalla de splash con imagen de fondo"""
    
    splash_finished = pyqtSignal()
    
    def __init__(self):
        # Intentar cargar la imagen de fondo
        background_path = os.path.join(os.path.dirname(__file__), "assets", "backgorund_splash.png")
        
        if os.path.exists(background_path):
            # Cargar la imagen de fondo
            pixmap = QPixmap(background_path)
            
            # Redimensionar si es necesario (máximo 400x300)
            if pixmap.width() > 400 or pixmap.height() > 300:
                pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            # Fallback: crear pixmap transparente
            pixmap = QPixmap(350, 250)
            pixmap.fill(Qt.GlobalColor.transparent)
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        
        # Configurar el mensaje inicial
        self.showMessage("🚀 Iniciando QA Generator...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        
        # Guardar si tenemos imagen de fondo
        self.has_background_image = os.path.exists(background_path)
        
        # Variables para la barra de progreso
        self.progress_value = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(50)  # Actualizar cada 50ms
        
    def paintEvent(self, event):
        """Dibuja la pantalla de splash"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Si no tenemos imagen de fondo, dibujar fondo manual
        if not self.has_background_image:
            # Obtener colores según el tema
            if ThemeManager.get_current_theme() == 'dark':
                bg_color = QColor("#282a36")
                border_color = QColor("#6272a4")
            else:
                bg_color = QColor("#FFFFFF")
                border_color = QColor("#616DB3")
            
            # Fondo
            painter.fillRect(rect, bg_color)
            
            # Borde
            painter.setPen(border_color)
            painter.drawRect(rect.adjusted(1, 1, -1, -1))
        
        # Configurar colores del texto
        if ThemeManager.get_current_theme() == 'dark':
            title_color = QColor("#f8f8f2")
            text_color = QColor("#f8f8f2")
            accent_color = QColor("#6272a4")
        else:
            title_color = QColor("#FFFFFF")
            text_color = QColor("#FFFFFF")
            accent_color = QColor("#616DB3")
        
        # Título principal
        title_font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(title_color)
        
        title_rect = rect.adjusted(0, 0, 0, -100)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, "🚀 QA Generator")
        
        # Subtítulo
        subtitle_font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(subtitle_font)
        painter.setPen(text_color)
        
        subtitle_rect = rect.adjusted(0, 60, 0, -40)
        painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignCenter, "Generador Automático de QA")
        
        # Descripción
        desc_font = QFont("Arial", 9, QFont.Weight.Bold)
        painter.setFont(desc_font)
        painter.setPen(text_color)
        
        desc_rect = rect.adjusted(0, 90, 0, -10)
        painter.drawText(desc_rect, Qt.AlignmentFlag.AlignCenter, "Integración con GitHub y Jira")
        
        # Versión
        version_font = QFont("Arial", 8)
        painter.setFont(version_font)
        version_color = QColor(text_color)
        version_color.setAlpha(200)
        painter.setPen(version_color)
        version_rect = rect.adjusted(0, 0, 0, -30)  # Ajustar para dejar espacio a la barra
        painter.drawText(version_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, "v1.0.0")
        
        # Barra de progreso en la parte inferior
        progress_height = 6
        progress_rect = rect.adjusted(20, rect.height() - progress_height - 10, -20, -10)
        
        # Fondo de la barra de progreso
        progress_bg_color = QColor("#2c3e50")
        progress_bg_color.setAlpha(150)
        painter.fillRect(progress_rect, progress_bg_color)
        
        # Barra de progreso actual
        if self.progress_value > 0:
            progress_width = int((progress_rect.width() * self.progress_value) / 100)
            progress_fill_rect = progress_rect.adjusted(0, 0, -progress_rect.width() + progress_width, 0)
            
            # Color azul claro para la barra de progreso
            progress_color = QColor("#3498db")  # Azul claro
            progress_color.setAlpha(220)
            painter.fillRect(progress_fill_rect, progress_color)
            
            # Efecto de brillo en la barra
            highlight_color = QColor("#5dade2")  # Azul más claro
            highlight_color.setAlpha(180)
            highlight_rect = progress_fill_rect.adjusted(0, 0, 0, -progress_height//2)
            painter.fillRect(highlight_rect, highlight_color)
        
        painter.end()
    
    def update_progress(self):
        """Actualiza el progreso de la barra"""
        if self.progress_value < 100:
            self.progress_value += 3.33  # Velocidad de progreso ajustada para 1.5 segundos
            self.update()  # Redibujar
        else:
            self.progress_timer.stop()
    
    def start_splash(self, duration_ms=1500):
        """Inicia la pantalla de splash"""
        self.show()
        
        # Cambiar mensaje progresivamente (ajustado para 1.5 segundos)
        QTimer.singleShot(300, lambda: self.showMessage("🔧 Cargando configuración...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white))
        QTimer.singleShot(600, lambda: self.showMessage("🎨 Inicializando temas...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white))
        QTimer.singleShot(900, lambda: self.showMessage("🚀 Configurando servicios...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white))
        QTimer.singleShot(1200, lambda: self.showMessage("✨ Preparando interfaz...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white))
        
        # Finalizar splash
        QTimer.singleShot(duration_ms, self._close_splash)
    
    def _close_splash(self):
        """Cierra la pantalla y emite señal"""
        self.progress_timer.stop()
        self.splash_finished.emit()
        self.close()
