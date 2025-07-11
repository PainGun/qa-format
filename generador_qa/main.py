#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Generador QA
Implementa Clean Architecture con Tkinter
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importaciones
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Función principal de la aplicación"""
    try:
        # Importar después de configurar el path
        from infrastructure.ui.views.main_window_slack import GeneradorQAMainWindow
        
        # Crear y ejecutar la aplicación principal con integración Slack
        app = GeneradorQAMainWindow()
        app.run()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de que todas las dependencias estén instaladas.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
