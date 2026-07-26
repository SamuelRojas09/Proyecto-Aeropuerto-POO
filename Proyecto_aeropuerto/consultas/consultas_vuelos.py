"""Consultas sobre los vuelos registrados en la torre de control."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Ajusta esta ruta según donde termine viviendo la clase Vuelo
    # (por ejemplo: from ..modelos.vuelo import Vuelo)
    from ..modelos.vuelo import Vuelo  # type: ignore


class ConsultasVuelos:
    def __init__(self, vuelos: list["Vuelo"]) -> None:
        self.vuelos = vuelos

    def mostrar_todos(self) -> None:
        print("\nHISTORIAL DE VUELOS")
        if not self.vuelos:
            print("  (ningun vuelo registrado)")
            return
        for i, vuelo in enumerate(self.vuelos, 1):
            print(
                f"  {i}. [{vuelo.estado}] {vuelo.codigo} | "
                f"{vuelo.origen} -> {vuelo.destino} | {vuelo.cantidad_pasajeros} pax"
            )

    def mostrar_autorizados(self) -> None:
        print("\nVUELOS AUTORIZADOS")
        autorizados = [v for v in self.vuelos if v.estado == "Autorizado"]
        if not autorizados:
            print("  (ninguno)")
            return
        for i, vuelo in enumerate(autorizados, 1):
            nombre_piloto = (
                vuelo.piloto.nombre if vuelo.piloto is not None else "Sin asignar"
            )
            modelo_aeronave = (
                vuelo.aeronave.modelo if vuelo.aeronave is not None else "Sin asignar"
            )
            print(f"  {i}. {vuelo.codigo} | {vuelo.origen} -> {vuelo.destino}")
            print(f"     Piloto: {nombre_piloto} | Aeronave: {modelo_aeronave}")
            print(f"     Pasajeros: {vuelo.cantidad_pasajeros}")

    def mostrar_denegados(self) -> None:
        print("\nVUELOS DENEGADOS")
        denegados = [v for v in self.vuelos if v.estado == "Denegado"]
        if not denegados:
            print("  (ninguno)")
            return
        for i, vuelo in enumerate(denegados, 1):
            print(
                f"  {i}. {vuelo.codigo} | "
                f"{vuelo.origen} -> {vuelo.destino} | {vuelo.cantidad_pasajeros} pax"
            )

    def buscar_vuelo(self) -> None:
        codigo = input("Codigo de vuelo a buscar: ").strip().upper()
        for vuelo in self.vuelos:
            if vuelo.codigo.upper() == codigo:
                print("\n-- FICHA DE VUELO --")
                print(f"  Codigo:     {vuelo.codigo}")
                print(f"  Origen:     {vuelo.origen}")
                print(f"  Destino:    {vuelo.destino}")
                print(f"  Pasajeros:  {vuelo.cantidad_pasajeros}")
                print(f"  Estado:     {vuelo.estado}")
                if vuelo.piloto is not None:
                    print(f"  Piloto:     {vuelo.piloto.nombre}")
                    print(f"  Licencia:   {vuelo.piloto.licencia}")
                    print(f"  Horas:      {vuelo.piloto.horas_vuelo}")
                if vuelo.aeronave is not None:
                    print(f"  Aeronave:   {vuelo.aeronave.modelo}")
                    print(f"  Matricula:  {vuelo.aeronave.matricula}")
                    print(f"  Capacidad:  {vuelo.aeronave.capacidad}")
                return
        print("  Vuelo no encontrado.")

    def filtrar_por_destino(self) -> None:
        destino = input("Destino a filtrar: ").strip().lower()
        resultados = [v for v in self.vuelos if v.destino.lower() == destino]
        print(f"\nVUELOS CON DESTINO: {destino.upper()}")
        if not resultados:
            print("  (ninguno)")
            return
        for i, v in enumerate(resultados, 1):
            print(f"  {i}. [{v.estado}] {v.codigo} - {v.cantidad_pasajeros} pax")

    def mostrar_estadisticas(self) -> None:
        total = len(self.vuelos)
        autorizados = len([v for v in self.vuelos if v.estado == "Autorizado"])
        denegados = len([v for v in self.vuelos if v.estado == "Denegado"])
        pendientes = len([v for v in self.vuelos if v.estado == "Pendiente"])
        total_pasajeros = sum(
            v.cantidad_pasajeros for v in self.vuelos if v.estado == "Autorizado"
        )
        destinos = [v.destino for v in self.vuelos if v.estado == "Autorizado"]
        destino_top = Counter(destinos).most_common(1)
        print("\n" + "=" * 45)
        print("  ESTADISTICAS DE VUELOS")
        print("=" * 45)
        print(f"  Total vuelos:       {total}")
        print(f"  Autorizados:        {autorizados}")
        print(f"  Denegados:          {denegados}")
        print(f"  Pendientes:         {pendientes}")
        if total > 0:
            pct = autorizados / total * 100
            print(f"  Tasa autorizacion:  {pct:.1f}%")
        print(f"  Pasajeros en vuelo: {total_pasajeros}")
        if destino_top:
            print(
                f"  Destino popular:    {destino_top[0][0]} ({destino_top[0][1]} vuelos)"
            )
        print("=" * 45)
