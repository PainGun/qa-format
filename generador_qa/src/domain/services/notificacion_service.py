"""
Servicio de dominio para notificaciones
Define la lógica de negocio para enviar notificaciones
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.tarea import TareaQA


class NotificacionService(ABC):
    """Interfaz para el servicio de notificaciones"""
    
    @abstractmethod
    def enviar_notificacion(self, mensaje: str, canal: str, **kwargs) -> bool:
        """Envía una notificación a un canal específico"""
        pass
    
    @abstractmethod
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool:
        """Envía un reporte de QA formateado"""
        pass


class NotificacionSlackService(NotificacionService):
    """Implementación específica para Slack"""
    
    def __init__(self, token: str, workspace: str):
        self.token = token
        self.workspace = workspace
    
    def enviar_notificacion(self, mensaje: str, canal: str, **kwargs) -> bool:
        """
        Envía una notificación a Slack
        Regla de negocio: validar que el mensaje no esté vacío
        """
        if not mensaje.strip():
            raise ValueError("El mensaje no puede estar vacío")
        
        if not canal.strip():
            raise ValueError("El canal es requerido")
        
        # La implementación real se hará en la capa de infraestructura
        return True
    
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool:
        """
        Envía un reporte de QA formateado para Slack
        Regla de negocio: la tarea debe estar completa
        """
        if not tarea.esta_completa():
            raise ValueError("La tarea debe estar completa para enviar el reporte")
        
        mensaje = self._formatear_mensaje_slack(tarea)
        return self.enviar_notificacion(mensaje, canal)
    
    def _formatear_mensaje_slack(self, tarea: TareaQA) -> str:
        """Formatea el mensaje para Slack con emojis y estructura"""
        ambientes_text = "\n".join(f"• {str(ambiente)}" for ambiente in tarea.ambientes_prs)
        comentarios_text = "\n\n".join(f"• {str(comentario)}" for comentario in tarea.comentarios)
        qa_usu_text = "\n".join(f"• {qa}" for qa in tarea.qa_usabilidad)
        qa_cod_text = "\n".join(f"• {qa}" for qa in tarea.qa_codigo)
        
        return f"""
:clipboard: *Nuevo Reporte de QA*

:page_facing_up: *Tarea:* {tarea.titulo}
:link: *Jira:* {tarea.jira}

:rocket: *Ambientes + PRs:*
{ambientes_text if ambientes_text else '• Sin registros agregados'}

:speech_balloon: *Comentarios:*
{comentarios_text if comentarios_text else '• Sin comentarios agregados'}

:people_holding_hands: *Responsables:*

:eyes: *QA Usabilidad:*
{qa_usu_text if qa_usu_text else '• Ninguno'}

:computer: *QA Código:*
{qa_cod_text if qa_cod_text else '• Ninguno'}

---
:clock1: Generado el {tarea.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}
        """.strip() 