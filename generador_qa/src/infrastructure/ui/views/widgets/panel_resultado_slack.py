"""
Panel de resultado mejorado con integración de Slack
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from ....external.slack_notification_service import SlackNotificationService
from ....external.slack_client import SlackClient
from generador_qa.src.infrastructure.ui.views.widgets.slack_config_widget import SlackConfigWidget
import datetime
from generador_qa.src.shared.utils import db


class PanelResultadoSlack(tk.Frame):
    """Panel para mostrar el resultado y enviar a Slack"""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.slack_service = None
        self.tarea_actual = None
        self.canal_seleccionado = None  # <-- Añadido para evitar errores
        self.canal_seleccionado_tipo = None  # <-- Añadido para evitar errores
        self.historial_envios = []  # <-- Historial de envíos
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pestaña de resultado
        self.setup_tab_resultado()
        
        # Pestaña de configuración de Slack
        self.setup_tab_slack()
        
        # Pestaña de envío
        self.setup_tab_envio()
        self.setup_tab_historial()  # <-- Nueva pestaña
    
    def setup_tab_resultado(self):
        """Configura la pestaña de resultado"""
        frame_resultado = tk.Frame(self.notebook)
        self.notebook.add(frame_resultado, text="📋 Resultado")
        
        # Botones de acción
        frame_botones = tk.Frame(frame_resultado)
        frame_botones.pack(fill=tk.X, pady=5)
        
        self.btn_generar = tk.Button(frame_botones, text="🔄 Generar", 
                                   command=self.generar_texto)
        self.btn_generar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_copiar = tk.Button(frame_botones, text="📋 Copiar", 
                                  command=self.copiar_texto)
        self.btn_copiar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_enviar_slack = tk.Button(frame_botones, text="📤 Enviar a Slack", 
                                        command=self.mostrar_dialogo_envio,
                                        state=tk.DISABLED)
        self.btn_enviar_slack.pack(side=tk.LEFT)
        
        # Área de resultado
        self.resultado_text = tk.Text(frame_resultado, height=15, width=100, bg="#f0f0f0")
        self.resultado_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def setup_tab_slack(self):
        """Configura la pestaña de configuración de Slack"""
        frame_slack = tk.Frame(self.notebook)
        self.notebook.add(frame_slack, text="🔗 Slack")
        
        # Widget de configuración de Slack
        self.slack_config = SlackConfigWidget(frame_slack, on_slack_ready=self.on_slack_ready)
        self.slack_config.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_tab_envio(self):
        """Configura la pestaña de envío"""
        frame_envio = tk.Frame(self.notebook)
        self.notebook.add(frame_envio, text="📤 Envío")
        
        # Información del envío
        info_frame = tk.LabelFrame(frame_envio, text="📋 Información del Envío")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(info_frame, text="Estado de Slack:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.lbl_slack_status = tk.Label(info_frame, text="❌ No configurado", fg="red")
        self.lbl_slack_status.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(info_frame, text="Canal seleccionado:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.lbl_canal = tk.Label(info_frame, text="Ninguno")
        self.lbl_canal.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Botones de acción
        action_frame = tk.Frame(frame_envio)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_seleccionar_canal = tk.Button(action_frame, text="🎯 Seleccionar Canal", 
                                             command=self.seleccionar_canal)
        self.btn_seleccionar_canal.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_enviar_ahora = tk.Button(action_frame, text="📤 Enviar Ahora", 
                                        command=self.enviar_ahora,
                                        state=tk.DISABLED)
        self.btn_enviar_ahora.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_mensaje_prueba = tk.Button(action_frame, text="🧪 Mensaje de Prueba", 
                                          command=self.enviar_mensaje_prueba)
        self.btn_mensaje_prueba.pack(side=tk.LEFT)
    
    def setup_tab_historial(self):
        frame_historial = tk.Frame(self.notebook)
        self.notebook.add(frame_historial, text="🕓 Historial")
        self.historial_listbox = tk.Listbox(frame_historial, height=10)
        self.historial_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.historial_listbox.bind('<<ListboxSelect>>', self.mostrar_detalle_historial)
        self.detalle_text = tk.Text(frame_historial, height=6, state=tk.DISABLED)
        self.detalle_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        self.cargar_historial_desde_db()

    def cargar_historial_desde_db(self):
        self.historial_envios = db.get_historial_envios()
        self.historial_listbox.delete(0, tk.END)
        for envio in self.historial_envios:
            resumen = envio['mensaje'][:60].replace('\n', ' ') + ("..." if len(envio['mensaje']) > 60 else "")
            item = f"[{envio['fecha']}] → {envio['destino']} | {envio['estado']} | Remitente: @{envio['usuario']} | {resumen}"
            self.historial_listbox.insert(tk.END, item)

    def agregar_a_historial(self, fecha, destino, mensaje, estado):
        usuario = db.get_config('slack_user') or 'desconocido'
        resumen = mensaje[:60].replace('\n', ' ') + ("..." if len(mensaje) > 60 else "")
        item = f"[{fecha}] → {destino} | {estado} | Remitente: @{usuario} | {resumen}"
        self.historial_envios.append({
            "fecha": fecha,
            "destino": destino,
            "mensaje": mensaje,
            "estado": estado,
            "usuario": usuario
        })
        self.historial_listbox.insert(tk.END, item)
        db.save_historial_envio(fecha, destino, mensaje, estado, usuario)
    def mostrar_detalle_historial(self, event):
        seleccion = self.historial_listbox.curselection()
        if seleccion:
            idx = seleccion[0]
            envio = self.historial_envios[idx]
            detalle = f"Fecha: {envio['fecha']}\nDestino: {envio['destino']}\nEstado: {envio['estado']}\nRemitente: @{envio['usuario']}\n\nMensaje:\n{envio['mensaje']}"
            self.detalle_text.config(state=tk.NORMAL)
            self.detalle_text.delete("1.0", tk.END)
            self.detalle_text.insert(tk.END, detalle)
            self.detalle_text.config(state=tk.DISABLED)
    
    def on_slack_ready(self, slack_service: SlackNotificationService):
        """Callback cuando Slack está configurado y listo"""
        self.slack_service = slack_service
        self.lbl_slack_status.config(text="✅ Conectado", fg="green")
        self.btn_enviar_slack.config(state=tk.NORMAL)
        self.btn_enviar_ahora.config(state=tk.NORMAL)
        self.btn_mensaje_prueba.config(state=tk.NORMAL)
        
        # Obtener canales automáticamente
        self.obtener_canales()
    
    def obtener_canales(self):
        """Obtiene la lista de canales y usuarios disponibles"""
        if not self.slack_service:
            return
        try:
            canales = self.slack_service.obtener_canales_disponibles()  # canales
            # Obtener usuarios
            usuarios = []
            if hasattr(self.slack_service, 'obtener_usuarios_disponibles'):
                usuarios = self.slack_service.obtener_usuarios_disponibles()
            self.destinos_disponibles = []
            # Agregar canales
            for canal in canales:
                nombre = canal.get('name', 'Sin nombre')
                es_privado = canal.get('is_private', False)
                self.destinos_disponibles.append({
                    'tipo': 'canal',
                    'id': canal.get('id'),
                    'name': nombre,
                    'emoji': '🔒' if es_privado else '🌐',
                    'is_private': es_privado
                })
            # Agregar usuarios
            for usuario in usuarios:
                nombre = usuario.get('real_name', usuario.get('name', 'Sin nombre'))
                self.destinos_disponibles.append({
                    'tipo': 'usuario',
                    'id': usuario.get('id'),
                    'name': nombre,
                    'emoji': '👤',
                    'is_private': False
                })
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener canales/usuarios: {str(e)}")

    def seleccionar_canal(self):
        """Muestra un diálogo para seleccionar canal o usuario"""
        if not self.slack_service:
            messagebox.showwarning("Advertencia", "Primero debes configurar Slack")
            return
        if not hasattr(self, 'destinos_disponibles') or not self.destinos_disponibles:
            self.obtener_canales()
            if not hasattr(self, 'destinos_disponibles') or not self.destinos_disponibles:
                messagebox.showwarning("Advertencia", "No se pudieron obtener los canales/usuarios")
                return
        dialog = tk.Toplevel(self)
        dialog.title("Seleccionar Destino de Slack")
        dialog.geometry("400x400")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        main_frame = tk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(main_frame, text="Selecciona un canal o usuario:").pack(anchor="w", pady=(0, 5))
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        # Llenar lista
        for destino in self.destinos_disponibles:
            if destino['tipo'] == 'canal':
                listbox.insert(tk.END, f"{destino['emoji']} #{destino['name']}")
            else:
                listbox.insert(tk.END, f"{destino['emoji']} {destino['name']}")
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        def seleccionar():
            seleccion = listbox.curselection()
            if seleccion:
                destino = self.destinos_disponibles[seleccion[0]]
                self.canal_seleccionado = destino['id']
                self.canal_seleccionado_tipo = destino['tipo']
                self.lbl_canal.config(text=(f"#{destino['name']}" if destino['tipo']=='canal' else destino['name']))
                dialog.destroy()
                messagebox.showinfo("Destino Seleccionado", f"Destino seleccionado: {destino['emoji']} {destino['name']}")
            else:
                messagebox.showwarning("Selección", "Por favor selecciona un canal o usuario")
        def cancelar():
            dialog.destroy()
        tk.Button(button_frame, text="✅ Seleccionar", command=seleccionar).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="❌ Cancelar", command=cancelar).pack(side=tk.LEFT)
    
    def mostrar_dialogo_envio(self):
        """Muestra un diálogo para editar y confirmar el envío"""
        if not self.slack_service:
            messagebox.showwarning("Configuración", "Primero debes configurar Slack en la pestaña 'Slack'")
            self.notebook.select(1)  # Cambiar a pestaña de Slack
            return
        if not self.canal_seleccionado:
            messagebox.showinfo("Destino", "Selecciona un canal o usuario de destino")
            self.notebook.select(2)  # Cambiar a pestaña de envío
            return
        if not self.tarea_actual:
            messagebox.showwarning("Datos", "No hay datos para enviar. Genera el reporte primero.")
            return
        mensaje_default = self.resultado_text.get("1.0", tk.END).strip()
        dialog = tk.Toplevel(self)
        dialog.title("Editar y Enviar a Slack")
        dialog.geometry("600x400")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        destino_str = self.canal_seleccionado if self.canal_seleccionado_tipo == 'usuario' else f"#{self.canal_seleccionado}"
        tk.Label(dialog, text=f"Destino: {destino_str}", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Label(dialog, text="Edita el mensaje antes de enviarlo:").pack(anchor="w", padx=10, pady=(5, 0))
        text_frame = tk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget = tk.Text(text_frame, height=15, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, mensaje_default)
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        def enviar():
            mensaje_editado = text_widget.get("1.0", tk.END).strip()
            if not mensaje_editado:
                messagebox.showwarning("Mensaje vacío", "El mensaje no puede estar vacío.")
                return
            if not self.canal_seleccionado:
                messagebox.showwarning("Destino", "Selecciona un canal o usuario antes de enviar.")
                return
            if not self.slack_service:
                messagebox.showerror("Error", "Slack no está configurado.")
                return
            try:
                # Buscar user_id si es usuario
                remitente = None
                if self.canal_seleccionado_tipo == 'usuario':
                    for d in getattr(self, 'destinos_disponibles', []):
                        if d['tipo'] == 'usuario' and d['id'] == self.canal_seleccionado:
                            remitente = f"<@{d['id']}>"
                            break
                else:
                    usuario = db.get_config('slack_user') or ''
                    remitente = f"@{usuario}" if usuario else ''
                mensaje_final = f"Remitente: {remitente}\n\n{mensaje_editado}" if remitente else mensaje_editado
                resultado = self.slack_service.enviar_notificacion(mensaje_final, self.canal_seleccionado)
                destino_str = self.canal_seleccionado if self.canal_seleccionado_tipo == 'usuario' else f"#{self.canal_seleccionado}"
                estado = "Éxito" if resultado else "Error"
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self.agregar_a_historial(fecha, destino_str, mensaje_final, estado)
                if resultado:
                    messagebox.showinfo("Éxito", f"✅ Mensaje enviado exitosamente a {destino_str}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "❌ No se pudo enviar el mensaje")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al enviar mensaje: {str(e)}")
        def cancelar():
            dialog.destroy()
        tk.Button(button_frame, text="📤 Enviar", command=enviar).pack(side=tk.LEFT, padx=(10, 10))
        tk.Button(button_frame, text="❌ Cancelar", command=cancelar).pack(side=tk.LEFT)
    
    def enviar_ahora(self):
        """Envía el reporte actual a Slack"""
        if not self.slack_service or not self.canal_seleccionado:
            messagebox.showwarning("Destino", "Selecciona un canal o usuario antes de enviar.")
            return
        if not self.tarea_actual:
            messagebox.showwarning("Datos", "No hay datos para enviar. Genera el reporte primero.")
            return
        if not self.slack_service:
            messagebox.showerror("Error", "Slack no está configurado.")
            return
        try:
            # Buscar user_id si es usuario
            remitente = None
            if self.canal_seleccionado_tipo == 'usuario':
                for d in getattr(self, 'destinos_disponibles', []):
                    if d['tipo'] == 'usuario' and d['id'] == self.canal_seleccionado:
                        remitente = f"<@{d['id']}>"
                        break
            else:
                usuario = db.get_config('slack_user') or ''
                remitente = f"@{usuario}" if usuario else ''
            mensaje = self.resultado_text.get("1.0", tk.END).strip()
            mensaje_final = f"Remitente: {remitente}\n\n{mensaje}" if remitente else mensaje
            resultado = self.slack_service.enviar_reporte_qa(self.tarea_actual, self.canal_seleccionado)
            destino_str = self.canal_seleccionado if self.canal_seleccionado_tipo == 'usuario' else f"#{self.canal_seleccionado}"
            estado = "Éxito" if resultado else "Error"
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.agregar_a_historial(fecha, destino_str, mensaje_final, estado)
            if resultado:
                messagebox.showinfo("Éxito", f"✅ Reporte enviado exitosamente a {destino_str}")
            else:
                messagebox.showerror("Error", "❌ No se pudo enviar el reporte")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al enviar reporte: {str(e)}")

    def enviar_mensaje_prueba(self):
        """Envía un mensaje de prueba"""
        if not self.slack_service or not self.canal_seleccionado:
            messagebox.showwarning("Destino", "Selecciona un canal o usuario antes de enviar.")
            return
        if not self.slack_service:
            messagebox.showerror("Error", "Slack no está configurado.")
            return
        try:
            # Buscar user_id si es usuario
            remitente = None
            if self.canal_seleccionado_tipo == 'usuario':
                for d in getattr(self, 'destinos_disponibles', []):
                    if d['tipo'] == 'usuario' and d['id'] == self.canal_seleccionado:
                        remitente = f"<@{d['id']}>"
                        break
            else:
                usuario = db.get_config('slack_user') or ''
                remitente = f"@{usuario}" if usuario else ''
            mensaje = "🧪 Mensaje de prueba desde Generador QA - ¡La integración funciona perfectamente!"
            mensaje_final = f"Remitente: {remitente}\n\n{mensaje}" if remitente else mensaje
            resultado = self.slack_service.enviar_notificacion(mensaje_final, self.canal_seleccionado)
            destino_str = self.canal_seleccionado if self.canal_seleccionado_tipo == 'usuario' else f"#{self.canal_seleccionado}"
            estado = "Éxito" if resultado else "Error"
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.agregar_a_historial(fecha, destino_str, mensaje_final, estado)
            if resultado:
                messagebox.showinfo("Éxito", f"✅ Mensaje de prueba enviado a {destino_str}")
            else:
                messagebox.showerror("Error", "❌ No se pudo enviar el mensaje de prueba")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al enviar mensaje de prueba: {str(e)}")
    
    def generar_texto(self):
        """Genera el texto de la tarea"""
        texto = self.controller.generar_texto()
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert(tk.END, texto)
        
        # Guardar la tarea actual para envío
        self.tarea_actual = self.controller.tarea
        
        # Habilitar botón de envío si Slack está configurado
        if self.slack_service:
            self.btn_enviar_slack.config(state=tk.NORMAL)
    
    def copiar_texto(self):
        """Copia el texto al portapapeles"""
        texto = self.resultado_text.get("1.0", tk.END)
        self.controller.copiar_al_portapapeles(texto) 