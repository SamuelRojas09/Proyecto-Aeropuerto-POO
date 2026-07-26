"""Consultas y reportes sobre los pasajeros procesados por el sistema."""

from pathlib import Path
from collections import Counter


class SistemaConsultas:
    def __init__(self, aprobados: list, rechazados: list) -> None:
        self.aprobados = aprobados
        self.rechazados = rechazados

    # ── Listados básicos ───────────────────────────────────────

    def mostrar_aprobados(self) -> None:
        print("\nPASAJEROS APROBADOS")

        if not self.aprobados:
            print("  (ninguno)")
            return

        for i, (pasajero, equipaje) in enumerate(self.aprobados, 1):
            cargo = (
                f"  cargo: ${equipaje.cargo_adicional:,.0f}"
                if equipaje.cargo_adicional
                else ""
            )
            print(f"  {i}. {pasajero.nombre} → {pasajero.destino}{cargo}")

    def mostrar_rechazados(self) -> None:
        print("\nPASAJEROS RECHAZADOS")

        if not self.rechazados:
            print("  (ninguno)")
            return

        for i, (pasajero, motivo) in enumerate(self.rechazados, 1):
            print(f"  {i}. {pasajero.nombre}  |  Motivo: {motivo}")

    # ── Búsqueda ───────────────────────────────────────────────

    def buscar_pasajero(self) -> None:
        nombre = input("Nombre a buscar: ").strip().lower()

        for pasajero, equipaje in self.aprobados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_aprobado(pasajero, equipaje)
                return

        for pasajero, motivo in self.rechazados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_rechazado(pasajero, motivo)
                return

        print("  Pasajero no encontrado.")

    def _mostrar_ficha_aprobado(self, pasajero, equipaje) -> None:
        print("\n── FICHA PASAJERO (APROBADO) ──")
        print(f"  Nombre:       {pasajero.nombre}")
        print(f"  Edad:         {pasajero.edad} años")
        print(f"  Nacionalidad: {pasajero.nacionalidad}")
        print(f"  Destino:      {pasajero.destino}")
        print(f"  Teléfono:     {pasajero.telefono}")
        print(f"  Correo:       {pasajero.correo}")
        print(f"  Tipo sangre:  {pasajero.tipo_sangre}")
        print(
            f"  Maletas:      {equipaje.cantidad_maletas}  |  Peso: {equipaje.peso_total} kg"
        )
        print(f"  En bodega:    {'Sí' if equipaje.en_bodega else 'No'}")
        print(f"  Cargo extra:  ${equipaje.cargo_adicional:,.0f}")

    def _mostrar_ficha_rechazado(self, pasajero, motivo: str) -> None:
        print("\n── FICHA PASAJERO (RECHAZADO) ──")
        print(f"  Nombre:       {pasajero.nombre}")
        print(f"  Edad:         {pasajero.edad} años")
        print(f"  Nacionalidad: {pasajero.nacionalidad}")
        print(f"  Destino:      {pasajero.destino}")
        print(f"  Motivo:       {motivo}")

    # ── Filtros ────────────────────────────────────────────────

    def filtrar_por_destino(self) -> None:
        destino = input("Destino a filtrar: ").strip().lower()

        resultados = [
            pasajero
            for pasajero, _ in self.aprobados
            if pasajero.destino.lower() == destino
        ]

        print(f"\nPASAJEROS APROBADOS CON DESTINO: {destino.upper()}")

        if not resultados:
            print("  (ninguno)")
            return

        for i, pasajero in enumerate(resultados, 1):
            print(f"  {i}. {pasajero.nombre}")

    def filtrar_por_nacionalidad(self) -> None:
        nacionalidad = input("Nacionalidad a filtrar: ").strip().lower()

        aprobados = [
            p for p, _ in self.aprobados if p.nacionalidad.lower() == nacionalidad
        ]

        rechazados = [
            (p, m) for p, m in self.rechazados if p.nacionalidad.lower() == nacionalidad
        ]

        print(f"\nPASAJEROS DE NACIONALIDAD: {nacionalidad.upper()}")
        print(f"  Aprobados: {len(aprobados)}")

        for p in aprobados:
            print(f"    • {p.nombre} → {p.destino}")

        print(f"  Rechazados: {len(rechazados)}")

        for p, m in rechazados:
            print(f"    • {p.nombre}  ({m})")

    def filtrar_por_edad(self) -> None:
        print("Rango de edad:")
        try:
            edad_min = int(input("  Desde: "))
            edad_max = int(input("  Hasta: "))
        except ValueError:
            print("  Error, ingresa solo números enteros.")
            return

        resultados = [
            (pasajero, equipaje)
            for pasajero, equipaje in self.aprobados
            if edad_min <= pasajero.edad <= edad_max
        ]

        print(f"\nAPROBADOS ENTRE {edad_min} Y {edad_max} AÑOS")

        if not resultados:
            print("  (ninguno)")
            return

        for i, (p, _) in enumerate(resultados, 1):
            print(f"  {i}. {p.nombre}  ({p.edad} años) → {p.destino}")

    # ── Bodega ─────────────────────────────────────────────────

    def mostrar_bodega(self) -> None:
        en_bodega = [(p, e) for p, e in self.aprobados if e.en_bodega]

        print("\nEQUIPAJE EN BODEGA")

        if not en_bodega:
            print("  Ningún equipaje en bodega.")
            return

        total = 0

        for p, e in en_bodega:
            print(f"  • {p.nombre}  — ${e.cargo_adicional:,.0f}")
            total += e.cargo_adicional

        print(f"\n  Total recaudado por bodega: ${total:,.0f}")

    # ── Pasajeros sin cargo ────────────────────────────────────

    def mostrar_sin_cargo(self) -> None:
        sin_cargo = [p for p, e in self.aprobados if e.cargo_adicional == 0]

        print("\nPASAJEROS SIN CARGO ADICIONAL")

        if not sin_cargo:
            print("  (ninguno)")
            return

        for i, p in enumerate(sin_cargo, 1):
            print(f"  {i}. {p.nombre} → {p.destino}")

    # ── Estadísticas ───────────────────────────────────────────

    def mostrar_estadisticas(self) -> None:
        total = len(self.aprobados) + len(self.rechazados)
        dinero = sum(e.cargo_adicional for _, e in self.aprobados)
        en_bodega = sum(1 for _, e in self.aprobados if e.en_bodega)

        destinos = [p.destino for p, _ in self.aprobados]
        destino_top = Counter(destinos).most_common(1)

        mayor = max(self.aprobados, key=lambda x: x[1].cargo_adicional, default=None)

        motivos: Counter[str] = Counter()
        for _, m in self.rechazados:
            for linea in m.splitlines():
                linea = linea.strip()
                if linea.startswith("- "):
                    motivos[linea[2:]] += 1

        print("\n" + "═" * 45)
        print("  ESTADÍSTICAS")
        print("═" * 45)
        print(f"  Registrados:          {total}")
        print(f"  Aprobados:            {len(self.aprobados)}")
        print(f"  Rechazados:           {len(self.rechazados)}")

        if total > 0:
            pct = len(self.aprobados) / total * 100
            print(f"  Tasa de aprobación:   {pct:.1f}%")

        print(f"  En bodega:            {en_bodega}")
        print(f"  Dinero recaudado:     ${dinero:,.0f}")

        if destino_top:
            print(
                f"  Destino más popular:  {destino_top[0][0]} ({destino_top[0][1]} pax)"
            )

        if mayor and mayor[1].cargo_adicional > 0:
            print(
                f"  Mayor cargo:          "
                f"{mayor[0].nombre} (${mayor[1].cargo_adicional:,.0f})"
            )

        if motivos:
            print("\n  Motivos de rechazo:")
            for motivo, cantidad in motivos.most_common():
                print(f"    • {motivo}: {cantidad}")

        print("═" * 45)

    # ── Destinos frecuentes ────────────────────────────────────

    def mostrar_destinos(self) -> None:
        todos = [p.destino for p, _ in self.aprobados]
        conteo = Counter(todos).most_common()

        print("\nDESTINOS MÁS FRECUENTES")

        if not conteo:
            print("  (sin datos)")
            return

        for destino, cantidad in conteo:
            barra = "█" * cantidad
            print(f"  {destino:<20} {barra} {cantidad}")

    # ── Exportar reporte ───────────────────────────────────────

    def exportar_reporte(self) -> None:
        total = len(self.aprobados) + len(self.rechazados)
        dinero = sum(e.cargo_adicional for _, e in self.aprobados)

        lineas = [
            "=" * 60,
            "  REPORTE FINAL - SISTEMA AEROPUERTO",
            "=" * 60,
            "",
            f"Total registrados : {total}",
            f"Aprobados         : {len(self.aprobados)}",
            f"Rechazados        : {len(self.rechazados)}",
            f"Dinero recaudado  : ${dinero:,.0f}",
            "",
            "─" * 60,
            "PASAJEROS APROBADOS",
            "─" * 60,
        ]

        for i, (p, e) in enumerate(self.aprobados, 1):
            lineas.append(
                f"{i:>3}. {p.nombre:<25} → {p.destino:<20} "
                f"cargo: ${e.cargo_adicional:,.0f}"
            )

        lineas += ["", "─" * 60, "PASAJEROS RECHAZADOS", "─" * 60]

        for i, (p, m) in enumerate(self.rechazados, 1):
            lineas.append(f"{i:>3}. {p.nombre:<25}  motivo: {m}")

        lineas += ["", "=" * 60]

        # proyecto_aeropuerto/consultas/sistema_consultas.py
        #   -> parent        = consultas/
        #   -> parent.parent = proyecto_aeropuerto/
        # Así el reporte siempre cae en proyecto_aeropuerto/Reportes/,
        # sin importar desde qué carpeta se ejecute el programa.
        # El reporte debe quedar dentro de Reportes/Aeropuerto.
        carpeta_reportes = (
            Path(__file__).resolve().parent.parent / "Reportes" / "Aeropuerto"
        )
        carpeta_reportes.mkdir(parents=True, exist_ok=True)
        nombre_archivo = carpeta_reportes / "reporte_aeropuerto.txt"

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("\n".join(lineas))
        except OSError as error:
            print(f"\n  No se pudo exportar el reporte: {error}")
            return

        print(f"\n  ✔ Reporte exportado como '{nombre_archivo}'")
