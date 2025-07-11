# 🔗 Integración con Slack

Esta documentación explica cómo configurar y usar la integración con Slack en el Generador QA.

## 🎯 Características

- **Envío de reportes**: Envía reportes de QA directamente a canales de Slack
- **Formato rico**: Mensajes con emojis y estructura organizada
- **Configuración fácil**: Interfaz gráfica para configurar credenciales
- **Selección de canales**: Lista de canales disponibles en tu workspace
- **Pruebas de conexión**: Verifica que la configuración funcione

## 🚀 Configuración Inicial

### 1. Crear una App de Slack

1. Ve a [api.slack.com/apps](https://api.slack.com/apps)
2. Haz clic en "Create New App"
3. Selecciona "From scratch"
4. Dale un nombre a tu app (ej: "Generador QA")
5. Selecciona tu workspace

### 2. Configurar Permisos

1. En el menú lateral, ve a "OAuth & Permissions"
2. En "Scopes" > "Bot Token Scopes", agrega estos permisos:
   - `chat:write` - Enviar mensajes
   - `channels:read` - Leer canales públicos
   - `groups:read` - Leer canales privados
   - `users:read` - Leer información de usuarios

### 3. Instalar la App

1. Ve a "Install App" en el menú lateral
2. Haz clic en "Install to Workspace"
3. Autoriza la app

### 4. Obtener el Token

1. En "OAuth & Permissions", copia el "Bot User OAuth Token"
2. El token empieza con `xoxb-`

## 🎨 Uso en la Aplicación

### Configuración

1. Abre el Generador QA
2. Ve a la sección "Configuración de Slack"
3. Pega tu token de bot en el campo "Token de Bot"
4. Haz clic en "🧪 Probar Conexión"
5. Si la conexión es exitosa, verás "✅ Conectado"

### Envío de Reportes

1. Completa tu tarea de QA normalmente
2. En la sección de Slack, selecciona un canal de la lista
3. Haz clic en "📤 Enviar a Slack"
4. El reporte se enviará con formato rico

### Mensajes de Prueba

- Usa "🧪 Mensaje de Prueba" para verificar la configuración
- Los mensajes incluyen emojis y formato markdown
- Se pueden enviar a cualquier canal público o privado

## 📋 Formato de Mensajes

### Reporte Completo
```
📋 Nuevo Reporte de QA

📄 Tarea: [Título de la tarea]
🔗 Jira: [Link de Jira]

🚀 Ambientes + PRs:
• Ambiente: [ambiente] - PR: [pr]

💬 Comentarios:
• Para [tipo] (Ambiente: [ambiente]):
  Prueba en [link]
  Instrucción: [instrucción]

👥 Responsables:

👀 QA Usabilidad:
• [nombre]

💻 QA Código:
• [nombre]

---
🕐 Generado el [fecha]
```

### Mensaje Simple
```
🧪 Mensaje de prueba desde Generador QA
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes configurar Slack usando variables de entorno:

```bash
export SLACK_BOT_TOKEN="xoxb-tu-token-aqui"
export SLACK_WORKSPACE="tu-workspace.slack.com"
```

### Configuración Programática

```python
from src.infrastructure.external.slack_notification_service import SlackNotificationService
from src.application.use_cases.enviar_notificacion_slack import EnviarNotificacionSlackUseCase

# Crear servicio
slack_service = SlackNotificationService("xoxb-tu-token", "tu-workspace.slack.com")

# Crear caso de uso
use_case = EnviarNotificacionSlackUseCase(slack_service)

# Enviar mensaje
use_case.execute("Hola desde Generador QA!", "#general")

# Enviar reporte
use_case.enviar_reporte_qa(tarea, "#qa-reports")
```

## 🛠️ Solución de Problemas

### Error: "invalid_auth"
- Verifica que el token sea correcto
- Asegúrate de que la app esté instalada en el workspace

### Error: "channel_not_found"
- Verifica que el canal existe
- Asegúrate de que el bot tenga acceso al canal

### Error: "missing_scope"
- Agrega los permisos necesarios en la configuración de la app
- Reinstala la app después de cambiar permisos

### Error: "rate_limited"
- Slack tiene límites de rate limiting
- Espera unos segundos antes de enviar otro mensaje

## 🔒 Seguridad

### Tokens
- **Nunca** compartas tu token de bot
- Los tokens empiezan con `xoxb-` y son secretos
- Si se compromete un token, revócalo inmediatamente

### Permisos
- Solo solicita los permisos necesarios
- Revisa regularmente los permisos de tu app
- Usa el principio de menor privilegio

### Workspace
- Solo instala la app en workspaces de confianza
- Revisa qué datos puede acceder la app

## 📚 API Reference

### SlackNotificationService

```python
class SlackNotificationService:
    def __init__(self, token: str, workspace: str = "slack.com")
    def enviar_notificacion(self, mensaje: str, canal: str) -> bool
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool
    def verificar_conexion(self) -> bool
    def obtener_canales_disponibles(self) -> list
```

### EnviarNotificacionSlackUseCase

```python
class EnviarNotificacionSlackUseCase:
    def __init__(self, notificacion_service: NotificacionService)
    def execute(self, mensaje: str, canal: str) -> bool
    def enviar_reporte_qa(self, tarea: TareaQA, canal: str) -> bool
    def enviar_mensaje_personalizado(self, tarea: TareaQA, canal: str, mensaje: str) -> bool
```

## 🚀 Próximas Funcionalidades

### Funcionalidades Planificadas
- **Respuestas automáticas**: Responder a mensajes en Slack
- **Comandos slash**: Comandos `/qa` en Slack
- **Notificaciones programadas**: Enviar reportes automáticamente
- **Integración con Jira**: Vincular tickets de Jira
- **Plantillas personalizables**: Diferentes formatos de mensaje

### Mejoras Técnicas
- **Persistencia de configuración**: Guardar tokens de forma segura
- **Múltiples workspaces**: Conectar con varios workspaces
- **Webhooks**: Recibir notificaciones de Slack
- **Analytics**: Estadísticas de uso

## 🤝 Contribución

Para contribuir a la integración con Slack:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa siguiendo Clean Architecture
4. Agrega pruebas para nuevas funcionalidades
5. Documenta los cambios
6. Envía un pull request

## 📞 Soporte

Si tienes problemas con la integración:

1. Revisa esta documentación
2. Verifica la configuración de tu app de Slack
3. Revisa los logs de la aplicación
4. Abre un issue en GitHub con detalles del problema

---

**¡Disfruta enviando reportes de QA directamente a Slack! 🎉** 