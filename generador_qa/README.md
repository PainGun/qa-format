# 🏗️ Generador QA - Clean Architecture

Una aplicación de escritorio desarrollada en Python con Tkinter siguiendo los principios de **Clean Architecture** para generar reportes de QA de manera estructurada y organizada.

## 🎯 Características

- **🏗️ Clean Architecture**: Separación clara de responsabilidades
- **🧪 Testabilidad**: Código fácil de probar y mantener
- **🔄 Independencia de Frameworks**: Fácil migrar a otras tecnologías
- **📈 Escalabilidad**: Estructura preparada para crecimiento
- **🎨 UI Modular**: Componentes reutilizables y mantenibles

## 📁 Estructura del Proyecto

```
generador_qa/
├── src/                          # Código fuente principal
│   ├── domain/                   # 🎯 Capa de Dominio
│   │   ├── entities/            # Entidades del negocio
│   │   ├── value_objects/       # Objetos de valor
│   │   └── services/            # Servicios de dominio
│   ├── application/             # 🔄 Capa de Aplicación
│   │   ├── use_cases/           # Casos de uso
│   │   ├── interfaces/          # Interfaces (puertos)
│   │   └── dto/                 # Objetos de transferencia
│   ├── infrastructure/          # 🛠️ Capa de Infraestructura
│   │   ├── persistence/         # Persistencia de datos
│   │   ├── ui/                  # Interfaz de usuario
│   │   └── external/            # Servicios externos
│   └── shared/                  # 🔗 Código compartido
│       ├── utils/               # Utilidades
│       └── exceptions/          # Excepciones
├── tests/                       # 🧪 Pruebas
├── config/                      # ⚙️ Configuración
├── docs/                        # 📚 Documentación
├── assets/                      # 🎨 Recursos
├── requirements.txt             # 📦 Dependencias
├── setup.py                     # 📋 Configuración del paquete
└── main.py                      # 🚀 Punto de entrada
```

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7+
- tkinter (incluido en la mayoría de instalaciones de Python)

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd generador_qa

# Instalar dependencias (opcional para desarrollo)
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 🏗️ Arquitectura Clean

### 🎯 **Domain Layer** (Dominio)
- **Entidades**: `TareaQA`, `AmbientePR`, `ComentarioQA`
- **Reglas de Negocio**: Validaciones, lógica pura
- **Independiente**: No conoce frameworks externos

### 🔄 **Application Layer** (Aplicación)
- **Casos de Uso**: Orquestan el dominio
- **Interfaces**: Definen contratos (puertos)
- **DTOs**: Objetos de transferencia de datos

### 🛠️ **Infrastructure Layer** (Infraestructura)
- **UI**: Implementación con Tkinter
- **Persistence**: Almacenamiento de datos
- **External**: Servicios externos (clipboard, etc.)

## 📋 Funcionalidades

### ✅ **Gestión de Tareas**
- Crear y editar tareas de QA
- Validación de campos requeridos
- Reglas de negocio integradas

### ✅ **Ambientes y PRs**
- Asociar ambientes con Pull Requests
- Validación de datos
- Gestión de múltiples entradas

### ✅ **Comentarios de QA**
- Crear comentarios detallados
- Tipos de QA (Usabilidad/Código)
- Instrucciones específicas

### ✅ **Responsables**
- Asignar QAs de usabilidad
- Asignar QAs de código
- Gestión de múltiples responsables

### ✅ **Generación de Reportes**
- Formato markdown estructurado
- Información completa de la tarea
- Copia automática al portapapeles

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=src

# Ejecutar pruebas específicas
pytest tests/unit/domain/
pytest tests/unit/application/
pytest tests/integration/
```

## 📚 Documentación

- [📖 README Principal](docs/README.md)
- [🏗️ Arquitectura Detallada](docs/ARCHITECTURE.md)
- [🔌 API Reference](docs/API.md)

## 🔄 Migración desde la Versión Anterior

### Fase 1: Estructura Básica ✅
- [x] Crear estructura de carpetas
- [x] Configurar archivos básicos
- [x] Documentación inicial

### Fase 2: Migración de Entidades
- [x] Crear entidades del dominio
- [x] Implementar reglas de negocio
- [ ] Migrar lógica existente

### Fase 3: Casos de Uso
- [ ] Crear casos de uso
- [ ] Implementar orquestación
- [ ] Separar lógica de UI

### Fase 4: UI Refactorizada
- [ ] Migrar componentes de UI
- [ ] Implementar presentadores
- [ ] Conectar con casos de uso

### Fase 5: Testing Completo
- [ ] Agregar pruebas unitarias
- [ ] Implementar pruebas de integración
- [ ] Cobertura de código

## 🎯 Ventajas de Clean Architecture

### ✅ **Independencia de Frameworks**
- El dominio no conoce Tkinter
- Fácil migrar a PyQt, web, API, etc.

### ✅ **Testabilidad**
- Cada capa se puede probar independientemente
- Fácil mockear dependencias

### ✅ **Mantenibilidad**
- Código organizado y fácil de entender
- Cambios localizados en capas específicas

### ✅ **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Estructura preparada para crecimiento

### ✅ **Flexibilidad**
- Fácil cambiar implementaciones
- Bajo acoplamiento entre componentes

## 🚀 Próximas Funcionalidades

### 📊 **Persistencia de Datos**
- Guardar/cargar configuraciones
- Base de datos local
- Sincronización en la nube

### 🎨 **Temas y Personalización**
- Temas visuales
- Configuración personalizable
- Accesibilidad mejorada

### 📤 **Exportación Avanzada**
- Múltiples formatos (PDF, Word, HTML)
- Plantillas personalizables
- Integración con herramientas externas

### 🔗 **Integraciones**
- Jira API
- GitHub/GitLab
- Slack notifications

### 🧪 **Testing Avanzado**
- Pruebas automatizadas
- CI/CD pipeline
- Cobertura de código

## 🤝 Contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### 📋 Guías de Contribución

- Sigue los principios de Clean Architecture
- Agrega pruebas para nuevas funcionalidades
- Mantén la documentación actualizada
- Usa commits descriptivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Felipe Duarte** - *Desarrollo inicial* - [Pain-Gun](https://github.com/Pain-Gun)

- **Gonzalo Cañas** - *Desarrollo inicial* - [User](https://github.com/User)

## 🙏 Agradecimientos

- [Robert C. Martin](https://blog.cleancoder.com/) por Clean Architecture
- [Python](https://www.python.org/) y [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Comunidad de desarrolladores que contribuyen al proyecto

---

**⭐ Si este proyecto te ayuda, considera darle una estrella en GitHub!** 