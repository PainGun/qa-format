"""
Widget de configuración de Slack para la UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from ....external.slack_notification_service import SlackNotificationService
from ....external.slack_client import SlackClient
import importlib
try:
    settings = importlib.import_module('config.settings')
except Exception:
    settings = None
from generador_qa.src.shared.utils import db


class SlackConfigWidget(tk.LabelFrame):
    """Widget para configurar y probar la integración con Slack"""
    
    def __init__(self, parent, on_slack_ready: Optional[Callable] = None, **kwargs):
        super().__init__(parent, text="🔗 Configuración de Slack", **kwargs)
        self.on_slack_ready = on_slack_ready
        self.slack_service = None
        db.init_db()  # Inicializar la base de datos
        self.setup_ui()
        # Cargar token y usuario automáticamente si existen en la base de datos
        token = db.get_config('slack_token')
        if token:
            self.entry_token.insert(0, token)
        usuario = db.get_config('slack_user')
        if usuario:
            self.entry_usuario.insert(0, usuario)
        if token:
            self.after(100, self.probar_conexion)  # Espera a que la UI esté lista antes de probar conexión
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Token de Slack
        tk.Label(main_frame, text="Token de Bot:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_token = tk.Entry(main_frame, width=50, show="*")
        self.entry_token.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Nombre de usuario
        tk.Label(main_frame, text="Tu usuario Slack (@...):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_usuario = tk.Entry(main_frame, width=30)
        self.entry_usuario.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Workspace (opcional)
        tk.Label(main_frame, text="Workspace:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_workspace = tk.Entry(main_frame, width=30)
        self.entry_workspace.insert(0, "slack.com")
        self.entry_workspace.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Frame de botones
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.btn_test = tk.Button(button_frame, text="🧪 Probar Conexión", 
                                command=self.probar_conexion)
        self.btn_test.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_save = tk.Button(button_frame, text="💾 Guardar Config", 
                                command=self.guardar_configuracion)
        self.btn_save.pack(side=tk.LEFT, padx=(0, 10))
        
        # Estado de conexión
        self.lbl_status = tk.Label(button_frame, text="❌ No configurado", 
                                 fg="red", font=("Arial", 9, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=(10, 0))
        
        # Frame de canales
        self.canales_frame = tk.LabelFrame(self, text="📢 Canales Disponibles")
        self.canales_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Lista de canales
        self.lista_canales = tk.Listbox(self.canales_frame, height=4)
        self.lista_canales.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón para refrescar canales
        self.btn_refresh = tk.Button(self.canales_frame, text="🔄 Refrescar Canales", 
                                   command=self.obtener_canales)
        self.btn_refresh.pack(pady=5)
        
        # Configurar grid
        main_frame.grid_columnconfigure(1, weight=1)
    
    def probar_conexion(self):
        """Prueba la conexión con Slack"""
        token = self.entry_token.get().strip()
        usuario = self.entry_usuario.get().strip()
        workspace = self.entry_workspace.get().strip()
        
        if not token:
            messagebox.showerror("Error", "El token de Slack es requerido")
            return
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario es requerido")
            return
        
        try:
            # Crear cliente temporal para probar
            client = SlackClient(token, workspace)
            
            if client.verificar_conexion():
                self.lbl_status.config(text="✅ Conectado", fg="green")
                messagebox.showinfo("Éxito", "Conexión con Slack establecida correctamente")
                
                # Crear servicio
                self.slack_service = SlackNotificationService(token, workspace)
                
                # Notificar que está listo
                if self.on_slack_ready:
                    self.on_slack_ready(self.slack_service)
                    
            else:
                self.lbl_status.config(text="❌ Error de conexión", fg="red")
                messagebox.showerror("Error", "No se pudo conectar con Slack. Verifica el token.")
                
        except Exception as e:
            self.lbl_status.config(text="❌ Error", fg="red")
            messagebox.showerror("Error", f"Error al conectar con Slack: {str(e)}")
    
    def guardar_configuracion(self):
        """Guarda la configuración de Slack"""
        token = self.entry_token.get().strip()
        usuario = self.entry_usuario.get().strip()
        workspace = self.entry_workspace.get().strip()
        
        if not token:
            messagebox.showerror("Error", "El token de Slack es requerido")
            return
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario es requerido")
            return
        
        try:
            db.set_config('slack_token', token)
            db.set_config('slack_user', usuario)
            messagebox.showinfo("Configuración", "Configuración guardada correctamente en la base de datos")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {str(e)}")
    
    def obtener_canales(self):
        """Obtiene la lista de canales disponibles"""
        if not self.slack_service:
            messagebox.showwarning("Advertencia", "Primero debes probar la conexión")
            return
        
        try:
            canales = self.slack_service.obtener_canales_disponibles()
            
            # Limpiar lista
            self.lista_canales.delete(0, tk.END)
            
            # Agregar canales
            for canal in canales:
                nombre = canal.get('name', 'Sin nombre')
                es_privado = "🔒" if canal.get('is_private', False) else "🌐"
                self.lista_canales.insert(tk.END, f"{es_privado} #{nombre}")
            
            messagebox.showinfo("Canales", f"Se encontraron {len(canales)} canales")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener canales: {str(e)}")
    
    def obtener_canal_seleccionado(self) -> Optional[str]:
        """Obtiene el canal seleccionado"""
        seleccion = self.lista_canales.curselection()
        if seleccion:
            canal_text = self.lista_canales.get(seleccion[0])
            # Extraer nombre del canal (quitar emoji y #)
            nombre = canal_text.split('#')[1] if '#' in canal_text else canal_text
            return nombre
        return None
    
    def enviar_mensaje_prueba(self, mensaje: str = "🧪 Mensaje de prueba desde Generador QA"):
        """Envía un mensaje de prueba"""
        if not self.slack_service:
            messagebox.showwarning("Advertencia", "Primero debes configurar Slack")
            return
        
        canal = self.obtener_canal_seleccionado()
        if not canal:
            messagebox.showwarning("Advertencia", "Selecciona un canal")
            return
        
        try:
            if self.slack_service.enviar_notificacion(mensaje, canal):
                messagebox.showinfo("Éxito", f"Mensaje enviado al canal #{canal}")
            else:
                messagebox.showerror("Error", "No se pudo enviar el mensaje")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar mensaje: {str(e)}")
    
    def get_slack_service(self) -> Optional[SlackNotificationService]:
        """Obtiene el servicio de Slack configurado"""
        return self.slack_service 