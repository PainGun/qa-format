"""
Ventana principal con integración de Slack
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ...controllers.main_controller import TareaQAController
from .secciones.info_basica import SeccionInfoBasica
from .secciones.ambientes_prs import SeccionAmbientesPRs
from .secciones.comentarios import SeccionComentarios
from .secciones.responsables import SeccionResponsables
from .widgets.panel_resultado_slack import PanelResultadoSlack


class GeneradorQAMainWindow:
    """Ventana principal del Generador QA con integración de Slack"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.controller = TareaQAController()
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title("Generador QA - Con Integración Slack")
        self.root.geometry("1400x1000")
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Frame principal con scroll
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Configurar scroll con mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar secciones
        self.setup_secciones()
        
        # Configurar panel de resultado con Slack
        self.setup_panel_resultado()
        
        # Configurar barra de estado
        self.setup_status_bar()
    
    def setup_secciones(self):
        """Configura las secciones de la aplicación"""
        # Sección de información básica
        self.seccion_info = SeccionInfoBasica(self.scrollable_frame, self.controller)
        self.seccion_info.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Sección de ambientes y PRs
        self.seccion_ambientes = SeccionAmbientesPRs(self.scrollable_frame, self.controller)
        self.seccion_ambientes.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Sección de comentarios
        self.seccion_comentarios = SeccionComentarios(self.scrollable_frame, self.controller)
        self.seccion_comentarios.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Secciones de responsables
        self.setup_secciones_responsables()
    
    def setup_secciones_responsables(self):
        """Configura las secciones de responsables"""
        frame_qa = tk.Frame(self.scrollable_frame)
        frame_qa.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_qa.grid_columnconfigure(0, weight=1)
        frame_qa.grid_columnconfigure(1, weight=1)
        
        # QA Usabilidad
        self.seccion_qa_usu = SeccionResponsables(frame_qa, self.controller, "usabilidad")
        self.seccion_qa_usu.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # QA Código
        self.seccion_qa_cod = SeccionResponsables(frame_qa, self.controller, "código")
        self.seccion_qa_cod.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def setup_panel_resultado(self):
        """Configura el panel de resultado con Slack"""
        # Frame para el panel de resultado
        resultado_frame = tk.Frame(self.scrollable_frame)
        resultado_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        resultado_frame.grid_columnconfigure(0, weight=1)
        
        # Panel de resultado con Slack
        self.panel_resultado = PanelResultadoSlack(resultado_frame, self.controller)
        self.panel_resultado.grid(row=0, column=0, sticky="ew")
    
    def setup_status_bar(self):
        """Configura la barra de estado"""
        self.status_bar = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.lbl_status = tk.Label(self.status_bar, text="Listo", anchor="w")
        self.lbl_status.pack(side=tk.LEFT, padx=5)
        
        self.lbl_slack_status = tk.Label(self.status_bar, text="Slack: ❌ No configurado", fg="red")
        self.lbl_slack_status.pack(side=tk.RIGHT, padx=5)
    
    def setup_bindings(self):
        """Configura los enlaces de eventos"""
        # Actualizar datos del controlador cuando cambien los campos básicos
        self.seccion_info.bind_changes(self.on_data_change)
        
        # Actualizar listas cuando se genere texto
        self.panel_resultado.btn_generar.config(command=self.generar_y_actualizar)
        
        # Configurar eventos de teclado
        self.root.bind('<Control-g>', lambda e: self.generar_y_actualizar())
        self.root.bind('<Control-s>', lambda e: self.enviar_a_slack())
        self.root.bind('<Control-c>', lambda e: self.copiar_texto())
        
        # Configurar menú
        self.setup_menu()
    
    def setup_menu(self):
        """Configura el menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.nuevo_proyecto)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Generar Reporte", command=self.generar_y_actualizar, accelerator="Ctrl+G")
        edit_menu.add_command(label="Copiar", command=self.copiar_texto, accelerator="Ctrl+C")
        
        # Menú Slack
        slack_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Slack", menu=slack_menu)
        slack_menu.add_command(label="Configurar Slack", command=self.configurar_slack)
        slack_menu.add_command(label="Enviar a Slack", command=self.enviar_a_slack, accelerator="Ctrl+S")
        slack_menu.add_command(label="Mensaje de Prueba", command=self.mensaje_prueba)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.acerca_de)
        help_menu.add_command(label="Documentación Slack", command=self.abrir_docs_slack)
    
    def _on_mousewheel(self, event):
        """Maneja el scroll del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_data_change(self):
        """Maneja cambios en los datos"""
        self.actualizar_status("Datos actualizados")
    
    def generar_y_actualizar(self):
        """Genera el texto y actualiza las listas"""
        try:
            # Actualizar listas con datos del controlador
            self.seccion_ambientes.actualizar_lista()
            self.seccion_comentarios.actualizar_lista()
            self.seccion_qa_usu.actualizar_lista()
            self.seccion_qa_cod.actualizar_lista()
            
            # Generar texto
            self.panel_resultado.generar_texto()
            
            self.actualizar_status("Reporte generado exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            self.actualizar_status("Error al generar reporte")
    
    def enviar_a_slack(self):
        """Envía el reporte a Slack"""
        self.panel_resultado.mostrar_dialogo_envio()
    
    def copiar_texto(self):
        """Copia el texto al portapapeles"""
        self.panel_resultado.copiar_texto()
        self.actualizar_status("Texto copiado al portapapeles")
    
    def configurar_slack(self):
        """Abre la configuración de Slack"""
        self.panel_resultado.notebook.select(1)  # Cambiar a pestaña de Slack
    
    def mensaje_prueba(self):
        """Envía un mensaje de prueba a Slack"""
        self.panel_resultado.enviar_mensaje_prueba()
    
    def nuevo_proyecto(self):
        """Crea un nuevo proyecto"""
        respuesta = messagebox.askyesno("Nuevo Proyecto", "¿Deseas crear un nuevo proyecto? Se perderán los datos actuales.")
        if respuesta:
            self.controller.limpiar_datos()
            self.actualizar_ui()
            self.actualizar_status("Nuevo proyecto creado")
    
    def actualizar_ui(self):
        """Actualiza toda la interfaz de usuario"""
        # Limpiar campos
        self.seccion_info.limpiar_campos()
        
        # Limpiar listas
        self.seccion_ambientes.limpiar_lista()
        self.seccion_comentarios.limpiar_lista()
        self.seccion_qa_usu.limpiar_lista()
        self.seccion_qa_cod.limpiar_lista()
        
        # Limpiar resultado
        self.panel_resultado.resultado_text.delete("1.0", tk.END)
    
    def actualizar_status(self, mensaje: str):
        """Actualiza la barra de estado"""
        self.lbl_status.config(text=mensaje)
        self.root.after(3000, lambda: self.lbl_status.config(text="Listo"))
    
    def actualizar_slack_status(self, conectado: bool):
        """Actualiza el estado de Slack en la barra de estado"""
        if conectado:
            self.lbl_slack_status.config(text="Slack: ✅ Conectado", fg="green")
        else:
            self.lbl_slack_status.config(text="Slack: ❌ No configurado", fg="red")
    
    def acerca_de(self):
        """Muestra información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de Generador QA",
            "Generador QA v1.0.0\n\n"
            "Aplicación para generar reportes de QA\n"
            "con integración de Slack\n\n"
            "Desarrollado con Clean Architecture\n"
            "Python + Tkinter + Slack API"
        )
    
    def abrir_docs_slack(self):
        """Abre la documentación de Slack"""
        messagebox.showinfo(
            "Documentación Slack",
            "Para configurar Slack:\n\n"
            "1. Ve a api.slack.com/apps\n"
            "2. Crea una nueva app\n"
            "3. Configura los permisos necesarios\n"
            "4. Instala la app en tu workspace\n"
            "5. Copia el token de bot\n\n"
            "Consulta docs/SLACK_INTEGRATION.md para más detalles."
        )
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop() 