# Generador de QA - Aplicación PyQt6

Una aplicación de escritorio moderna para generar tareas de QA de manera eficiente, construida con PyQt6.

## Características

- **Interfaz moderna**: Interfaz de usuario elegante y responsive usando PyQt6
- **Gestión de ambientes y PRs**: Agregar y gestionar ambientes con sus PRs asociados
- **Comentarios de QA**: Crear comentarios detallados con instrucciones específicas
- **QA Usabilidad y Código**: Separar responsabilidades entre QA de usabilidad y código
- **Generación automática**: Generar texto formateado para tareas de QA
- **Copiar al portapapeles**: Función integrada para copiar el resultado generado
- **🤖 Chatbot RFlex**: Asistente IA especializado en QA (módulo independiente)
- **🔗 Integración Slack**: Envío de reportes a canales de Slack
- **🐙 Integración GitHub**: Gestión de repositorios y commits
- **🔧 Integración Jira**: Gestión de tickets y estados

## Instalación

### Requisitos
- Python 3.8 o superior
- PyQt6

### Instalación de dependencias

```bash
# Instalar PyQt6
pip3 install PyQt6 --break-system-packages
```

## Uso

### Ejecutar la aplicación

```bash
# Aplicación principal
python3 main.py

# Ejemplo independiente del chatbot RFlex
python3 generador_qa/ejemplo_rflex.py
```

### Funcionalidades principales

1. **📝 Generador de QA**
   - Información básica de tareas
   - Gestión de ambientes y PRs
   - Comentarios detallados de QA
   - QA de usabilidad y código
   - Generación automática de texto formateado

2. **🤖 Chatbot RFlex**
   - Chat en tiempo real con IA especializada en QA
   - Gestión de múltiples sesiones de chat
   - Análisis de código y documentación
   - Generación de casos de prueba
   - Exportación de conversaciones

3. **🔗 Integración Slack**
   - Configuración de tokens y canales
   - Envío de reportes de QA
   - Historial de mensajes enviados
   - Prueba de conexión

4. **🐙 Integración GitHub**
   - Gestión de repositorios
   - Visualización de commits y branches
   - Integración con workflows de QA

5. **🔧 Integración Jira**
   - Gestión de tickets
   - Actualización de estados
   - Seguimiento de tareas

## Estructura del Proyecto

```
├── main.py                    # Aplicación principal con PyQt6
├── controllers.py             # Lógica de control
├── models.py                  # Modelos de datos
├── requirements.txt           # Dependencias del proyecto
├── generador_qa/              # Módulo principal con Clean Architecture
│   ├── src/
│   │   ├── infrastructure/
│   │   │   └── ui/
│   │   │       └── views/
│   │   │           └── widgets/
│   │   │               ├── rflex_chatbot_widget.py    # Widget del chatbot RFlex
│   │   │               ├── slack_config_widget.py     # Widget de configuración Slack
│   │   │               └── panel_resultado_slack.py   # Panel de resultados Slack
│   │   └── ...
│   ├── docs/
│   │   └── RFLEX_CHATBOT.md   # Documentación del chatbot RFlex
│   └── ejemplo_rflex.py       # Ejemplo de uso independiente
├── github_widget.py           # Widget de integración GitHub
├── jira_widget.py             # Widget de integración Jira
└── README.md                  # Este archivo
```

## Tecnologías Utilizadas

- **PyQt6**: Framework de interfaz gráfica moderna
- **Python**: Lenguaje de programación principal
- **Dataclasses**: Para modelos de datos limpios

## Ventajas de PyQt6 sobre Tkinter

- **Interfaz más moderna**: Widgets nativos del sistema operativo
- **Mejor rendimiento**: Más eficiente en el manejo de eventos
- **Más funcionalidades**: Widgets avanzados y personalización
- **Mejor documentación**: API más consistente y bien documentada
- **Soporte multiplataforma**: Funciona igual en Windows, macOS y Linux

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles. 