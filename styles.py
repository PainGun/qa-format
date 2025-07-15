"""
Estilos CSS para la aplicación PyQt6 - Tema Personalizado
Archivo separado para mantener los estilos organizados y fáciles de modificar
Paleta: Fondo blanco, azul principal (#616DB3), azul claro (#A4B3DC), gris oscuro (#3D3D3D), amarillo acento (#FACC53)
"""

class DarkTheme:
    """Clase que contiene todos los estilos del tema personalizado"""
    
    # Paleta de colores personalizada
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
            font-weight: bold;
            background-color: transparent;
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

# Clase adicional para otros temas (preparado para futuras expansiones)
class LightTheme:
    """Tema claro (para futuras implementaciones)"""
    
    COLORS = {
        'background': '#ffffff',
        'foreground': '#333333',
        'primary': '#007acc',
        'secondary': '#f0f0f0'
    }
    
    @staticmethod
    def get_main_stylesheet():
        """Placeholder para tema claro"""
        return "/* Light theme - Por implementar */"

# Temas disponibles
AVAILABLE_THEMES = {
    'dark': DarkTheme,
    'light': LightTheme
}

def get_theme(theme_name='dark'):
    """
    Obtiene una clase de tema por nombre
    
    Args:
        theme_name (str): Nombre del tema ('dark', 'light')
        
    Returns:
        Theme class: Clase del tema solicitado
    """
    return AVAILABLE_THEMES.get(theme_name, DarkTheme)
