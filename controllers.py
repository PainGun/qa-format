from models import TareaQA, AmbientePR, ComentarioQA
from PyQt6.QtWidgets import QApplication

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
    
    def copiar_al_portapapeles(self, texto: str) -> bool:
        """Copia texto al portapapeles usando PyQt6"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(texto)
            return True
        except Exception as e:
            print(f"Error al copiar al portapapeles: {e}")
            return False
    
    def limpiar_datos(self):
        """Limpia todos los datos de la tarea"""
        self.tarea = TareaQA() 
    
    def formatear_ambiente_pr_para_ui(self, ambiente: str, pr: str) -> str:
        """Formatea ambiente y PR para mostrar en la UI"""
        return f"Ambiente: {ambiente} - PR: {pr}"
    
    def formatear_comentario_para_ui(self, tipo: str, link: str, ambiente: str, instruccion: str) -> str:
        """Formatea comentario para mostrar en la UI"""
        return f"Para {tipo} (Ambiente: {ambiente}):\nPrueba en {link}\nInstrucción:\n{instruccion}"
    
    def obtener_ambiente_pr_por_indice(self, index: int) -> str:
        """Obtiene el ambiente y PR formateado por índice para la UI"""
        if 0 <= index < len(self.tarea.ambientes_prs):
            item = self.tarea.ambientes_prs[index]
            return self.formatear_ambiente_pr_para_ui(item.ambiente, item.pr)
        return ""
    
    def obtener_comentario_por_indice(self, index: int) -> str:
        """Obtiene el comentario formateado por índice para la UI"""
        if 0 <= index < len(self.tarea.comentarios):
            comentario = self.tarea.comentarios[index]
            return self.formatear_comentario_para_ui(
                comentario.tipo, comentario.link, 
                comentario.ambiente, comentario.instruccion
            )
        return ""
    
    def obtener_todas_las_listas_para_ui(self):
        """Obtiene todas las listas formateadas para sincronizar con la UI"""
        return {
            'ambientes_prs': [self.formatear_ambiente_pr_para_ui(item.ambiente, item.pr) 
                             for item in self.tarea.ambientes_prs],
            'comentarios': [self.formatear_comentario_para_ui(
                            item.tipo, item.link, item.ambiente, item.instruccion)
                           for item in self.tarea.comentarios],
            'qa_usabilidad': self.tarea.qa_usabilidad.copy(),
            'qa_codigo': self.tarea.qa_codigo.copy()
        }