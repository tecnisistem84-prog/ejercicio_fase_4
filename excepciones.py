"""Excepciones personalizadas de Software FJ.

Jerarquía:
    SoftwareFJError
    ├── ClienteInvalidoError
    │   ├── ClienteDuplicadoError
    │   └── ClienteNoEncontradoError
    ├── ServicioInvalidoError
    │   ├── ServicioDuplicadoError
    │   ├── ServicioNoEncontradoError
    │   └── ServicioNoDisponibleError
    ├── CalculoCostoError
    └── ReservaError
"""


class SoftwareFJError(Exception):
    """Excepción base: todo error controlado del sistema hereda de ella."""
    codigo = "FJ-000"

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


class ClienteInvalidoError(SoftwareFJError):
    codigo = "FJ-100"


class ClienteDuplicadoError(ClienteInvalidoError):
    codigo = "FJ-101"


class ClienteNoEncontradoError(ClienteInvalidoError):
    codigo = "FJ-102"


class ServicioInvalidoError(SoftwareFJError):
    codigo = "FJ-200"


class ServicioDuplicadoError(ServicioInvalidoError):
    codigo = "FJ-201"


class ServicioNoEncontradoError(ServicioInvalidoError):
    codigo = "FJ-202"


class ServicioNoDisponibleError(ServicioInvalidoError):
    codigo = "FJ-203"


class CalculoCostoError(SoftwareFJError):
    codigo = "FJ-400"


class ReservaError(SoftwareFJError):
    codigo = "FJ-300"
