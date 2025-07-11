"""
Objetos de valor para tipos de QA
"""

from enum import Enum


class TipoQA(Enum):
    """Enumeración de tipos de QA"""
    USABILIDAD = "usabilidad"
    CODIGO = "código"
    
    @classmethod
    def from_string(cls, value: str) -> 'TipoQA':
        """Crear TipoQA desde string"""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Tipo de QA inválido: {value}")
    
    def __str__(self) -> str:
        return self.value
    
    def display_name(self) -> str:
        """Obtener nombre para mostrar"""
        return self.value.title() 