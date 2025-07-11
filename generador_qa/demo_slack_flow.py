#!/usr/bin/env python3
"""
Demostración del flujo completo con integración de Slack
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def demo_flujo_completo():
    """Demuestra el flujo completo de uso con Slack"""
    print("🚀 DEMOSTRACIÓN: Flujo Completo con Slack")
    print("=" * 60)
    
    print("\n📋 PASO 1: Configurar la aplicación")
    print("- Abre la aplicación: python main_slack.py")
    print("- Ve a la pestaña '🔗 Slack'")
    print("- Configura tu token de bot de Slack")
    print("- Haz clic en '🧪 Probar Conexión'")
    
    print("\n📝 PASO 2: Llenar los datos de QA")
    print("- Pestaña '📋 Resultado' > '🔄 Generar'")
    print("- Completa la información básica:")
    print("  • Título de la tarea")
    print("  • Link de Jira")
    print("- Agrega ambientes y PRs:")
    print("  • Ambiente: Desarrollo")
    print("  • PR: https://github.com/company/app/pull/123")
    print("- Agrega comentarios de QA:")
    print("  • Tipo: Usabilidad")
    print("  • Link: https://staging.company.com/feature")
    print("  • Instrucción: Verificar flujo de usuario")
    print("- Agrega responsables:")
    print("  • QA Usabilidad: Ana García")
    print("  • QA Código: Carlos López")
    
    print("\n🔄 PASO 3: Generar el reporte")
    print("- Haz clic en '🔄 Generar'")
    print("- El reporte se genera en formato markdown")
    print("- Puedes copiarlo al portapapeles con '📋 Copiar'")
    
    print("\n📤 PASO 4: Enviar a Slack")
    print("- Haz clic en '📤 Enviar a Slack'")
    print("- Si no está configurado, te llevará a la configuración")
    print("- Si está configurado, te preguntará:")
    print("  • ¿A qué canal quieres enviarlo?")
    print("  • Selecciona un canal de la lista")
    print("  • Confirma el envío")
    
    print("\n✅ PASO 5: Confirmación")
    print("- El reporte se envía con formato rico")
    print("- Incluye emojis y estructura organizada")
    print("- Aparece en el canal seleccionado")
    print("- Recibes confirmación en la aplicación")
    
    print("\n" + "=" * 60)
    print("🎯 FLUJO ALTERNATIVO: Envío Directo")
    print("=" * 60)
    
    print("\n📤 Envío Directo desde Menú:")
    print("- Menú > Slack > Enviar a Slack")
    print("- O usar Ctrl+S")
    print("- Te guía automáticamente por el proceso")
    
    print("\n🧪 Mensaje de Prueba:")
    print("- Menú > Slack > Mensaje de Prueba")
    print("- Envía un mensaje simple para verificar la conexión")
    
    print("\n" + "=" * 60)
    print("🔧 CONFIGURACIÓN AVANZADA")
    print("=" * 60)
    
    print("\n📋 Pestaña '📤 Envío':")
    print("- Estado de conexión de Slack")
    print("- Canal seleccionado actualmente")
    print("- Botones de acción rápida")
    print("- Información del envío")
    
    print("\n🎯 Selección de Canal:")
    print("- Lista de canales disponibles")
    print("- Canales públicos y privados")
    print("- Indicadores visuales (🌐 público, 🔒 privado)")
    print("- Búsqueda y filtrado")
    
    print("\n⚙️ Configuración:")
    print("- Token de bot persistente")
    print("- Workspace configurable")
    print("- Validación automática")
    print("- Manejo de errores")
    
    print("\n" + "=" * 60)
    print("🎨 CARACTERÍSTICAS DE LA INTERFAZ")
    print("=" * 60)
    
    print("\n📱 Interfaz Moderna:")
    print("- Pestañas organizadas")
    print("- Scroll automático")
    print("- Barra de estado")
    print("- Menús contextuales")
    
    print("\n⌨️ Atajos de Teclado:")
    print("- Ctrl+G: Generar reporte")
    print("- Ctrl+S: Enviar a Slack")
    print("- Ctrl+C: Copiar al portapapeles")
    
    print("\n🔔 Notificaciones:")
    print("- Mensajes de confirmación")
    print("- Indicadores de estado")
    print("- Manejo de errores")
    print("- Feedback visual")
    
    print("\n" + "=" * 60)
    print("🚀 PRÓXIMAS FUNCIONALIDADES")
    print("=" * 60)
    
    print("\n📊 Funcionalidades Planificadas:")
    print("- Persistencia de configuración")
    print("- Múltiples workspaces")
    print("- Plantillas personalizables")
    print("- Envío programado")
    print("- Integración con Jira")
    print("- Comandos slash en Slack")
    
    print("\n" + "=" * 60)
    print("📚 DOCUMENTACIÓN")
    print("=" * 60)
    
    print("\n📖 Archivos de Documentación:")
    print("- docs/SLACK_INTEGRATION.md: Guía completa")
    print("- docs/ARCHITECTURE.md: Arquitectura del proyecto")
    print("- README.md: Información general")
    
    print("\n🔧 Archivos de Ejemplo:")
    print("- ejemplo_slack.py: Ejemplos de código")
    print("- demo_slack_flow.py: Esta demostración")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Disfruta usando Generador QA con Slack!")
    print("=" * 60)


def demo_codigo_programatico():
    """Demuestra el uso programático"""
    print("\n💻 DEMOSTRACIÓN: Uso Programático")
    print("=" * 60)
    
    print("\n📝 Ejemplo de código:")
    print("""
from src.infrastructure.external.slack_notification_service import SlackNotificationService
from src.application.use_cases.enviar_notificacion_slack import EnviarNotificacionSlackUseCase
from src.domain.entities.tarea import TareaQA

# Configurar Slack
slack_service = SlackNotificationService("xoxb-tu-token", "tu-workspace.slack.com")

# Crear caso de uso
use_case = EnviarNotificacionSlackUseCase(slack_service)

# Crear tarea
tarea = TareaQA("Mi Tarea", "https://jira.com/123")
tarea.agregar_ambiente_pr("Desarrollo", "https://github.com/pr/123")

# Enviar reporte
use_case.enviar_reporte_qa(tarea, "#qa-reports")
    """)
    
    print("\n🔧 Configuración avanzada:")
    print("""
# Verificar conexión
if slack_service.verificar_conexion():
    print("✅ Slack conectado")

# Obtener canales
canales = slack_service.obtener_canales_disponibles()
for canal in canales:
    print(f"Canal: #{canal['name']}")

# Enviar mensaje personalizado
use_case.enviar_mensaje_personalizado(tarea, "#general", "🚨 URGENTE: Nuevo reporte")
    """)


if __name__ == "__main__":
    demo_flujo_completo()
    demo_codigo_programatico() 