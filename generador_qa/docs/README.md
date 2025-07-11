# Generador QA - Clean Architecture

Una aplicación de escritorio desarrollada en Python con Tkinter siguiendo los principios de Clean Architecture para generar reportes de QA de manera estructurada y organizada.

## 🏗️ Arquitectura

Este proyecto implementa **Clean Architecture** (Arquitectura Limpia) con las siguientes capas:

### 📁 Estructura del Proyecto

```
generador_qa/
├── src/
│   ├── domain/                 # Capa de Dominio
│   │   ├── entities/           # Entidades del dominio
│   │   ├── value_objects/      # Objetos de valor
│   │   └── services/           # Servicios de dominio
│   ├── application/            # Capa de Aplicación
│   │   ├── use_cases/          # Casos de uso
│   │   ├── interfaces/         # Interfaces (puertos)
│   │   └── dto/               # Objetos de transferencia
│   ├── infrastructure/         # Capa de Infraestructura
│   │   ├── persistence/        # Persistencia
│   │   ├── ui/                # Interfaz de usuario
│   │   └── external/          # Servicios externos
│   └── shared/                # Código compartido
│       ├── utils/             # Utilidades
│       └── exceptions/        # Excepciones
├── tests/                     # Pruebas
├── config/                    # Configuración
├── docs/                      # Documentación
└── assets/                    # Recursos
```

## 🎯 Principios de Clean Architecture

### 1. **Independencia de Frameworks**
- El dominio no depende de Tkinter
- Fácil cambiar de UI framework

### 2. **Testabilidad**
- Cada capa se puede probar independientemente
- Fácil mockear dependencias

### 3. **Independencia de UI**
- La lógica de negocio es independiente de la interfaz
- Fácil cambiar de Tkinter a web, API, etc.

### 4. **Independencia de Base de Datos**
- El dominio no conoce detalles de persistencia
- Fácil cambiar de archivos a base de datos

### 5. **Independencia de Agentes Externos**
- El dominio no depende de servicios externos
- Fácil cambiar implementaciones

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd generador_qa

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 📋 Funcionalidades

- **Gestión de Tareas**: Crear y gestionar tareas de QA
- **Ambientes y PRs**: Asociar ambientes con Pull Requests
- **Comentarios de QA**: Crear comentarios detallados
- **Responsables**: Asignar QAs de usabilidad y código
- **Generación de Reportes**: Crear reportes formateados
- **Copia al Portapapeles**: Funcionalidad de copia automática

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=src

# Ejecutar pruebas específicas
pytest tests/unit/domain/
```

## 📚 Documentación Adicional

- [Arquitectura Detallada](ARCHITECTURE.md)
- [API Reference](API.md)

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa siguiendo Clean Architecture
4. Añade pruebas
5. Envía un pull request

## 📄 Licencia

MIT License
