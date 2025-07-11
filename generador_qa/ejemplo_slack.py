#!/usr/bin/env python3
"""
Ejemplo de uso de la integración con Slack
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from domain.entities.tarea import TareaQA, AmbientePR
from domain.value_objects.tipos_qa import TipoQA
from domain.services.notificacion_service import ComentarioQA
from infrastructure.external.slack_notification_service import SlackNotificationService
from application.use_cases.enviar_notificacion_slack import EnviarNotificacionSlackUseCase


def ejemplo_basico():
    """Ejemplo básico de envío de mensaje a Slack"""
    print("🚀 Ejemplo básico de integración con Slack")
    
    # Configurar Slack (reemplaza con tu token real)
    token = "xoxb-tu-token-aqui"  # Reemplaza con tu token
    workspace = "tu-workspace.slack.com"  # Reemplaza con tu workspace
    
    try:
        # Crear servicio de Slack
        slack_service = SlackNotificationService(token, workspace)
        
        # Crear caso de uso
        use_case = EnviarNotificacionSlackUseCase(slack_service)
        
        # Enviar mensaje simple
        canal = "#general"  # Reemplaza con tu canal
        mensaje = "🧪 ¡Hola desde Generador QA! Este es un mensaje de prueba."
        
        print(f"Enviando mensaje a {canal}...")
        resultado = use_case.execute(mensaje, canal)
        
        if resultado:
            print("✅ Mensaje enviado exitosamente")
        else:
            print("❌ Error al enviar mensaje")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_reporte_completo():
    """Ejemplo de envío de reporte completo de QA"""
    print("\n📋 Ejemplo de reporte completo de QA")
    
    # Configurar Slack
    token = "xoxb-tu-token-aqui"  # Reemplaza con tu token
    workspace = "tu-workspace.slack.com"  # Reemplaza con tu workspace
    
    try:
        # Crear una tarea de ejemplo
        tarea = TareaQA(
            titulo="Implementación de login con OAuth2",
            jira="https://jira.company.com/browse/QA-123"
        )
        
        # Agregar ambientes y PRs
        tarea.agregar_ambiente_pr("Desarrollo", "https://github.com/company/app/pull/456")
        tarea.agregar_ambiente_pr("Staging", "https://github.com/company/app/pull/457")
        
        # Agregar comentarios de QA
        tarea.agregar_comentario(
            tipo=TipoQA.USABILIDAD,
            link="https://staging.company.com/login",
            ambiente="Staging",
            instruccion="Verificar que el flujo de login funcione correctamente con Google y GitHub"
        )
        
        tarea.agregar_comentario(
            tipo=TipoQA.CODIGO,
            link="https://github.com/company/app/pull/456",
            ambiente="Desarrollo",
            instruccion="Revisar la implementación de OAuth2, validar manejo de errores y seguridad"
        )
        
        # Agregar responsables
        tarea.agregar_qa_usabilidad("Ana García")
        tarea.agregar_qa_codigo("Carlos López")
        tarea.agregar_qa_codigo("María Rodríguez")
        
        # Crear servicio y caso de uso
        slack_service = SlackNotificationService(token, workspace)
        use_case = EnviarNotificacionSlackUseCase(slack_service)
        
        # Enviar reporte
        canal = "#qa-reports"  # Reemplaza con tu canal
        print(f"Enviando reporte completo a {canal}...")
        
        resultado = use_case.enviar_reporte_qa(tarea, canal)
        
        if resultado:
            print("✅ Reporte enviado exitosamente")
        else:
            print("❌ Error al enviar reporte")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_mensaje_personalizado():
    """Ejemplo de envío de mensaje personalizado con reporte"""
    print("\n💬 Ejemplo de mensaje personalizado")
    
    # Configurar Slack
    token = "xoxb-tu-token-aqui"  # Reemplaza con tu token
    workspace = "tu-workspace.slack.com"  # Reemplaza con tu workspace
    
    try:
        # Crear tarea simple
        tarea = TareaQA(
            titulo="Corrección de bug en dashboard",
            jira="https://jira.company.com/browse/QA-124"
        )
        
        tarea.agregar_ambiente_pr("Hotfix", "https://github.com/company/app/pull/458")
        tarea.agregar_qa_codigo("Luis Pérez")
        
        # Crear servicio y caso de uso
        slack_service = SlackNotificationService(token, workspace)
        use_case = EnviarNotificacionSlackUseCase(slack_service)
        
        # Mensaje personalizado
        mensaje_personalizado = "🚨 **URGENTE**: Nuevo hotfix listo para QA"
        canal = "#qa-urgente"  # Reemplaza con tu canal
        
        print(f"Enviando mensaje personalizado a {canal}...")
        
        resultado = use_case.enviar_mensaje_personalizado(
            tarea, canal, mensaje_personalizado
        )
        
        if resultado:
            print("✅ Mensaje personalizado enviado exitosamente")
        else:
            print("❌ Error al enviar mensaje personalizado")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def verificar_conexion():
    """Verificar conexión con Slack"""
    print("\n🔍 Verificando conexión con Slack...")
    
    token = "xoxb-tu-token-aqui"  # Reemplaza con tu token
    workspace = "tu-workspace.slack.com"  # Reemplaza con tu workspace
    
    try:
        slack_service = SlackNotificationService(token, workspace)
        
        if slack_service.verificar_conexion():
            print("✅ Conexión exitosa con Slack")
            
            # Obtener canales disponibles
            canales = slack_service.obtener_canales_disponibles()
            print(f"📢 Canales disponibles: {len(canales)}")
            
            for canal in canales[:5]:  # Mostrar solo los primeros 5
                nombre = canal.get('name', 'Sin nombre')
                es_privado = "🔒" if canal.get('is_private', False) else "🌐"
                print(f"  {es_privado} #{nombre}")
                
        else:
            print("❌ No se pudo conectar con Slack")
            
    except Exception as e:
        print(f"❌ Error al verificar conexión: {e}")


def main():
    """Función principal del ejemplo"""
    print("🔗 Ejemplos de Integración con Slack")
    print("=" * 50)
    
    # Verificar conexión primero
    verificar_conexion()
    
    # Ejemplos de uso
    ejemplo_basico()
    ejemplo_reporte_completo()
    ejemplo_mensaje_personalizado()
    
    print("\n" + "=" * 50)
    print("📚 Para más información, consulta docs/SLACK_INTEGRATION.md")
    print("🔧 Recuerda reemplazar los tokens y canales con los tuyos")


if __name__ == "__main__":
    main() 