"""Software FJ - Simulación de 15 operaciones (válidas e inválidas)."""
from gestor import GestorFJ


def main():
    g = GestorFJ()
    print("=" * 70, "\n SOFTWARE FJ - SIMULACIÓN DE OPERACIONES\n", "=" * 70, "\n", sep="")

    # --- Clientes ---
    g.ejecutar("Registrar cliente válido (Laura)", g.registrar_cliente,
               id_cliente="1075123456", nombre="laura gómez", email="laura@mail.com", telefono="3101234567")
    g.ejecutar("Registrar cliente con correo inválido", g.registrar_cliente,
               id_cliente="1075999888", nombre="Pedro Ruiz", email="pedro#mail", telefono="3201112233")
    g.ejecutar("Registrar cliente válido (Carlos)", g.registrar_cliente,
               id_cliente="79845612", nombre="Carlos Pérez", email="carlos@fj.co", telefono="3009876543")
    g.ejecutar("Registrar cliente duplicado", g.registrar_cliente,
               id_cliente="1075123456", nombre="Laura Otra", email="otra@mail.com", telefono="3101234567")
    g.ejecutar("Registrar cliente con datos incompletos (sin teléfono)", g.registrar_cliente,
               id_cliente="55512345", nombre="Ana Torres", email="ana@mail.com")

    # --- Servicios ---
    g.ejecutar("Crear sala de reuniones válida", g.crear_servicio, "sala",
               codigo="s01", nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=30)
    g.ejecutar("Crear servicio con tarifa negativa", g.crear_servicio, "equipo",
               codigo="E01", nombre="Video Beam", tarifa_hora=-100, deposito=20000)
    g.ejecutar("Crear asesoría con nivel inválido", g.crear_servicio, "asesoria",
               codigo="A01", nombre="Asesoría en Redes", tarifa_hora=80000, nivel="maestro")
    g.ejecutar("Crear asesoría válida", g.crear_servicio, "asesoria",
               codigo="A02", nombre="Asesoría en Redes", tarifa_hora=80000, nivel="Senior")
    g.ejecutar("Crear equipo válido", g.crear_servicio, "equipo",
               codigo="E02", nombre="Portátil Gamer", tarifa_hora=15000, deposito=50000)

    # --- Reservas ---
    g.ejecutar("Reserva exitosa de sala (3 h)", g.reservar, "1075123456", "S01", 3)
    g.ejecutar("Reserva con cliente inexistente", g.reservar, "000000000", "S01", 2)
    g.ejecutar("Reserva con duración inválida (30 h)", g.reservar, "79845612", "E02", 30)
    g.servicios["E02"].disponible = False
    g.ejecutar("Reserva de servicio no disponible", g.reservar, "79845612", "E02", 2)
    g.ejecutar("Reserva exitosa de asesoría con 10% descuento", g.reservar, "79845612", "A02", 2, 0.10)
    g.ejecutar("Cancelar reserva R001 (válida)", g.cancelar_reserva, "R001")
    g.ejecutar("Cancelar de nuevo R001 (estado inválido)", g.cancelar_reserva, "R001")
    g.ejecutar("Falla interna simulada (división por cero)", lambda: 1 / 0)
    g.ejecutar("Reserva posterior al error grave (el sistema sigue activo)", g.reservar, "1075123456", "A02", 1)

    # --- Resumen ---
    ok = sum(1 for _, _, e in g.resultados if e == "OK")
    ctrl = sum(1 for _, _, e in g.resultados if e == "ERROR CONTROLADO")
    inesp = sum(1 for _, _, e in g.resultados if e == "ERROR INESPERADO")
    print("=" * 70, f"\n RESUMEN: {len(g.resultados)} operaciones | {ok} exitosas | "
          f"{ctrl} errores controlados | {inesp} inesperados\n", "=" * 70, sep="")
    print("\nClientes:");  [print("  ", c) for c in g.clientes.values()]
    print("Servicios:");   [print("  ", s) for s in g.servicios.values()]
    print("Reservas:");    [print("  ", r) for r in g.reservas]
    print("\nEl programa terminó sin interrupciones. Detalle en logs/software_fj.log")


if __name__ == "__main__":
    main()
