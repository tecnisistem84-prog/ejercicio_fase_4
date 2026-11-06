"""Servicios: clase abstracta + 3 especializaciones (herencia y polimorfismo)."""
from abc import ABC, abstractmethod

from entidades import Entidad
from excepciones import CalculoCostoError, ServicioInvalidoError


def _es_numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


class Servicio(Entidad, ABC):
    HORAS_MIN, HORAS_MAX = 1, 12

    def __init__(self, codigo, nombre, tarifa_hora):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ServicioInvalidoError(f"Código de servicio inválido: {codigo!r}.")
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError(f"Nombre de servicio inválido: {nombre!r}.")
        if not _es_numero(tarifa_hora) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r} (debe ser > 0).")
        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = True

    # ---- cálculo de costo: método sobrecargado con parámetros opcionales ----
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        """Costo final = (base * (1-descuento)) * (1+impuesto)."""
        self._validar_horas(horas)
        if not _es_numero(descuento) or not 0 <= descuento <= 0.5:
            raise CalculoCostoError(f"Descuento inválido: {descuento!r} (0 a 0.5).")
        if not _es_numero(impuesto) or not 0 <= impuesto <= 0.5:
            raise CalculoCostoError(f"Impuesto inválido: {impuesto!r}.")
        subtotal = self._costo_base(horas)
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def _validar_horas(self, horas):
        if not _es_numero(horas) or not self.HORAS_MIN <= horas <= self.HORAS_MAX:
            raise CalculoCostoError(
                f"Duración inválida: {horas!r} (permitido {self.HORAS_MIN}-{self.HORAS_MAX} h).")

    @abstractmethod
    def _costo_base(self, horas):
        """Cada servicio define su propia regla de costo (polimorfismo)."""

    def describir(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"{self.__class__.__name__} {self.codigo} | {self.nombre} | ${self.tarifa_hora:,.0f}/h | {estado}"

    def __str__(self):
        return self.describir()


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, capacidad):
        super().__init__(codigo, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self.capacidad = capacidad

    def _costo_base(self, horas):
        recargo = 1.10 if self.capacidad > 20 else 1.0  # salas grandes +10 %
        return self.tarifa_hora * horas * recargo


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, deposito):
        super().__init__(codigo, nombre, tarifa_hora)
        if not _es_numero(deposito) or deposito < 0:
            raise ServicioInvalidoError(f"Depósito inválido: {deposito!r}.")
        self.deposito = float(deposito)

    def _costo_base(self, horas):
        return self.tarifa_hora * horas + self.deposito


class AsesoriaEspecializada(Servicio):
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, codigo, nombre, tarifa_hora, nivel):
        super().__init__(codigo, nombre, tarifa_hora)
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r} (use {', '.join(self.NIVELES)}).")
        self.nivel = nivel.lower()

    def _costo_base(self, horas):
        return self.tarifa_hora * horas * self.NIVELES[self.nivel]
