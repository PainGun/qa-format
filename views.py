import tkinter as tk
from tkinter import ttk
from typing import Callable

class ListaConEliminacion(tk.Frame):
    """Widget personalizado que combina una lista con botón de eliminación"""
    
    def __init__(self, parent, width=60, height=4, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.lista = tk.Listbox(self, width=width, height=height)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.btn_eliminar = tk.Button(self, text="❌", command=self.eliminar_seleccionado)
        self.btn_eliminar.pack(side=tk.RIGHT, padx=(5, 0))
    
    def eliminar_seleccionado(self):
        """Elimina el elemento seleccionado de la lista"""
        seleccion = self.lista.curselection()
        if seleccion:
            self.lista.delete(seleccion[0])
    
    def insertar(self, item):
        """Inserta un elemento en la lista"""
        self.lista.insert(tk.END, item)
    
    def obtener_todos(self):
        """Obtiene todos los elementos de la lista"""
        return list(self.lista.get(0, tk.END))
    
    def limpiar(self):
        """Limpia toda la lista"""
        self.lista.delete(0, tk.END)
    
    def actualizar_lista(self, items):
        """Actualiza la lista con nuevos elementos"""
        self.limpiar()
        for item in items:
            self.insertar(str(item))

class SeccionAmbientesPRs(tk.LabelFrame):
    """Sección para manejar ambientes y PRs"""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, text="Ambientes + PRs", **kwargs)
        self.controller = controller
        
        # Campos de entrada
        frame_entrada = tk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Ambiente:").grid(row=0, column=0, sticky="e", padx=(0, 5))
        self.entry_ambiente = tk.Entry(frame_entrada, width=30)
        self.entry_ambiente.grid(row=0, column=1, sticky="w", padx=(0, 10))
        
        tk.Label(frame_entrada, text="PR:").grid(row=1, column=0, sticky="e", padx=(0, 5))
        self.entry_pr = tk.Entry(frame_entrada, width=30)
        self.entry_pr.grid(row=1, column=1, sticky="w", padx=(0, 10))
        
        self.btn_agregar = tk.Button(frame_entrada, text="Agregar Ambiente + PR", 
                                   command=self.agregar_ambiente_pr)
        self.btn_agregar.grid(row=1, column=2, padx=(10, 0))
        
        # Lista
        self.lista = ListaConEliminacion(self, width=80, height=4)
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def agregar_ambiente_pr(self):
        """Agrega un ambiente y PR"""
        ambiente = self.entry_ambiente.get()
        pr = self.entry_pr.get()
        
        if self.controller.agregar_ambiente_pr(ambiente, pr):
            self.lista.insertar(f"Ambiente: {ambiente} - PR: {pr}")
            self.entry_ambiente.delete(0, tk.END)
            self.entry_pr.delete(0, tk.END)
    
    def actualizar_lista(self):
        """Actualiza la lista con los datos del controlador"""
        items = [str(item) for item in self.controller.tarea.ambientes_prs]
        self.lista.actualizar_lista(items)

class SeccionComentarios(tk.LabelFrame):
    """Sección para manejar comentarios de QA"""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, text="Comentarios de QA", **kwargs)
        self.controller = controller
        
        # Campos de entrada
        frame_entrada = tk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Tipo QA:").grid(row=0, column=0, sticky="e", padx=(0, 5))
        self.entry_tipo = tk.Entry(frame_entrada, width=40)
        self.entry_tipo.grid(row=0, column=1, sticky="w", padx=(0, 10))
        
        tk.Label(frame_entrada, text="Link:").grid(row=1, column=0, sticky="e", padx=(0, 5))
        self.entry_link = tk.Entry(frame_entrada, width=40)
        self.entry_link.grid(row=1, column=1, sticky="w", padx=(0, 10))
        
        tk.Label(frame_entrada, text="Ambiente:").grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.entry_ambiente = tk.Entry(frame_entrada, width=40)
        self.entry_ambiente.grid(row=2, column=1, sticky="w", padx=(0, 10))
        
        tk.Label(frame_entrada, text="Instrucción:").grid(row=3, column=0, sticky="ne", padx=(0, 5))
        self.txt_instruccion = tk.Text(frame_entrada, width=40, height=4)
        self.txt_instruccion.grid(row=3, column=1, sticky="w", padx=(0, 10))
        
        self.btn_agregar = tk.Button(frame_entrada, text="Agregar Comentario", 
                                   command=self.agregar_comentario)
        self.btn_agregar.grid(row=3, column=2, padx=(10, 0), pady=(0, 5))
        
        # Lista
        self.lista = ListaConEliminacion(self, width=60, height=4)
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def agregar_comentario(self):
        """Agrega un comentario de QA"""
        tipo = self.entry_tipo.get()
        link = self.entry_link.get()
        ambiente = self.entry_ambiente.get()
        instruccion = self.txt_instruccion.get("1.0", tk.END)
        
        if self.controller.agregar_comentario(tipo, link, ambiente, instruccion):
            comentario = f"Para {tipo} (Ambiente: {ambiente}):\nPrueba en {link}\nInstrucción:\n{instruccion}"
            self.lista.insertar(comentario)
            self.limpiar_campos()
    
    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self.entry_tipo.delete(0, tk.END)
        self.entry_link.delete(0, tk.END)
        self.entry_ambiente.delete(0, tk.END)
        self.txt_instruccion.delete("1.0", tk.END)
    
    def actualizar_lista(self):
        """Actualiza la lista con los datos del controlador"""
        items = [str(item) for item in self.controller.tarea.comentarios]
        self.lista.actualizar_lista(items)

class SeccionQA(tk.LabelFrame):
    """Sección para manejar QAs de usabilidad y código"""
    
    def __init__(self, parent, controller, tipo_qa, **kwargs):
        super().__init__(parent, text=f"QA {tipo_qa.title()}", **kwargs)
        self.controller = controller
        self.tipo_qa = tipo_qa
        
        # Campo de entrada y botón
        frame_entrada = tk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        self.entry_qa = tk.Entry(frame_entrada, width=45)
        self.entry_qa.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.btn_agregar = tk.Button(frame_entrada, text="Agregar", 
                                   command=self.agregar_qa)
        self.btn_agregar.pack(side=tk.RIGHT)
        
        # Lista
        self.lista = ListaConEliminacion(self, width=60, height=2)
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def agregar_qa(self):
        """Agrega un QA"""
        qa = self.entry_qa.get()
        
        if self.tipo_qa == "usabilidad":
            if self.controller.agregar_qa_usabilidad(qa):
                self.lista.insertar(qa)
                self.entry_qa.delete(0, tk.END)
        else:  # código
            if self.controller.agregar_qa_codigo(qa):
                self.lista.insertar(qa)
                self.entry_qa.delete(0, tk.END)
    
    def actualizar_lista(self):
        """Actualiza la lista con los datos del controlador"""
        if self.tipo_qa == "usabilidad":
            items = self.controller.tarea.qa_usabilidad
        else:
            items = self.controller.tarea.qa_codigo
        self.lista.actualizar_lista(items)

class PanelResultado(tk.Frame):
    """Panel para mostrar el resultado generado"""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        
        # Botones
        frame_botones = tk.Frame(self)
        frame_botones.pack(fill=tk.X, pady=5)
        
        self.btn_generar = tk.Button(frame_botones, text="Generar", 
                                   command=self.generar_texto)
        self.btn_generar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_copiar = tk.Button(frame_botones, text="Copiar", 
                                  command=self.copiar_texto)
        self.btn_copiar.pack(side=tk.LEFT)
        
        # Área de resultado
        self.resultado_text = tk.Text(self, height=15, width=100, bg="#f0f0f0")
        self.resultado_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def generar_texto(self):
        """Genera el texto de la tarea"""
        texto = self.controller.generar_texto()
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert(tk.END, texto)
    
    def copiar_texto(self):
        """Copia el texto al portapapeles"""
        texto = self.resultado_text.get("1.0", tk.END)
        self.controller.copiar_al_portapapeles(texto) 