from models import TareaQA, AmbientePR, ComentarioQA
import tkinter as tk
from tkinter import messagebox

class TareaQAController:
    """Controlador principal para manejar la lógica de negocio"""
    
    def __init__(self):
        self.tarea = TareaQA()
    
    def agregar_ambiente_pr(self, ambiente: str, pr: str) -> bool:
        """Agrega un ambiente y PR a la tarea"""
        if ambiente.strip() and pr.strip():
            self.tarea.ambientes_prs.append(AmbientePR(ambiente.strip(), pr.strip()))
            return True
        return False
    
    def eliminar_ambiente_pr(self, index: int) -> bool:
        """Elimina un ambiente y PR por índice"""
        if 0 <= index < len(self.tarea.ambientes_prs):
            del self.tarea.ambientes_prs[index]
            return True
        return False
    
    def agregar_comentario(self, tipo: str, link: str, ambiente: str, instruccion: str) -> bool:
        """Agrega un comentario de QA a la tarea"""
        if all([tipo.strip(), link.strip(), ambiente.strip(), instruccion.strip()]):
            self.tarea.comentarios.append(ComentarioQA(
                tipo.strip(), link.strip(), ambiente.strip(), instruccion.strip()
            ))
            return True
        return False
    
    def eliminar_comentario(self, index: int) -> bool:
        """Elimina un comentario por índice"""
        if 0 <= index < len(self.tarea.comentarios):
            del self.tarea.comentarios[index]
            return True
        return False
    
    def agregar_qa_usabilidad(self, qa: str) -> bool:
        """Agrega un QA de usabilidad"""
        if qa.strip():
            self.tarea.qa_usabilidad.append(qa.strip())
            return True
        return False
    
    def eliminar_qa_usabilidad(self, index: int) -> bool:
        """Elimina un QA de usabilidad por índice"""
        if 0 <= index < len(self.tarea.qa_usabilidad):
            del self.tarea.qa_usabilidad[index]
            return True
        return False
    
    def agregar_qa_codigo(self, qa: str) -> bool:
        """Agrega un QA de código"""
        if qa.strip():
            self.tarea.qa_codigo.append(qa.strip())
            return True
        return False
    
    def eliminar_qa_codigo(self, index: int) -> bool:
        """Elimina un QA de código por índice"""
        if 0 <= index < len(self.tarea.qa_codigo):
            del self.tarea.qa_codigo[index]
            return True
        return False
    
    def actualizar_titulo(self, titulo: str):
        """Actualiza el título de la tarea"""
        self.tarea.titulo = titulo
    
    def actualizar_jira(self, jira: str):
        """Actualiza el link de Jira"""
        self.tarea.jira = jira
    
    def generar_texto(self) -> str:
        """Genera el texto formateado de la tarea"""
        return self.tarea.generar_texto()
    
    def copiar_al_portapapeles(self, texto: str):
        """Copia texto al portapapeles"""
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana
            root.clipboard_clear()
            root.clipboard_append(texto)
            root.destroy()
            messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar al portapapeles: {e}")
    
    def limpiar_datos(self):
        """Limpia todos los datos de la tarea"""
        self.tarea = TareaQA() 