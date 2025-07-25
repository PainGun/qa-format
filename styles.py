"""
Estilos CSS para la aplicación PyQt6 - Sistema de Temas
Archivo separado para mantener los estilos organizados y fáciles de modificar
Soporte para temas oscuro y claro con toggle dinámico
"""

class LightTheme:
    """Clase que contiene todos los estilos del tema claro"""
    
    # Paleta de colores tema claro
    COLORS = {
        'background': '#FFFFFF',        # Fondo blanco
        'current_line': '#F5F7FA',      # Línea actual (gris muy claro)
        'selection': '#A4B3DC',         # Selección (azul claro)
        'foreground': '#3D3D3D',        # Texto principal (gris oscuro)
        'comment': '#616DB3',           # Comentarios (azul principal)
        'cyan': '#616DB3',              # Cyan (azul principal)
        'green': '#28A745',             # Verde (mantener funcional)
        'orange': '#FACC53',            # Naranja (amarillo acento)
        'pink': '#A4B3DC',              # Rosa (azul claro)
        'purple': '#616DB3',            # Morado (azul principal)
        'red': '#DC3545',               # Rojo (mantener funcional)
        'yellow': '#FACC53'             # Amarillo (amarillo acento)
    }
    
    @staticmethod
    def get_main_stylesheet():
        """Retorna el stylesheet principal para la aplicación"""
        return f"""
        QMainWindow {{
            background-color: #FFFFFF;
            color: #3D3D3D;
        }}
        QWidget {{
            background-color: #FFFFFF;
            color: #3D3D3D;
            font-family: 'Arial', sans-serif;
        }}
        QFrame {{
            background-color: #FFFFFF;
            color: #3D3D3D;
        }}
        QTabWidget::pane {{
            border: 2px solid #616DB3;
            background-color: #FFFFFF;
            border-radius: 6px;
        }}
        QTabBar::tab {{
            background-color: #F5F7FA;
            color: #3D3D3D;
            padding: 8px 16px;
            margin: 2px;
            border-radius: 6px;
            border: 1px solid #616DB3;
        }}
        QTabBar::tab:selected {{
            background-color: #616DB3;
            color: #FFFFFF;
        }}
        QTabBar::tab:hover {{
            background-color: #A4B3DC;
        }}
        {LightTheme.get_groupbox_style()}
        {LightTheme.get_label_style()}
        {LightTheme.get_lineedit_style()}
        {LightTheme.get_button_style()}
        {LightTheme.get_textedit_style()}
        {LightTheme.get_listwidget_style()}
        {LightTheme.get_scrollbar_style()}
        {LightTheme.get_scrollarea_style()}
        {LightTheme.get_frame_style()}
        """
    
    @staticmethod
    def get_groupbox_style():
        """Estilos para QGroupBox (secciones)"""
        return f"""
        QGroupBox {{
            font-weight: bold;
            border: 2px solid #616DB3;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: #F5F7FA;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 8px 15px 8px 15px;
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
            background-color: #616DB3;
            border-radius: 6px;
            border: 1px solid #616DB3;
        }}
        """
    
    @staticmethod
    def get_label_style():
        """Estilos para QLabel"""
        return f"""
        QLabel {{
            color: #3D3D3D;
            background-color: transparent;
            padding: 2px;
        }}
        QLabel[styleClass="title"] {{
            font-weight: bold;
            font-size: 14px;
            color: #616DB3;
        }}
        QLabel[styleClass="subtitle"] {{
            font-weight: bold;
            font-size: 12px;
            color: #3D3D3D;
        }}
        QLabel[styleClass="info"] {{
            font-size: 10px;
            color: #616DB3;
        }}
        """
    
    @staticmethod
    def get_lineedit_style():
        """Estilos para QLineEdit (campos de texto)"""
        return f"""
        QLineEdit {{
            background-color: #F5F7FA;
            border: 2px solid #616DB3;
            border-radius: 6px;
            padding: 8px;
            color: #3D3D3D;
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: #616DB3;
            background-color: #FFFFFF;
        }}
        QLineEdit::placeholder {{
            color: #616DB3;
        }}
        QComboBox {{
            background-color: #F5F7FA;
            border: 2px solid #616DB3;
            border-radius: 6px;
            padding: 8px;
            color: #3D3D3D;
            font-size: 12px;
        }}
        QComboBox:focus {{
            border-color: #616DB3;
            background-color: #FFFFFF;
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: transparent;
        }}
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTcgMTBMMTIgNUgyWiIgZmlsbD0iIzNEM0QzRCIvPgo8L3N2Zz4K);
        }}
        """
    
    @staticmethod
    def get_button_style():
        """Estilos para QPushButton"""
        return f"""
        QPushButton {{
            background-color: #F5F7FA;
            border: 2px solid #616DB3;
            border-radius: 8px;
            padding: 12px 18px;
            color: #3D3D3D;
            font-weight: bold;
            font-size: 13px;
            min-height: 20px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: #616DB3;
            border-color: #616DB3;
            color: #FFFFFF;
        }}
        QPushButton:pressed {{
            background-color: #616DB3;
            border-color: #616DB3;
            color: #FFFFFF;
        }}
        QPushButton:disabled {{
            background-color: #E0E0E0;
            border-color: #CCCCCC;
            color: #999999;
        }}
        QPushButton#deleteBtn {{
            background-color: #DC3545;
            max-width: 40px;
            padding: 8px;
            color: #FFFFFF;
        }}
        QPushButton#deleteBtn:hover {{
            background-color: #C82333;
            color: #FFFFFF;
        }}
        QPushButton#clearBtn {{
            background-color: #DC3545;
            color: #FFFFFF;
        }}
        QPushButton#clearBtn:hover {{
            background-color: #C82333;
            color: #FFFFFF;
        }}
        """
    
    @staticmethod
    def get_textedit_style():
        """Estilos para QTextEdit (áreas de texto)"""
        return f"""
        QTextEdit {{
            background-color: #F5F7FA;
            border: 2px solid #616DB3;
            border-radius: 6px;
            padding: 8px;
            color: #3D3D3D;
            font-size: 12px;
        }}
        QTextEdit:focus {{
            border-color: #616DB3;
            background-color: #FFFFFF;
        }}
        """
    
    @staticmethod
    def get_listwidget_style():
        """Estilos para QListWidget (listas)"""
        return f"""
        QListWidget {{
            background-color: #F5F7FA;
            border: 2px solid #616DB3;
            border-radius: 6px;
            color: #3D3D3D;
            font-size: 11px;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 5px;
            border-bottom: 1px solid #A4B3DC;
        }}
        QListWidget::item:selected {{
            background-color: #616DB3;
            color: #FFFFFF;
        }}
        """
    
    @staticmethod
    def get_scrollbar_style():
        """Estilos para las barras de desplazamiento"""
        return f"""
        QScrollBar:vertical {{
            background-color: #F5F7FA;
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: #616DB3;
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #616DB3;
        }}
        """
    
    @staticmethod
    def get_scrollarea_style():
        """Estilos para QScrollArea"""
        return f"""
        QScrollArea {{
            border: none;
            background-color: #FFFFFF;
        }}
        """
    
    @staticmethod
    def get_frame_style():
        """Estilos para QFrame"""
        return f"""
        QFrame {{
            background-color: #FFFFFF;
            color: #3D3D3D;
            border: none;
        }}
        """
    
    @staticmethod
    def get_title_label_style():
        """Estilo especial para el título principal"""
        return f"""
            color: #3D3D3D; 
            background-color: #F5F7FA;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #616DB3;
            margin: 10px;
        """

class DarkTheme:
    """Clase que contiene todos los estilos del tema oscuro"""
    
    # Paleta de colores tema oscuro
    COLORS = {
        'background': '#282a36',        # Fondo oscuro
        'current_line': '#44475a',      # Línea actual
        'selection': '#6272a4',         # Selección
        'foreground': '#f8f8f2',        # Texto principal
        'comment': '#6272a4',           # Comentarios
        'cyan': '#8be9fd',              # Cyan
        'green': '#50fa7b',             # Verde
        'orange': '#ffb86c',            # Naranja
        'pink': '#ff79c6',              # Rosa
        'purple': '#bd93f9',            # Morado
        'red': '#ff5555',               # Rojo
        'yellow': '#f1fa8c'             # Amarillo
    }
    
    @staticmethod
    def get_main_stylesheet():
        """Retorna el stylesheet principal para la aplicación"""
        return f"""
        QMainWindow {{
            background-color: #282a36;
            color: #f8f8f2;
        }}
        QWidget {{
            background-color: #282a36;
            color: #f8f8f2;
            font-family: 'Arial', sans-serif;
        }}
        QFrame {{
            background-color: #282a36;
            color: #f8f8f2;
        }}
        QTabWidget::pane {{
            border: 2px solid #6272a4;
            background-color: #282a36;
            border-radius: 6px;
        }}
        QTabBar::tab {{
            background-color: #44475a;
            color: #f8f8f2;
            padding: 8px 16px;
            margin: 2px;
            border-radius: 6px;
            border: 1px solid #6272a4;
        }}
        QTabBar::tab:selected {{
            background-color: #6272a4;
            color: #f8f8f2;
        }}
        QTabBar::tab:hover {{
            background-color: #6272a4;
        }}
        {DarkTheme.get_groupbox_style()}
        {DarkTheme.get_label_style()}
        {DarkTheme.get_lineedit_style()}
        {DarkTheme.get_button_style()}
        {DarkTheme.get_textedit_style()}
        {DarkTheme.get_listwidget_style()}
        {DarkTheme.get_scrollbar_style()}
        {DarkTheme.get_scrollarea_style()}
        {DarkTheme.get_frame_style()}
        """
    
    @staticmethod
    def get_groupbox_style():
        """Estilos para QGroupBox (secciones)"""
        return f"""
        QGroupBox {{
            font-weight: bold;
            border: 2px solid #6272a4;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: #44475a;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 8px 15px 8px 15px;
            color: #f8f8f2;
            font-size: 14px;
            font-weight: bold;
            background-color: #6272a4;
            border-radius: 6px;
            border: 1px solid #6272a4;
        }}
        """
    
    @staticmethod
    def get_label_style():
        """Estilos para QLabel"""
        return f"""
        QLabel {{
            color: #f8f8f2;
            background-color: transparent;
            padding: 2px;
        }}
        QLabel[styleClass="title"] {{
            font-weight: bold;
            font-size: 14px;
            color: #bd93f9;
        }}
        QLabel[styleClass="subtitle"] {{
            font-weight: bold;
            font-size: 12px;
            color: #f8f8f2;
        }}
        QLabel[styleClass="info"] {{
            font-size: 10px;
            color: #6272a4;
        }}
        """
    
    @staticmethod
    def get_lineedit_style():
        """Estilos para QLineEdit (campos de texto)"""
        return f"""
        QLineEdit {{
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: #bd93f9;
            background-color: #44475a;
        }}
        QLineEdit::placeholder {{
            color: #6272a4;
        }}
        QComboBox {{
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 12px;
        }}
        QComboBox:focus {{
            border-color: #bd93f9;
            background-color: #44475a;
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: transparent;
        }}
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTcgMTBMMTIgNUgyWiIgZmlsbD0iI2Y4ZjhmMiIvPgo8L3N2Zz4K);
        }}
        """
    
    @staticmethod
    def get_button_style():
        """Estilos para QPushButton"""
        return f"""
        QPushButton {{
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 8px;
            padding: 12px 18px;
            color: #f8f8f2;
            font-weight: bold;
            font-size: 13px;
            min-height: 20px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: #6272a4;
            border-color: #bd93f9;
            color: #f8f8f2;
        }}
        QPushButton:pressed {{
            background-color: #6272a4;
            border-color: #bd93f9;
            color: #f8f8f2;
        }}
        QPushButton:disabled {{
            background-color: #282a36;
            border-color: #44475a;
            color: #6272a4;
        }}
        QPushButton#deleteBtn {{
            background-color: #ff5555;
            max-width: 40px;
            padding: 8px;
            color: #f8f8f2;
        }}
        QPushButton#deleteBtn:hover {{
            background-color: #ff6b6b;
            color: #f8f8f2;
        }}
        QPushButton#clearBtn {{
            background-color: #ff5555;
            color: #f8f8f2;
        }}
        QPushButton#clearBtn:hover {{
            background-color: #ff6b6b;
            color: #f8f8f2;
        }}
        """
    
    @staticmethod
    def get_textedit_style():
        """Estilos para QTextEdit (áreas de texto)"""
        return f"""
        QTextEdit {{
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 12px;
        }}
        QTextEdit:focus {{
            border-color: #bd93f9;
            background-color: #44475a;
        }}
        """
    
    @staticmethod
    def get_listwidget_style():
        """Estilos para QListWidget (listas)"""
        return f"""
        QListWidget {{
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            color: #f8f8f2;
            font-size: 11px;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 5px;
            border-bottom: 1px solid #6272a4;
        }}
        QListWidget::item:selected {{
            background-color: #6272a4;
            color: #f8f8f2;
        }}
        """
    
    @staticmethod
    def get_scrollbar_style():
        """Estilos para las barras de desplazamiento"""
        return f"""
        QScrollBar:vertical {{
            background-color: #44475a;
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: #6272a4;
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #bd93f9;
        }}
        """
    
    @staticmethod
    def get_scrollarea_style():
        """Estilos para QScrollArea"""
        return f"""
        QScrollArea {{
            border: none;
            background-color: #282a36;
        }}
        """
    
    @staticmethod
    def get_frame_style():
        """Estilos para QFrame"""
        return f"""
        QFrame {{
            background-color: #282a36;
            color: #f8f8f2;
            border: none;
        }}
        """
    
    @staticmethod
    def get_title_label_style():
        """Estilo especial para el título principal"""
        return f"""
            color: #f8f8f2; 
            background-color: #44475a;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #6272a4;
            margin: 10px;
        """

# Clase para gestionar el tema global
class ThemeManager:
    """Gestor de temas global para la aplicación"""
    
    _current_theme = 'light'  # Tema por defecto
    _theme_changed_callbacks = []
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Inicializa el gestor de temas con la configuración guardada"""
        if not cls._initialized:
            try:
                from config import app_config
                saved_theme = app_config.get_theme()
                cls._current_theme = saved_theme
                cls._initialized = True
            except ImportError:
                # Si no existe config.py, usar tema por defecto
                cls._current_theme = 'light'
                cls._initialized = True
    
    @classmethod
    def set_theme(cls, theme_name):
        """Establece el tema actual"""
        cls.initialize()
        if theme_name in AVAILABLE_THEMES:
            cls._current_theme = theme_name
            
            # Guardar en configuración
            try:
                from config import app_config
                app_config.set_theme(theme_name)
            except ImportError:
                pass
            
            # Notificar a todos los callbacks registrados
            for callback in cls._theme_changed_callbacks:
                try:
                    callback(theme_name)
                except Exception as e:
                    print(f"Error en callback de tema: {e}")
    
    @classmethod
    def get_current_theme(cls):
        """Obtiene el tema actual"""
        cls.initialize()
        return cls._current_theme
    
    @classmethod
    def get_theme_class(cls):
        """Obtiene la clase del tema actual"""
        cls.initialize()
        return AVAILABLE_THEMES.get(cls._current_theme, LightTheme)
    
    @classmethod
    def register_theme_changed_callback(cls, callback):
        """Registra un callback para cuando cambie el tema"""
        cls._theme_changed_callbacks.append(callback)
    
    @classmethod
    def unregister_theme_changed_callback(cls, callback):
        """Desregistra un callback"""
        if callback in cls._theme_changed_callbacks:
            cls._theme_changed_callbacks.remove(callback)
    
    @classmethod
    def toggle_theme(cls):
        """Alterna entre tema claro y oscuro"""
        cls.initialize()
        new_theme = 'dark' if cls._current_theme == 'light' else 'light'
        cls.set_theme(new_theme)
        return new_theme
    
    @classmethod
    def get_main_stylesheet(cls):
        """Obtiene el stylesheet principal del tema actual"""
        cls.initialize()
        return cls.get_theme_class().get_main_stylesheet()

# Temas disponibles
AVAILABLE_THEMES = {
    'light': LightTheme,
    'dark': DarkTheme
}

def get_theme(theme_name='light'):
    """
    Obtiene una clase de tema por nombre
    
    Args:
        theme_name (str): Nombre del tema ('light', 'dark')
        
    Returns:
        Theme class: Clase del tema solicitado
    """
    return AVAILABLE_THEMES.get(theme_name, LightTheme)

# Nota: Las clases DarkTheme y LightTheme están disponibles directamente
# El ThemeManager maneja automáticamente cuál usar
