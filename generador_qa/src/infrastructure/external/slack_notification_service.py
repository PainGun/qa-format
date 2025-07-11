"""
Servicio de notificación de Slack para la capa de infraestructura
Implementa la interfaz del dominio usando el cliente de Slack
"""

from typing import Optional
from ...domain.services.notificacion_service import NotificacionService
from ...domain.entities.tarea import TareaQA
from ...shared.exceptions.domain_exceptions import DomainException
from .slack_client import SlackClient


class SlackNotificationService(NotificacionService):
    """Implementación de notificaciones usando Slack"""
    
    def __init__(self, token: str, workspace: str = "slack.com"):
        self.slack_client = SlackClient(token, workspace)
        self.token = token
        self.workspace = workspace
    
    def enviar_notificacion(self, mensaje: str, canal: str, **kwargs) -> bool:
        """
        Envía una notificación simple a Slack
        """
        try:
            return self.slack_client.enviar_mensaje(canal, mensaje, **kwargs)
        except Exception as e:
            raise DomainException(f"Error al enviar notificación a Slack: {str(e)}")
    
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool:
        """
        Envía un reporte de QA formateado a Slack
        """
        try:
            # Crear bloques de Slack para un formato más rico
            bloques = self.slack_client.crear_bloques_reporte_qa(
                titulo=tarea.titulo,
                jira=tarea.jira,
                ambientes=tarea.ambientes_prs,
                comentarios=tarea.comentarios,
                qa_usabilidad=tarea.qa_usabilidad,
                qa_codigo=tarea.qa_codigo
            )
            
            return self.slack_client.enviar_mensaje_con_bloques(canal, bloques)
            
        except Exception as e:
            raise DomainException(f"Error al enviar reporte de QA a Slack: {str(e)}")
    
    def enviar_reporte_qa_simple(self, tarea: TareaQA, canal: str) -> bool:
        """
        Envía un reporte de QA en formato de texto simple
        """
        try:
            mensaje = self._formatear_mensaje_slack(tarea)
            return self.slack_client.enviar_mensaje(canal, mensaje)
            
        except Exception as e:
            raise DomainException(f"Error al enviar reporte simple a Slack: {str(e)}")
    
    def verificar_conexion(self) -> bool:
        """
        Verifica que la conexión con Slack funcione
        """
        return self.slack_client.verificar_conexion()
    
    def obtener_canales_disponibles(self) -> list:
        """
        Obtiene la lista de canales disponibles
        """
        try:
            return self.slack_client.obtener_canales()
        except Exception as e:
            raise DomainException(f"Error al obtener canales: {str(e)}")
    
    def obtener_usuarios_disponibles(self) -> list:
        """
        Obtiene la lista de usuarios disponibles (no bots, no eliminados)
        """
        try:
            return self.slack_client.obtener_usuarios()
        except Exception as e:
            raise DomainException(f"Error al obtener usuarios: {str(e)}")
    
    def _formatear_mensaje_slack(self, tarea: TareaQA) -> str:
        """Formatea el mensaje para Slack con emojis y estructura"""
        ambientes_text = "\n".join(f"• {str(ambiente)}" for ambiente in tarea.ambientes_prs)
        comentarios_text = "\n\n".join(f"• {str(comentario)}" for comentario in tarea.comentarios)
        qa_usu_text = "\n".join(f"• {qa}" for qa in tarea.qa_usabilidad)
        qa_cod_text = "\n".join(f"• {qa}" for qa in tarea.qa_codigo)
        
        return f"""
📋 *Nuevo Reporte de QA*

📄 *Tarea:* {tarea.titulo}
🔗 *Jira:* {tarea.jira}

🚀 *Ambientes + PRs:*
{ambientes_text if ambientes_text else '• Sin registros agregados'}

💬 *Comentarios:*
{comentarios_text if comentarios_text else '• Sin comentarios agregados'}

👥 *Responsables:*

👀 *QA Usabilidad:*
{qa_usu_text if qa_usu_text else '• Ninguno'}

💻 *QA Código:*
{qa_cod_text if qa_cod_text else '• Ninguno'}

---
🕐 Generado el {tarea.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}
        """.strip() 