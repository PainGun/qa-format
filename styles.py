"""
Estilos CSS para la aplicación PyQt6 - Tema Oscuro
Archivo separado para mantener los estilos organizados y fáciles de modificar
"""

class DarkTheme:
    """Clase que contiene todos los estilos del tema oscuro"""
    
    # Colores del tema oscuro
    COLORS = {
        'background': '#282a36',        # Fondo principal
        'current_line': '#44475a',      # Línea actual
        'selection': '#44475a',         # Selección
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
            background-color: {DarkTheme.COLORS['background']};
            color: {DarkTheme.COLORS['foreground']};
        }}
        QWidget {{
            background-color: {DarkTheme.COLORS['background']};
            color: {DarkTheme.COLORS['foreground']};
            font-family: 'Arial', sans-serif;
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
            border: 2px solid {DarkTheme.COLORS['current_line']};
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: {DarkTheme.COLORS['current_line']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 8px 15px 8px 15px;
            color: {DarkTheme.COLORS['foreground']};
            font-size: 14px;
            font-weight: bold;
            background-color: {DarkTheme.COLORS['purple']};
            border-radius: 6px;
            border: 1px solid #9580e0;
        }}
        """
    
    @staticmethod
    def get_label_style():
        """Estilos para QLabel"""
        return f"""
        QLabel {{
            color: {DarkTheme.COLORS['foreground']};
            font-weight: bold;
        }}
        """
    
    @staticmethod
    def get_lineedit_style():
        """Estilos para QLineEdit (campos de texto)"""
        return f"""
        QLineEdit {{
            background-color: {DarkTheme.COLORS['comment']};
            border: 2px solid #565b5e;
            border-radius: 6px;
            padding: 8px;
            color: {DarkTheme.COLORS['foreground']};
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: {DarkTheme.COLORS['purple']};
        }}
        QLineEdit::placeholder {{
            color: {DarkTheme.COLORS['cyan']};
        }}
        """
    
    @staticmethod
    def get_button_style():
        """Estilos para QPushButton"""
        return f"""
        QPushButton {{
            background-color: {DarkTheme.COLORS['comment']};
            border: 2px solid {DarkTheme.COLORS['purple']};
            border-radius: 8px;
            padding: 12px 18px;
            color: {DarkTheme.COLORS['foreground']};
            font-weight: bold;
            font-size: 13px;
            min-height: 20px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: {DarkTheme.COLORS['green']};
            border-color: #45d668;
            color: {DarkTheme.COLORS['background']};
        }}
        QPushButton:pressed {{
            background-color: #45d668;
            border-color: #3bc95a;
        }}
        QPushButton#deleteBtn {{
            background-color: {DarkTheme.COLORS['red']};
            max-width: 40px;
            padding: 8px;
        }}
        QPushButton#deleteBtn:hover {{
            background-color: #ff6e6e;
        }}
        QPushButton#clearBtn {{
            background-color: {DarkTheme.COLORS['red']};
        }}
        QPushButton#clearBtn:hover {{
            background-color: #ff6e6e;
        }}
        """
    
    @staticmethod
    def get_textedit_style():
        """Estilos para QTextEdit (áreas de texto)"""
        return f"""
        QTextEdit {{
            background-color: {DarkTheme.COLORS['current_line']};
            border: 2px solid #565b5e;
            border-radius: 6px;
            padding: 8px;
            color: {DarkTheme.COLORS['foreground']};
            font-size: 12px;
        }}
        QTextEdit:focus {{
            border-color: {DarkTheme.COLORS['purple']};
        }}
        """
    
    @staticmethod
    def get_listwidget_style():
        """Estilos para QListWidget (listas)"""
        return f"""
        QListWidget {{
            background-color: {DarkTheme.COLORS['current_line']};
            border: 2px solid #565b5e;
            border-radius: 6px;
            color: {DarkTheme.COLORS['foreground']};
            font-size: 11px;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 5px;
            border-bottom: 1px solid {DarkTheme.COLORS['comment']};
        }}
        QListWidget::item:selected {{
            background-color: {DarkTheme.COLORS['purple']};
            color: {DarkTheme.COLORS['background']};
        }}
        """
    
    @staticmethod
    def get_scrollbar_style():
        """Estilos para las barras de desplazamiento"""
        return f"""
        QScrollBar:vertical {{
            background-color: {DarkTheme.COLORS['current_line']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {DarkTheme.COLORS['comment']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {DarkTheme.COLORS['green']};
        }}
        """
    
    @staticmethod
    def get_scrollarea_style():
        """Estilos para QScrollArea"""
        return f"""
        QScrollArea {{
            border: none;
            background-color: {DarkTheme.COLORS['background']};
        }}
        """
    
    @staticmethod
    def get_frame_style():
        """Estilos para QFrame"""
        return f"""
        QFrame {{
            background-color: transparent;
        }}
        """
    
    @staticmethod
    def get_title_label_style():
        """Estilo especial para el título principal"""
        return f"""
            color: {DarkTheme.COLORS['foreground']}; 
            background-color: {DarkTheme.COLORS['comment']};
            padding: 15px;
            border-radius: 8px;
            border: 2px solid {DarkTheme.COLORS['purple']};
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
