from ..Consola import Consola
from ..validaciones import ControladorAereo
from ..modelos import (
    Piloto,
    Vuelo,
    Aeronave,
    SolicitudDespegue,
)

from pathlib import Path
import queue


class ColaPrioridadVuelos:
    def __init__(self) -> None:
        self._cola: "queue.PriorityQueue" = queue.PriorityQueue()
        self._contador = (
            0  # Desempata solicitudes con la misma prioridad (orden de llegada)
        )

    def encolar(self, solicitud: SolicitudDespegue, prioridad: int) -> None:
        # Prioridad menor = se atiende primero (1=emergencia, 5=normal)
        self._contador += 1
        self._cola.put((prioridad, self._contador, solicitud))
        print(
            f"  Vuelo {solicitud.vuelo.codigo} encolado con prioridad {prioridad} "
            f"(1=emergencia, 5=normal)."
        )

    def siguiente(self) -> SolicitudDespegue | None:
        if self._cola.empty():
            return None
        _, _, solicitud = self._cola.get()
        return solicitud

    def esta_vacia(self) -> bool:
        return self._cola.empty()


class SistemaTorreControl(Consola):
    def __init__(self, pasajeros_aprobados: list[tuple]) -> None:
        self.pasajeros_aprobados = pasajeros_aprobados
        self.vuelos: list[Vuelo] = []
        self.controlador = ControladorAereo()
        self.cola_prioridad = ColaPrioridadVuelos()

    def _codigo_vuelo_repetido(self, codigo: str) -> bool:
        codigo_normalizado = codigo.strip().upper()
        return any(vuelo.codigo.upper() == codigo_normalizado for vuelo in self.vuelos)

    def _matricula_repetida(self, matricula: str) -> bool:
        matricula_normalizada = matricula.strip().upper()
        return any(
            vuelo.aeronave is not None
            and vuelo.aeronave.matricula.upper() == matricula_normalizada
            for vuelo in self.vuelos
        )

    def registrar_vuelo(self) -> None:
        print("\n" + "=" * 60)
        print("  REGISTRO DE VUELO")
        print("=" * 60)

        cantidad_pasajeros = len(self.pasajeros_aprobados)
        print(f"\n  Pasajeros aprobados del sistema: {cantidad_pasajeros}")

        print("\nDATOS DEL VUELO")
        while True:
            codigo = self._leer_texto_no_vacio("Codigo del vuelo: ").upper()
            if not self._codigo_vuelo_repetido(codigo):
                break
            print("  Error, ya existe un vuelo con ese codigo")

        origen = self._leer_texto_no_vacio("Origen: ")
        destino = self._leer_texto_no_vacio("Destino: ")

        print("\nDATOS DEL PILOTO")
        nombre_piloto = self._leer_texto_no_vacio("Nombre: ")
        licencia = self._leer_texto_no_vacio("Licencia: ")
        horas_vuelo = self._leer_entero_positivo("Horas de vuelo (500 horas mínimas): ")
        piloto_disponible = self._leer_booleano("Disponible? (s/n): ")

        print("\nDATOS DE LA AERONAVE")
        while True:
            matricula = self._leer_texto_no_vacio("Matricula: ").upper()
            if not self._matricula_repetida(matricula):
                break
            print("  Error, ya existe una aeronave registrada con esa matricula")

        modelo = self._leer_texto_no_vacio("Modelo: ")
        capacidad = self._leer_entero_positivo("Capacidad maxima: ")
        aeronave_disponible = self._leer_booleano("Disponible? (s/n): ")

        print("\nCONDICIONES")
        clima_favorable = self._leer_booleano("Clima favorable? (s/n): ")
        pista_libre = self._leer_booleano("Pista libre? (s/n): ")
        combustible_suficiente = self._leer_booleano("Combustible suficiente? (s/n): ")

        print("\nPRIORIDAD")
        prioridad = self._leer_prioridad()
        piloto = Piloto(nombre_piloto, licencia, horas_vuelo, piloto_disponible)
        aeronave = Aeronave(matricula, modelo, capacidad, aeronave_disponible)
        vuelo = Vuelo(codigo, origen, destino, cantidad_pasajeros)

        solicitud = SolicitudDespegue(
            vuelo,
            piloto,
            aeronave,
            clima_favorable,
            pista_libre,
            combustible_suficiente,
        )
        self.cola_prioridad.encolar(solicitud, prioridad)
        self.vuelos.append(vuelo)

    def procesar_cola_despegues(self) -> None:
        if self.cola_prioridad.esta_vacia():
            print("\n  No hay vuelos pendientes en la cola de prioridad.")
            return

        print("\n" + "=" * 60)
        print("  PROCESANDO COLA DE DESPEGUES POR PRIORIDAD")
        print("=" * 60)

        while not self.cola_prioridad.esta_vacia():
            solicitud = self.cola_prioridad.siguiente()
            if solicitud is None:
                break

            autorizado, motivos = self.controlador.autorizar_despegue(
                solicitud.vuelo,
                solicitud.piloto,
                solicitud.aeronave,
                solicitud.clima_favorable,
                solicitud.pista_libre,
                solicitud.combustible_suficiente,
            )

            print("\n" + "-" * 60)
            if autorizado:
                print("  DESPEGUE AUTORIZADO")
                print(
                    f"  Vuelo {solicitud.vuelo.codigo}: "
                    f"{solicitud.vuelo.origen} -> {solicitud.vuelo.destino}"
                )
                print(f"  Pasajeros a bordo: {solicitud.vuelo.cantidad_pasajeros}")
            else:
                print("  DESPEGUE DENEGADO")
                print("  Motivos:")
                for motivo in motivos:
                    print(f"    - {motivo}")
            print("-" * 60)

    def exportar_reporte(self) -> None:
        autorizados = [v for v in self.vuelos if v.estado == "Autorizado"]
        denegados = [v for v in self.vuelos if v.estado == "Denegado"]

        lineas = [
            "=" * 60,
            "  REPORTE TORRE DE CONTROL",
            "=" * 60,
            "",
            f"Total vuelos registrados : {len(self.vuelos)}",
            f"Autorizados              : {len(autorizados)}",
            f"Denegados                : {len(denegados)}",
            "",
            "-" * 60,
            "VUELOS AUTORIZADOS",
            "-" * 60,
        ]

        for i, v in enumerate(autorizados, 1):
            nombre_piloto = v.piloto.nombre if v.piloto is not None else "Sin asignar"
            lineas.append(
                f"{i:>3}. {v.codigo:<10} {v.origen:<15} -> {v.destino:<15} "
                f"| {v.cantidad_pasajeros} pax | Piloto: {nombre_piloto}"
            )

        lineas += ["", "-" * 60, "VUELOS DENEGADOS", "-" * 60]

        for i, v in enumerate(denegados, 1):
            lineas.append(
                f"{i:>3}. {v.codigo:<10} {v.origen:<15} -> {v.destino:<15} "
                f"| {v.cantidad_pasajeros} pax"
            )

        lineas += ["", "=" * 60]

        # sistema_torre_control.py está en Proyecto_aeropuerto/Sistemas/
        #   -> parent        = Sistemas/
        #   -> parent.parent = Proyecto_aeropuerto/
        # Así el reporte siempre cae en Proyecto_aeropuerto/Reportes/,
        # sin importar desde qué carpeta se ejecute el programa.
        carpeta_reportes = (
            Path(__file__).resolve().parent.parent / "Reportes" / "TorreControl"
        )
        carpeta_reportes.mkdir(parents=True, exist_ok=True)
        nombre_archivo = carpeta_reportes / "reporte_torre_control.txt"

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("\n".join(lineas))
        except OSError as error:
            print(f"\n  No se pudo exportar el reporte: {error}")
            return

        print(f"\n  Reporte exportado como '{nombre_archivo}'")
