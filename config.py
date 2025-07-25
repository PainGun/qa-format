"""
Configuración de la aplicación QA Generator
"""

import json
import os
from pathlib import Path

class AppConfig:
    """Clase para manejar la configuración de la aplicación"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".qa_generator"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "theme": "light",
            "window_geometry": None,
            "github_token": None,
            "jira_server": None,
            "jira_username": None,
            "last_project": None
        }
        self.ensure_config_dir()
        self.config = self.load_config()
    
    def ensure_config_dir(self):
        """Asegura que el directorio de configuración exista"""
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Combinar con configuración por defecto
                    config = self.default_config.copy()
                    config.update(loaded_config)
                    return config
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return self.default_config.copy()
    
    def save_config(self):
        """Guarda la configuración actual"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def get(self, key, default=None):
        """Obtiene un valor de configuración"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Establece un valor de configuración"""
        self.config[key] = value
        self.save_config()
    
    def get_theme(self):
        """Obtiene el tema actual"""
        return self.get("theme", "light")
    
    def set_theme(self, theme):
        """Establece el tema actual"""
        self.set("theme", theme)

# Instancia global de configuración
app_config = AppConfig()
