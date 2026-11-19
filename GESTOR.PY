"""Gestor en memoria (sin base de datos) + ejecución protegida + registro en log."""
import logging
import os

from entidades import Cliente
from excepciones import (ClienteDuplicadoError, ClienteInvalidoError, ClienteNoEncontradoError,
                         ServicioDuplicadoError, ServicioInvalidoError, ServicioNoEncontradoError,
                         SoftwareFJError)
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": AsesoriaEspecializada}


class GestorFJ:
    def __init__(self, carpeta_logs="logs"):
        self.clientes, self.servicios, self.reservas, self.resultados = {}, {}, [], []
        os.makedirs(carpeta_logs, exist_ok=True)
        self.log = logging.getLogger("software_fj")
        self.log.setLevel(logging.INFO)
        self.log.handlers.clear()
        manejador = logging.FileHandler(os.path.join(carpeta_logs, "software_fj.log"), mode="w", encoding="utf-8")
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        self.log.addHandler(manejador)

    # ---------------- operaciones de negocio ----------------
    def registrar_cliente(self, **datos):
        try:
            cliente = Cliente(**datos)
        except TypeError as e:  # faltan o sobran parámetros
            raise ClienteInvalidoError(f"Datos incompletos o no reconocidos: {e}") from e
        if cliente.id_cliente in self.clientes:
            raise ClienteDuplicadoError(f"Ya existe un cliente con documento {cliente.id_cliente}.")
        self.clientes[cliente.id_cliente] = cliente
        return cliente

    def crear_servicio(self, tipo, **datos):
        clase = TIPOS_SERVICIO.get(tipo)
        if clase is None:
            raise ServicioInvalidoError(f"Tipo de servicio desconocido: {tipo!r}.")
        try:
            servicio = clase(**datos)
        except TypeError as e:
            raise ServicioInvalidoError(f"Parámetros incorrectos para '{tipo}': {e}") from e
        if servicio.codigo in self.servicios:
            raise ServicioDuplicadoError(f"Ya existe el servicio {servicio.codigo}.")
        self.servicios[servicio.codigo] = servicio
        return servicio

    def reservar(self, id_cliente, codigo_servicio, horas, descuento=0.0):
        cliente = self.clientes.get(id_cliente)
        if cliente is None:
            raise ClienteNoEncontradoError(f"Cliente {id_cliente!r} no registrado.")
        servicio = self.servicios.get(str(codigo_servicio).upper())
        if servicio is None:
            raise ServicioNoEncontradoError(f"Servicio {codigo_servicio!r} no existe.")
        reserva = Reserva(cliente, servicio, horas, descuento)
        self.reservas.append(reserva)  # queda registrada aunque falle
        reserva.confirmar()
        return reserva

    def cancelar_reserva(self, id_reserva):
        for r in self.reservas:
            if r.id_reserva == id_reserva:
                r.cancelar()
                return r
        raise SoftwareFJError(f"Reserva {id_reserva!r} no encontrada.")

    # ---------------- ejecución protegida ----------------
    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación sin permitir que un error detenga el programa."""
        n = len(self.resultados) + 1
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as e:  # error de negocio esperado
            estado, detalle = "ERROR CONTROLADO", str(e)
            self.log.warning("Op %02d %s -> %s", n, descripcion, detalle)
        except Exception as e:  # error grave inesperado
            estado, detalle = "ERROR INESPERADO", f"{type(e).__name__}: {e}"
            self.log.error("Op %02d %s -> %s", n, descripcion, detalle, exc_info=True)
        else:
            estado, detalle = "OK", str(resultado)
            self.log.info("Op %02d %s -> %s", n, descripcion, detalle)
        finally:
            self.log.info("Op %02d finalizada", n)
        self.resultados.append((n, descripcion, estado))
        print(f"[{n:02d}] {descripcion}\n     -> {estado}: {detalle}\n")
