"""
Cliente de Slack para la capa de infraestructura
Implementa la comunicación real con la API de Slack
"""

import requests
import json
from typing import Dict, Any, Optional
from ...shared.exceptions.domain_exceptions import DomainException


class SlackClient:
    """Cliente para interactuar con la API de Slack"""
    
    def __init__(self, token: str, workspace: str = "slack.com"):
        self.token = token
        self.base_url = f"https://{workspace}/api"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def enviar_mensaje(self, canal: str, mensaje: str, **kwargs) -> bool:
        """
        Envía un mensaje a un canal específico
        """
        try:
            payload = {
                "channel": canal,
                "text": mensaje,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/chat.postMessage",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    return True
                else:
                    raise DomainException(f"Error de Slack: {result.get('error', 'Unknown error')}")
            else:
                raise DomainException(f"Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise DomainException(f"Error de conexión: {str(e)}")
        except json.JSONDecodeError as e:
            raise DomainException(f"Error al procesar respuesta: {str(e)}")
    
    def enviar_mensaje_con_bloques(self, canal: str, bloques: list, **kwargs) -> bool:
        """
        Envía un mensaje con bloques de Slack (formato avanzado)
        """
        try:
            payload = {
                "channel": canal,
                "blocks": bloques,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/chat.postMessage",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    return True
                else:
                    raise DomainException(f"Error de Slack: {result.get('error', 'Unknown error')}")
            else:
                raise DomainException(f"Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise DomainException(f"Error de conexión: {str(e)}")
        except json.JSONDecodeError as e:
            raise DomainException(f"Error al procesar respuesta: {str(e)}")
    
    def obtener_canales(self) -> list:
        """
        Obtiene la lista de canales disponibles
        """
        try:
            response = requests.get(
                f"{self.base_url}/conversations.list",
                headers=self.headers,
                params={"types": "public_channel,private_channel"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    return result.get("channels", [])
                else:
                    raise DomainException(f"Error de Slack: {result.get('error', 'Unknown error')}")
            else:
                raise DomainException(f"Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise DomainException(f"Error de conexión: {str(e)}")
        except json.JSONDecodeError as e:
            raise DomainException(f"Error al procesar respuesta: {str(e)}")
    
    def verificar_conexion(self) -> bool:
        """
        Verifica que la conexión con Slack funcione
        """
        try:
            response = requests.get(
                f"{self.base_url}/auth.test",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("ok", False)
            return False
            
        except Exception:
            return False
    
    def crear_bloques_reporte_qa(self, titulo: str, jira: str, ambientes: list, 
                               comentarios: list, qa_usabilidad: list, qa_codigo: list) -> list:
        """
        Crea bloques de Slack para un reporte de QA
        """
        bloques = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📋 Nuevo Reporte de QA",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Tarea:*\n{titulo}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Jira:*\n{jira}"
                    }
                ]
            }
        ]
        
        # Agregar ambientes
        if ambientes:
            ambientes_text = "\n".join(f"• {str(ambiente)}" for ambiente in ambientes)
            bloques.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚀 Ambientes + PRs:*\n{ambientes_text}"
                }
            })
        
        # Agregar comentarios
        if comentarios:
            comentarios_text = "\n\n".join(f"• {str(comentario)}" for comentario in comentarios)
            bloques.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*💬 Comentarios:*\n{comentarios_text}"
                }
            })
        
        # Agregar responsables
        responsables_fields = []
        if qa_usabilidad:
            qa_usu_text = "\n".join(f"• {qa}" for qa in qa_usabilidad)
            responsables_fields.append({
                "type": "mrkdwn",
                "text": f"*👀 QA Usabilidad:*\n{qa_usu_text}"
            })
        
        if qa_codigo:
            qa_cod_text = "\n".join(f"• {qa}" for qa in qa_codigo)
            responsables_fields.append({
                "type": "mrkdwn",
                "text": f"*💻 QA Código:*\n{qa_cod_text}"
            })
        
        if responsables_fields:
            bloques.append({
                "type": "section",
                "fields": responsables_fields
            })
        
        # Agregar separador
        bloques.append({
            "type": "divider"
        })
        
        return bloques 