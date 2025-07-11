"""
Excepciones del dominio
Definen errores específicos del negocio
"""


class DomainException(Exception):
    """Excepción base para errores del dominio"""
    pass


class CampoRequeridoException(DomainException):
    """Excepción cuando un campo requerido está vacío"""
    pass


class ValidacionException(DomainException):
    """Excepción cuando falla la validación de datos"""
    pass


class EntidadNoEncontradaException(DomainException):
    """Excepción cuando no se encuentra una entidad"""
    pass


class ReglaNegocioException(DomainException):
    """Excepción cuando se viola una regla de negocio"""
    pass


class OperacionNoPermitidaException(DomainException):
    """Excepción cuando una operación no está permitida"""
    pass 