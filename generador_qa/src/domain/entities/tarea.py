"""
Entidad TareaQA del dominio
Implementa las reglas de negocio puras sin dependencias externas
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from ..value_objects.tipos_qa import TipoQA
from ...shared.exceptions.domain_exceptions import CampoRequeridoException, ValidacionException


@dataclass
class AmbientePR:
    """Objeto de valor para representar un ambiente y su PR"""
    ambiente: str
    pr: str
    
    def __post_init__(self):
        """Validar que los campos no estén vacíos"""
        if not self.ambiente.strip():
            raise CampoRequeridoException("El ambiente es requerido")
        if not self.pr.strip():
            raise CampoRequeridoException("El PR es requerido")
    
    def __str__(self) -> str:
        return f"Ambiente: {self.ambiente} - PR: {self.pr}"


@dataclass
class ComentarioQA:
    """Objeto de valor para representar un comentario de QA"""
    tipo: TipoQA
    link: str
    ambiente: str
    instruccion: str
    fecha_creacion: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validar que los campos requeridos no estén vacíos"""
        if not self.link.strip():
            raise CampoRequeridoException("El link es requerido")
        if not self.ambiente.strip():
            raise CampoRequeridoException("El ambiente es requerido")
        if not self.instruccion.strip():
            raise CampoRequeridoException("La instrucción es requerida")
    
    def __str__(self) -> str:
        return f"Para {self.tipo.value} (Ambiente: {self.ambiente}):\nPrueba en {self.link}\nInstrucción:\n{self.instruccion}"


@dataclass
class TareaQA:
    """
    Entidad principal que representa una tarea de QA
    Contiene todas las reglas de negocio relacionadas con las tareas
    """
    titulo: str
    jira: str
    ambientes_prs: List[AmbientePR] = field(default_factory=list)
    comentarios: List[ComentarioQA] = field(default_factory=list)
    qa_usabilidad: List[str] = field(default_factory=list)
    qa_codigo: List[str] = field(default_factory=list)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_modificacion: datetime = field(default_factory=datetime.now)
    id: Optional[str] = None
    
    def __post_init__(self):
        """Validar campos requeridos"""
        if not self.titulo.strip():
            raise CampoRequeridoException("El título es requerido")
        if not self.jira.strip():
            raise CampoRequeridoException("El link de Jira es requerido")
    
    def agregar_ambiente_pr(self, ambiente: str, pr: str) -> None:
        """
        Agregar un ambiente y PR a la tarea
        Regla de negocio: ambiente y pr no pueden estar vacíos
        """
        ambiente_pr = AmbientePR(ambiente, pr)
        self.ambientes_prs.append(ambiente_pr)
        self._actualizar_fecha_modificacion()
    
    def eliminar_ambiente_pr(self, index: int) -> bool:
        """
        Eliminar un ambiente y PR por índice
        Regla de negocio: el índice debe ser válido
        """
        if 0 <= index < len(self.ambientes_prs):
            del self.ambientes_prs[index]
            self._actualizar_fecha_modificacion()
            return True
        return False
    
    def agregar_comentario(self, tipo: TipoQA, link: str, ambiente: str, instruccion: str) -> None:
        """
        Agregar un comentario de QA
        Regla de negocio: todos los campos son requeridos
        """
        comentario = ComentarioQA(tipo, link, ambiente, instruccion)
        self.comentarios.append(comentario)
        self._actualizar_fecha_modificacion()
    
    def eliminar_comentario(self, index: int) -> bool:
        """
        Eliminar un comentario por índice
        Regla de negocio: el índice debe ser válido
        """
        if 0 <= index < len(self.comentarios):
            del self.comentarios[index]
            self._actualizar_fecha_modificacion()
            return True
        return False
    
    def agregar_qa_usabilidad(self, qa: str) -> None:
        """
        Agregar un QA de usabilidad
        Regla de negocio: el nombre no puede estar vacío
        """
        if not qa.strip():
            raise CampoRequeridoException("El nombre del QA es requerido")
        if qa.strip() not in self.qa_usabilidad:
            self.qa_usabilidad.append(qa.strip())
            self._actualizar_fecha_modificacion()
    
    def eliminar_qa_usabilidad(self, index: int) -> bool:
        """
        Eliminar un QA de usabilidad por índice
        Regla de negocio: el índice debe ser válido
        """
        if 0 <= index < len(self.qa_usabilidad):
            del self.qa_usabilidad[index]
            self._actualizar_fecha_modificacion()
            return True
        return False
    
    def agregar_qa_codigo(self, qa: str) -> None:
        """
        Agregar un QA de código
        Regla de negocio: el nombre no puede estar vacío
        """
        if not qa.strip():
            raise CampoRequeridoException("El nombre del QA es requerido")
        if qa.strip() not in self.qa_codigo:
            self.qa_codigo.append(qa.strip())
            self._actualizar_fecha_modificacion()
    
    def eliminar_qa_codigo(self, index: int) -> bool:
        """
        Eliminar un QA de código por índice
        Regla de negocio: el índice debe ser válido
        """
        if 0 <= index < len(self.qa_codigo):
            del self.qa_codigo[index]
            self._actualizar_fecha_modificacion()
            return True
        return False
    
    def actualizar_titulo(self, titulo: str) -> None:
        """
        Actualizar el título de la tarea
        Regla de negocio: el título no puede estar vacío
        """
        if not titulo.strip():
            raise CampoRequeridoException("El título es requerido")
        self.titulo = titulo.strip()
        self._actualizar_fecha_modificacion()
    
    def actualizar_jira(self, jira: str) -> None:
        """
        Actualizar el link de Jira
        Regla de negocio: el link no puede estar vacío
        """
        if not jira.strip():
            raise CampoRequeridoException("El link de Jira es requerido")
        self.jira = jira.strip()
        self._actualizar_fecha_modificacion()
    
    def esta_completa(self) -> bool:
        """
        Verificar si la tarea está completa
        Regla de negocio: debe tener título, jira y al menos un ambiente/PR
        """
        return (
            bool(self.titulo.strip()) and
            bool(self.jira.strip()) and
            len(self.ambientes_prs) > 0
        )
    
    def obtener_resumen(self) -> str:
        """
        Obtener un resumen de la tarea
        Regla de negocio: incluir información básica
        """
        return f"Tarea: {self.titulo} | Jira: {self.jira} | Ambientes: {len(self.ambientes_prs)}"
    
    def _actualizar_fecha_modificacion(self) -> None:
        """Actualizar la fecha de modificación"""
        self.fecha_modificacion = datetime.now()
    
    def __str__(self) -> str:
        return f"TareaQA(id={self.id}, titulo='{self.titulo}', ambientes={len(self.ambientes_prs)})" 