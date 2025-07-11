import tkinter as tk
from tkinter import ttk
from controllers import TareaQAController
from views import SeccionAmbientesPRs, SeccionComentarios, SeccionQA, PanelResultado

class GeneradorQAApp:
    """Aplicación principal del Generador de QA"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.controller = TareaQAController()
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title("Generador Paso a QA")
        self.root.geometry("1200x900")
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Sección de información básica
        self.setup_info_basica()
        
        # Sección de ambientes y PRs
        self.seccion_ambientes = SeccionAmbientesPRs(self.root, self.controller)
        self.seccion_ambientes.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Sección de comentarios
        self.seccion_comentarios = SeccionComentarios(self.root, self.controller)
        self.seccion_comentarios.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Secciones de QA
        self.setup_secciones_qa()
        
        # Panel de resultado
        self.panel_resultado = PanelResultado(self.root, self.controller)
        self.panel_resultado.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    def setup_info_basica(self):
        """Configura la sección de información básica"""
        frame_info = tk.LabelFrame(self.root, text="Información Básica")
        frame_info.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Título de la tarea
        tk.Label(frame_info, text="Título de la Tarea:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_titulo = tk.Entry(frame_info, width=60)
        self.entry_titulo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Link de Jira
        tk.Label(frame_info, text="Link Jira:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_jira = tk.Entry(frame_info, width=60)
        self.entry_jira.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    def setup_secciones_qa(self):
        """Configura las secciones de QA"""
        frame_qa = tk.Frame(self.root)
        frame_qa.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        frame_qa.grid_columnconfigure(0, weight=1)
        frame_qa.grid_columnconfigure(1, weight=1)
        
        # QA Usabilidad
        self.seccion_qa_usu = SeccionQA(frame_qa, self.controller, "usabilidad")
        self.seccion_qa_usu.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # QA Código
        self.seccion_qa_cod = SeccionQA(frame_qa, self.controller, "código")
        self.seccion_qa_cod.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def setup_bindings(self):
        """Configura los enlaces de eventos"""
        # Actualizar datos del controlador cuando cambien los campos básicos
        self.entry_titulo.bind('<KeyRelease>', self.on_titulo_change)
        self.entry_jira.bind('<KeyRelease>', self.on_jira_change)
        
        # Actualizar listas cuando se genere texto
        self.panel_resultado.btn_generar.config(command=self.generar_y_actualizar)
    
    def on_titulo_change(self, event=None):
        """Maneja cambios en el título"""
        self.controller.actualizar_titulo(self.entry_titulo.get())
    
    def on_jira_change(self, event=None):
        """Maneja cambios en el link de Jira"""
        self.controller.actualizar_jira(self.entry_jira.get())
    
    def generar_y_actualizar(self):
        """Genera el texto y actualiza las listas"""
        # Actualizar listas con datos del controlador
        self.seccion_ambientes.actualizar_lista()
        self.seccion_comentarios.actualizar_lista()
        self.seccion_qa_usu.actualizar_lista()
        self.seccion_qa_cod.actualizar_lista()
        
        # Generar texto
        self.panel_resultado.generar_texto()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = GeneradorQAApp()
    app.run()

if __name__ == "__main__":
    main() 