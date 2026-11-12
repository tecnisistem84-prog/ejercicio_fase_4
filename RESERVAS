"""Reserva: integra Cliente + Servicio con ciclo de vida y manejo de errores."""
from datetime import datetime

from entidades import Cliente, Entidad
from excepciones import ReservaError, ServicioNoDisponibleError, SoftwareFJError
from servicios import Servicio


class Reserva(Entidad):
    _consecutivo = 0

    def __init__(self, cliente, servicio, horas, descuento=0.0):
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un Servicio válido.")
        Reserva._consecutivo += 1
        self.id_reserva = f"R{Reserva._consecutivo:03d}"
        self.cliente, self.servicio = cliente, servicio
        self.horas, self.descuento = horas, descuento
        self.estado = "PENDIENTE"
        self.costo = None
        self.creada = datetime.now()

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise ReservaError(f"{self.id_reserva}: solo se confirma una reserva PENDIENTE (estado {self.estado}).")
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self.servicio.codigo} no está disponible.")
            self.costo = self.servicio.calcular_costo(self.horas, self.descuento)
        except SoftwareFJError as causa:
            self.estado = "FALLIDA"
            # encadenamiento de excepciones: se conserva la causa original
            raise ReservaError(f"{self.id_reserva}: no se pudo confirmar ({causa.mensaje})") from causa
        else:
            self.estado = "CONFIRMADA"
        finally:
            self.actualizada = datetime.now()  # se ejecuta siempre

    def cancelar(self):
        if self.estado != "CONFIRMADA":
            raise ReservaError(f"{self.id_reserva}: solo se cancela una reserva CONFIRMADA (estado {self.estado}).")
        self.estado = "CANCELADA"

    def describir(self):
        costo = f"${self.costo:,.0f}" if self.costo is not None else "-"
        return (f"{self.id_reserva} | {self.cliente.nombre} | {self.servicio.codigo} | "
                f"{self.horas} h | {self.estado} | {costo}")

    def __str__(self):
        return self.describir()
