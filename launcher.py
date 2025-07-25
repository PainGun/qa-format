#!/usr/bin/env python3
"""
Launcher principal para QA Generator con pantalla de splash
"""

import sys
import argparse
from PyQt6.QtWidgets import QApplication
from main import QAGenerator
from splash_screen import SplashScreen, MinimalSplashScreen
from styles import ThemeManager


def main():
    """Función principal con opciones de splash"""
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='QA Generator - Generador Automático de QA')
    parser.add_argument('--no-splash', action='store_true', 
                       help='Saltar pantalla de inicio')
    parser.add_argument('--minimal-splash', action='store_true',
                       help='Usar pantalla de inicio minimalista')
    parser.add_argument('--splash-duration', type=int, default=3000,
                       help='Duración del splash en milisegundos (default: 3000)')
    parser.add_argument('--theme', choices=['light', 'dark'], 
                       help='Tema inicial (light o dark)')
    
    args = parser.parse_args()
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Configurar tema inicial si se especifica
    if args.theme:
        ThemeManager.set_theme(args.theme)
    
    # Variable para la ventana principal
    window = None
    
    def show_main_window():
        """Muestra la ventana principal"""
        nonlocal window
        window = QAGenerator()
        window.show()
        
        # Mensaje de bienvenida en consola
        print("🎉 ¡QA Generator iniciado correctamente!")
        print(f"🎨 Tema activo: {ThemeManager.get_current_theme()}")
        print("💡 Usa el toggle en la barra superior para cambiar el tema")
    
    if args.no_splash:
        # Iniciar directamente sin splash
        print("🚀 Iniciando QA Generator (sin splash)...")
        show_main_window()
    
    elif args.minimal_splash:
        # Usar splash minimalista
        print("🌟 Iniciando QA Generator (splash minimalista)...")
        splash = MinimalSplashScreen()
        splash.splash_finished.connect(show_main_window)
        splash.start_splash(args.splash_duration)
    
    else:
        # Usar splash completo (por defecto)
        print("✨ Iniciando QA Generator (splash completo)...")
        splash = SplashScreen()
        splash.splash_finished.connect(show_main_window)
        splash.start_splash(args.splash_duration)
    
    # Ejecutar aplicación
    return app.exec()


def run_with_splash():
    """Launcher simple con splash por defecto"""
    return main()


def run_without_splash():
    """Launcher simple sin splash"""
    sys.argv.append('--no-splash')
    return main()


def run_minimal_splash():
    """Launcher simple con splash minimalista"""
    sys.argv.append('--minimal-splash')
    return main()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Aplicación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)
