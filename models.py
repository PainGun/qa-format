from dataclasses import dataclass
from typing import List

@dataclass
class AmbientePR:
    """Modelo para representar un ambiente y su PR asociado"""
    ambiente: str
    pr: str
    
    def __str__(self):
        return f"Ambiente: {self.ambiente} - PR: {self.pr}"

@dataclass
class ComentarioQA:
    """Modelo para representar un comentario de QA"""
    tipo: str
    link: str
    ambiente: str
    instruccion: str
    
    def __str__(self):
        return f"Para {self.tipo} (Ambiente: {self.ambiente}):\nPrueba en {self.link}\nInstrucción:\n{self.instruccion}"

@dataclass
class TareaQA:
    """Modelo principal que contiene toda la información de la tarea"""
    titulo: str = ""
    jira: str = ""
    ambientes_prs: List[AmbientePR] = None
    comentarios: List[ComentarioQA] = None
    qa_usabilidad: List[str] = None
    qa_codigo: List[str] = None
    
    def __post_init__(self):
        if self.ambientes_prs is None:
            self.ambientes_prs = []
        if self.comentarios is None:
            self.comentarios = []
        if self.qa_usabilidad is None:
            self.qa_usabilidad = []
        if self.qa_codigo is None:
            self.qa_codigo = []
    
    def generar_texto(self) -> str:
        """Genera el texto formateado para la tarea"""
        ambientes_prs_text = "\n".join(f"- {item}" for item in self.ambientes_prs)
        comentarios_text = "\n\n".join(str(comentario) for comentario in self.comentarios)
        qa_usu_text = "\n".join(f"- {item}" for item in self.qa_usabilidad)
        qa_cod_text = "\n".join(f"- {item}" for item in self.qa_codigo)
        
        return f"""*Tarea:* {self.titulo}
*Jira:* {self.jira}

*Ambientes + PRs:*
{ambientes_prs_text if ambientes_prs_text else '- Sin registros agregados'}

*Comentarios:*
{comentarios_text if comentarios_text else '- Sin comentarios agregados'}

*Responsables:*
*QA Usabilidad:*
{qa_usu_text if qa_usu_text else '- Ninguno'}
*QA Código:*
{qa_cod_text if qa_cod_text else '- Ninguno'}
""" 