"""
Caso de uso para enviar notificaciones a Slack
"""

from typing import Optional
from ...domain.services.notificacion_service import NotificacionService
from ...domain.entities.tarea import TareaQA
from ...shared.exceptions.domain_exceptions import DomainException


class EnviarNotificacionSlackUseCase:
    """Caso de uso para enviar notificaciones a Slack"""
    
    def __init__(self, notificacion_service: NotificacionService):
        self.notificacion_service = notificacion_service
    
    def execute(self, mensaje: str, canal: str, **kwargs) -> bool:
        """
        Ejecuta el envío de una notificación simple
        """
        try:
            return self.notificacion_service.enviar_notificacion(mensaje, canal, **kwargs)
        except Exception as e:
            raise DomainException(f"Error al enviar notificación: {str(e)}")
    
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool:
        """
        Ejecuta el envío de un reporte de QA
        """
        try:
            return self.notificacion_service.enviar_reporte_qa(tarea, canal)
        except Exception as e:
            raise DomainException(f"Error al enviar reporte de QA: {str(e)}")
    
    def enviar_mensaje_personalizado(self, tarea: TareaQA, canal: str, 
                                   mensaje_personalizado: Optional[str] = None) -> bool:
        """
        Ejecuta el envío de un mensaje personalizado con el reporte
        """
        try:
            if mensaje_personalizado:
                # Enviar mensaje personalizado primero
                self.notificacion_service.enviar_notificacion(mensaje_personalizado, canal)
            
            # Luego enviar el reporte
            return self.notificacion_service.enviar_reporte_qa(tarea, canal)
        except Exception as e:
            raise DomainException(f"Error al enviar mensaje personalizado: {str(e)}") 