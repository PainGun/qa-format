#!/usr/bin/env python3
"""
Script para probar el sistema de temas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from main import QAGenerator

def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)
    
    # Crear ventana principal
    window = QAGenerator()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
