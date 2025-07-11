# Arquitectura Detallada - Generador QA

## 🏗️ Clean Architecture Overview

Este proyecto implementa Clean Architecture (Arquitectura Limpia) siguiendo los principios de Robert C. Martin (Uncle Bob). La arquitectura está diseñada para ser independiente de frameworks, testable y mantenible.

## 📊 Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    UI Layer (Tkinter)                       │
├─────────────────────────────────────────────────────────────┤
│                Application Layer (Use Cases)                │
├─────────────────────────────────────────────────────────────┤
│                  Domain Layer (Entities)                    │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Capas de la Arquitectura

### 1. **Domain Layer** (`src/domain/`)

La capa más interna, contiene las entidades y reglas de negocio puras.

#### Entidades (`entities/`)
```python
# Ejemplo: TareaQA
class TareaQA:
    def __init__(self, titulo: str, jira: str):
        self.titulo = titulo
        self.jira = jira
        self.ambientes_prs: List[AmbientePR] = []
        self.comentarios: List[ComentarioQA] = []
        self.qa_usabilidad: List[str] = []
        self.qa_codigo: List[str] = []
    
    def agregar_ambiente_pr(self, ambiente: str, pr: str):
        # Regla de negocio: validar que ambiente y pr no estén vacíos
        if not ambiente.strip() or not pr.strip():
            raise ValueError("Ambiente y PR son requeridos")
        # ...
```

#### Objetos de Valor (`value_objects/`)
```python
# Ejemplo: TipoQA
class TipoQA(Enum):
    USABILIDAD = "usabilidad"
    CODIGO = "código"
```

#### Servicios de Dominio (`services/`)
```python
# Ejemplo: GeneradorTextoService
class GeneradorTextoService:
    def generar_reporte(self, tarea: TareaQA) -> str:
        # Lógica de generación de texto
        # No depende de frameworks externos
```

### 2. **Application Layer** (`src/application/`)

Orquesta las entidades del dominio para realizar casos de uso específicos.

#### Casos de Uso (`use_cases/`)
```python
# Ejemplo: AgregarAmbientePRUseCase
class AgregarAmbientePRUseCase:
    def __init__(self, tarea_repository: TareaRepository):
        self.tarea_repository = tarea_repository
    
    def execute(self, tarea_id: str, ambiente: str, pr: str) -> bool:
        tarea = self.tarea_repository.get_by_id(tarea_id)
        tarea.agregar_ambiente_pr(ambiente, pr)
        self.tarea_repository.save(tarea)
        return True
```

#### Interfaces (`interfaces/`)
```python
# Ejemplo: TareaRepository
class TareaRepository(ABC):
    @abstractmethod
    def save(self, tarea: TareaQA) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, tarea_id: str) -> TareaQA:
        pass
```

#### DTOs (`dto/`)
```python
# Ejemplo: TareaDTO
@dataclass
class TareaDTO:
    titulo: str
    jira: str
    ambientes_prs: List[AmbientePRDTO]
    comentarios: List[ComentarioQADTO]
```

### 3. **Infrastructure Layer** (`src/infrastructure/`)

Implementa las interfaces definidas en la capa de aplicación.

#### UI (`ui/`)
```python
# Ejemplo: TkinterTareaView
class TkinterTareaView:
    def __init__(self, root: tk.Tk, presenter: TareaPresenter):
        self.root = root
        self.presenter = presenter
        self.setup_ui()
    
    def setup_ui(self):
        # Configuración de widgets Tkinter
        # No contiene lógica de negocio
```

#### Persistencia (`persistence/`)
```python
# Ejemplo: FileTareaRepository
class FileTareaRepository(TareaRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def save(self, tarea: TareaQA) -> None:
        # Implementación con archivos
        # Fácil cambiar a base de datos
```

#### Servicios Externos (`external/`)
```python
# Ejemplo: ClipboardService
class ClipboardService:
    def copy_to_clipboard(self, text: str) -> bool:
        # Implementación específica del sistema
```

### 4. **Shared Layer** (`src/shared/`)

Código compartido entre todas las capas.

#### Utilidades (`utils/`)
```python
# Ejemplo: validators.py
def validar_campo_no_vacio(valor: str) -> bool:
    return valor is not None and valor.strip() != ""

def validar_campos_requeridos(campos: List[str]) -> bool:
    return all(validar_campo_no_vacio(campo) for campo in campos)
```

#### Excepciones (`exceptions/`)
```python
# Ejemplo: domain_exceptions.py
class DomainException(Exception):
    """Excepción base para errores del dominio"""
    pass

class CampoRequeridoException(DomainException):
    """Excepción cuando un campo requerido está vacío"""
    pass
```

## 🔄 Flujo de Datos

### 1. **Entrada de Usuario**
```
UI (Tkinter) → Controller → Use Case → Domain Entity
```

### 2. **Procesamiento**
```
Domain Entity → Domain Service → Use Case → Repository
```

### 3. **Salida**
```
Repository → Use Case → Presenter → UI (Tkinter)
```

## 🧪 Testing Strategy

### 1. **Unit Tests**
- **Domain**: Probar entidades y reglas de negocio
- **Application**: Probar casos de uso
- **Infrastructure**: Probar implementaciones

### 2. **Integration Tests**
- Probar interacción entre capas
- Probar flujos completos

### 3. **UI Tests**
- Probar comportamiento de la interfaz
- Mockear dependencias externas

## 📈 Ventajas de esta Arquitectura

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

## 🚀 Migración Gradual

### Fase 1: Estructura Básica ✅
- Crear estructura de carpetas
- Definir interfaces básicas

### Fase 2: Migración de Entidades
- Mover entidades al dominio
- Implementar reglas de negocio

### Fase 3: Casos de Uso
- Crear casos de uso para cada funcionalidad
- Implementar orquestación

### Fase 4: UI Refactorizada
- Migrar UI a la nueva arquitectura
- Implementar presentadores

### Fase 5: Testing Completo
- Agregar pruebas unitarias
- Implementar pruebas de integración

## 📚 Referencias

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture in Python](https://github.com/Enforcer/clean-architecture)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
