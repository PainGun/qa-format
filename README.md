# Generador de QA - Aplicación PyQt6

Una aplicación de escritorio moderna para generar tareas de QA de manera eficiente, construida con PyQt6.

## Características

- **Interfaz moderna**: Interfaz de usuario elegante y responsive usando PyQt6
- **Gestión de ambientes y PRs**: Agregar y gestionar ambientes con sus PRs asociados
- **Comentarios de QA**: Crear comentarios detallados con instrucciones específicas
- **QA Usabilidad y Código**: Separar responsabilidades entre QA de usabilidad y código
- **Generación automática**: Generar texto formateado para tareas de QA
- **Copiar al portapapeles**: Función integrada para copiar el resultado generado

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
python3 main_app.py
```

### Funcionalidades principales

1. **Información Básica**
   - Título de la tarea
   - Link de Jira

2. **Ambientes + PRs**
   - Agregar ambientes con sus PRs correspondientes
   - Eliminar elementos de la lista

3. **Comentarios de QA**
   - Tipo de QA
   - Link de prueba
   - Ambiente
   - Instrucciones detalladas

4. **QA Usabilidad y Código**
   - Agregar responsables para cada tipo de QA
   - Gestión independiente de listas

5. **Generación de Resultado**
   - Botón "Generar" para crear el texto formateado
   - Botón "Copiar" para copiar al portapapeles

## Estructura del Proyecto

```
├── main_app.py          # Aplicación principal con PyQt6
├── controllers.py       # Lógica de control
├── models.py           # Modelos de datos
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
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