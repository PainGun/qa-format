import tkinter as tk
from typing import List, Any

def validar_campo_no_vacio(valor: str) -> bool:
    """Valida que un campo no esté vacío"""
    return valor is not None and valor.strip() != ""

def validar_campos_requeridos(campos: List[str]) -> bool:
    """Valida que todos los campos requeridos estén completos"""
    return all(validar_campo_no_vacio(campo) for campo in campos)

def limpiar_entry(entry: tk.Entry):
    """Limpia un campo de entrada"""
    entry.delete(0, tk.END)

def limpiar_text(text: tk.Text):
    """Limpia un área de texto"""
    text.delete("1.0", tk.END)

def obtener_texto_entry(entry: tk.Entry) -> str:
    """Obtiene el texto de un campo de entrada"""
    return entry.get().strip()

def obtener_texto_text(text: tk.Text) -> str:
    """Obtiene el texto de un área de texto"""
    return text.get("1.0", tk.END).strip()

def formatear_lista_items(items: List[Any]) -> str:
    """Formatea una lista de elementos con viñetas"""
    if not items:
        return "- Sin elementos"
    return "\n".join(f"- {item}" for item in items)

def formatear_comentario_qa(tipo: str, link: str, ambiente: str, instruccion: str) -> str:
    """Formatea un comentario de QA"""
    return f"Para {tipo} (Ambiente: {ambiente}):\nPrueba en {link}\nInstrucción:\n{instruccion}"

def formatear_ambiente_pr(ambiente: str, pr: str) -> str:
    """Formatea un ambiente y PR"""
    return f"Ambiente: {ambiente} - PR: {pr}"

def crear_tooltip(widget: tk.Widget, texto: str):
    """Crea un tooltip para un widget"""
    def mostrar_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(tooltip, text=texto, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack()
        
        def ocultar_tooltip(event):
            tooltip.destroy()
        
        widget.bind('<Leave>', ocultar_tooltip)
        tooltip.bind('<Leave>', ocultar_tooltip)
    
    widget.bind('<Enter>', mostrar_tooltip) 