# Generador Paso a QA

Una aplicación de escritorio desarrollada en Python con Tkinter para generar reportes de QA de manera estructurada y organizada.

## Características

- **Interfaz modular**: Diseño limpio y organizado con secciones bien definidas
- **Gestión de ambientes y PRs**: Agregar y eliminar ambientes con sus PRs asociados
- **Comentarios de QA**: Crear comentarios detallados con instrucciones específicas
- **Gestión de responsables**: Asignar QAs de usabilidad y código
- **Generación automática**: Crear reportes formateados automáticamente
- **Copia al portapapeles**: Funcionalidad para copiar el resultado generado

## Estructura del Proyecto

```
├── main.py              # Archivo original (legacy)
├── main_app.py          # Aplicación principal refactorizada
├── models.py            # Modelos de datos
├── controllers.py       # Lógica de control
├── views.py             # Componentes de interfaz
├── utils.py             # Utilidades auxiliares
└── README.md           # Documentación
```

## Arquitectura

El proyecto sigue el patrón **MVC (Model-View-Controller)**:

### Models (`models.py`)
- `AmbientePR`: Representa un ambiente y su PR asociado
- `ComentarioQA`: Representa un comentario de QA con sus detalles
- `TareaQA`: Modelo principal que contiene toda la información

### Controllers (`controllers.py`)
- `TareaQAController`: Maneja toda la lógica de negocio
- Validaciones de datos
- Operaciones CRUD para cada entidad
- Generación de texto formateado

### Views (`views.py`)
- `ListaConEliminacion`: Widget personalizado para listas con botón de eliminar
- `SeccionAmbientesPRs`: Sección para gestionar ambientes y PRs
- `SeccionComentarios`: Sección para comentarios de QA
- `SeccionQA`: Sección para QAs de usabilidad y código
- `PanelResultado`: Panel para mostrar y copiar el resultado

### Utils (`utils.py`)
- Funciones auxiliares para validación
- Utilidades para manipulación de widgets
- Funciones de formateo

## Instalación y Uso

### Requisitos
- Python 3.7+
- tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución
```bash
# Ejecutar la versión refactorizada (recomendado)
python main_app.py

# O ejecutar la versión original
python main.py
```

## Ventajas de la Refactorización

### 1. **Separación de Responsabilidades**
- Cada archivo tiene una responsabilidad específica
- Fácil de mantener y extender

### 2. **Reutilización de Código**
- Componentes modulares que se pueden reutilizar
- Funciones utilitarias centralizadas

### 3. **Mantenibilidad**
- Código más limpio y organizado
- Fácil de debuggear y modificar

### 4. **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Estructura preparada para futuras mejoras

### 5. **Testabilidad**
- Lógica de negocio separada de la interfaz
- Fácil de escribir pruebas unitarias

## Funcionalidades

### Información Básica
- Título de la tarea
- Link de Jira

### Ambientes y PRs
- Agregar múltiples ambientes con sus PRs
- Eliminar entradas individuales
- Vista en lista organizada

### Comentarios de QA
- Tipo de QA (Usabilidad/Código)
- Link para pruebas
- Ambiente de prueba
- Instrucciones detalladas

### Responsables
- QA de Usabilidad
- QA de Código
- Gestión de múltiples responsables

### Generación de Reporte
- Formato estructurado con markdown
- Secciones claramente definidas
- Copia automática al portapapeles

## Mejoras Futuras Sugeridas

1. **Persistencia de datos**: Guardar/cargar configuraciones
2. **Templates**: Plantillas predefinidas para diferentes tipos de QA
3. **Exportación**: Exportar a diferentes formatos (PDF, Word)
4. **Validación avanzada**: Validación en tiempo real de campos
5. **Temas**: Soporte para temas visuales
6. **Configuración**: Panel de configuración de la aplicación

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios siguiendo la arquitectura existente
4. Añade pruebas si es necesario
5. Envía un pull request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. 