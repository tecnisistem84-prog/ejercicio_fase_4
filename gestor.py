"""Módulo GestorFJ: Administración en memoria, ejecución protegida y auditoría en logs."""
import logging
import os

from entidades import Cliente
from excepciones import (
    ClienteDuplicadoError,
    ClienteInvalidoError,
    ClienteNoEncontradoError,
    ServicioDuplicadoError,
    ServicioInvalidoError,
    ServicioNoEncontradoError,
    SoftwareFJError,
)
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

# Diccionario de mapeo para instanciar dinámicamente cada tipo de servicio especializado
TIPOS_SERVICIO = {
    "sala": ReservaSala,
    "equipo": AlquilerEquipo,
    "asesoria": AsesoriaEspecializada,
}


class GestorFJ:
    """Controlador central de Software FJ sin dependencia de bases de datos."""

    def __init__(self, carpeta_logs="logs"):
        # Estructuras en memoria para almacenar entidades y trazabilidad de operaciones
        self.clientes = {}
        self.servicios = {}
        self.reservas = []
        self.resultados = []

        # Configuracion del sistema de registro de eventos y errores en archivo .log
        os.makedirs(carpeta_logs, exist_ok=True)
        self.log = logging.getLogger("software_fj")
        self.log.setLevel(logging.INFO)
        self.log.handlers.clear()
        manejador = logging.FileHandler(
            os.path.join(carpeta_logs, "software_fj.log"), mode="w", encoding="utf-8"
        )
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        self.log.addHandler(manejador)

    # ---------------- Operaciones de Negocio ----------------
    def registrar_cliente(self, **datos):
        """Valida e incorpora un nuevo cliente aplicando encadenamiento de excepciones."""
        try:
            cliente = Cliente(**datos)
        except TypeError as e:
            # Encadenamiento: transforma un error nativo de argumentos en excepción de dominio
            raise ClienteInvalidoError(f"Datos incompletos o no reconocidos: {e}") from e

        if cliente.id_cliente in self.clientes:
            raise ClienteDuplicadoError(f"Ya existe un cliente con documento {cliente.id_cliente}.")

        self.clientes[cliente.id_cliente] = cliente
        return cliente

    def crear_servicio(self, tipo, **datos):
        """Instancia un servicio especializado según su tipo y lo registra en el catálogo."""
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
        """Crea una reserva vinculando cliente y servicio, y ejecuta su confirmación."""
        cliente = self.clientes.get(id_cliente)
        if cliente is None:
            raise ClienteNoEncontradoError(f"Cliente {id_cliente!r} no registrado.")

        servicio = self.servicios.get(str(codigo_servicio).upper())
        if servicio is None:
            raise ServicioNoEncontradoError(f"Servicio {codigo_servicio!r} no existe.")

        reserva = Reserva(cliente, servicio, horas, descuento)
        self.reservas.append(reserva)  # Se conserva historial incluso si pasa a estado FALLIDA
        reserva.confirmar()
        return reserva

    def cancelar_reserva(self, id_reserva):
        """Busca una reserva activa por su código y cambia su estado a CANCELADA."""
        for r in self.reservas:
            if r.id_reserva == id_reserva:
                r.cancelar()
                return r
        raise SoftwareFJError(f"Reserva {id_reserva!r} no encontrada.")

    # ---------------- Ejecución Protegida y Auditoría ----------------
    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta cada operación aislando fallos para garantizar continuidad operativa."""
        n = len(self.resultados) + 1
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as e:
            # Excepciones controladas propias de las reglas de negocio
            estado, detalle = "ERROR CONTROLADO", str(e)
            self.log.warning("Op %02d %s -> %s", n, descripcion, detalle)
        except Exception as e:
            # Excepciones críticas inesperadas del sistema (ej. ZeroDivisionError)
            estado, detalle = "ERROR INESPERADO", f"{type(e).__name__}: {e}"
            self.log.error("Op %02d %s -> %s", n, descripcion, detalle, exc_info=True)
        else:
            # Se ejecuta únicamente si no ocurrió ninguna excepción
            estado, detalle = "OK", str(resultado)
            self.log.info("Op %02d %s -> %s", n, descripcion, detalle)
        finally:
            # Registro de cierre obligatorio de la transacción
            self.log.info("Op %02d finalizada", n)

        self.resultados.append((n, descripcion, estado))
        print(f"[{n:02d}] {descripcion}\n     -> {estado}: {detalle}\n")

    def generar_reporte_financiero(self):
        """Calcula indicadores de ingresos confirmados y estadísticas de estado de reservas."""
        confirmadas = [r for r in self.reservas if r.estado == "CONFIRMADA"]
        canceladas = [r for r in self.reservas if r.estado == "CANCELADA"]
        fallidas = [r for r in self.reservas if r.estado == "FALLIDA"]
        ingresos_totales = sum(r.costo for r in confirmadas if r.costo is not None)

        reporte = (
            "\n--- REPORTE FINANCIERO Y AUDITORÍA DE RESERVAS ---\n"
            f"  * Total reservas procesadas : {len(self.reservas)}\n"
            f"  * Confirmadas (activas)     : {len(confirmadas)}\n"
            f"  * Canceladas                : {len(canceladas)}\n"
            f"  * Fallidas (rechazadas)     : {len(fallidas)}\n"
            f"  * Ingresos netos confirmados: ${ingresos_totales:,.2f} COP\n"
        )
        self.log.info("Reporte financiero generado: Ingresos=$%.2f", ingresos_totales)
        return reporte