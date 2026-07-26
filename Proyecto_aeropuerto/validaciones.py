from .modelos import Pasajero, Documento, Equipaje, Piloto, Vuelo, Aeronave


# ── Validación ─────────────────────────────────────────────────
# Esta clase se encarga de validar la información de un pasajero, sus documentos y su equipaje.
# Si el pasajero es aprobado, también calcula los cargos adicionales por exceso de equipaje o dimensiones fuera de los límites permitidos.
class ValidadorPasajero:
    PAISES_CON_VISA = ["canada", "estados unidos", "australia", "reino unido"]

    def validar_pasajero(
        self,
        pasajero: Pasajero,
        documento: Documento,
        equipaje: Equipaje,
    ) -> tuple[bool, list[str]]:

        motivos_rechazo: list[str] = []

        if pasajero.edad < 18:
            motivos_rechazo.append("Menor de edad")

        if not documento.pasaporte_vigente:
            motivos_rechazo.append("Pasaporte vencido")

        if pasajero.destino.lower() in self.PAISES_CON_VISA:
            if not documento.tiene_visa:
                motivos_rechazo.append("El destino requiere visa")
            if not documento.visa_vigente:
                motivos_rechazo.append("Visa vencida")

        if not documento.check_in_realizado:
            motivos_rechazo.append("No realizo check-in")

        if not documento.boleto_valido:
            motivos_rechazo.append("Boleto invalido")

        if equipaje.armas:
            motivos_rechazo.append("Transporta armas")

        if equipaje.material_inflamable:
            motivos_rechazo.append("Material inflamable")

        if equipaje.elementos_peligrosos:
            motivos_rechazo.append("Elementos peligrosos")

        self.validar_equipaje(equipaje)

        if motivos_rechazo:
            return False, motivos_rechazo

        return True, ["Aprobado"]

    def validar_equipaje(self, equipaje: Equipaje) -> None:

        if equipaje.cantidad_maletas < 1:
            return

        if equipaje.cantidad_maletas > 3:
            exceso = equipaje.cantidad_maletas - 3
            equipaje.cargo_adicional += exceso * 50000.0
            equipaje.en_bodega = True

        if equipaje.peso_total > 23.0:
            equipaje.cargo_adicional += (equipaje.peso_total - 23.0) * 10000.0
            equipaje.en_bodega = True

        for i, maleta in enumerate(equipaje.maletas, 1):
            if maleta["largo"] > 55 or maleta["ancho"] > 40 or maleta["alto"] > 25:
                equipaje.cargo_adicional += 50000.0
                equipaje.en_bodega = True
                print(f"  Maleta {i}: dimensiones exceden el limite, cargo $50.000")


class ControladorAereo:
    HORAS_MINIMAS = 500

    def verificar_piloto(self, piloto: Piloto) -> tuple[bool, str]:
        if not piloto.disponible:
            return False, "Piloto no disponible"
        if piloto.horas_vuelo < self.HORAS_MINIMAS:
            return False, f"Pocas horas de experiencia (minimo {self.HORAS_MINIMAS})"
        return True, "Piloto aprobado"

    def verificar_aeronave(self, aeronave: Aeronave) -> tuple[bool, str]:
        if not aeronave.disponible:
            return False, "Aeronave no disponible"
        return True, "Aeronave aprobada"

    def verificar_capacidad(self, vuelo: Vuelo, aeronave: Aeronave) -> tuple[bool, str]:
        if vuelo.cantidad_pasajeros > aeronave.capacidad:
            return (
                False,
                f"Capacidad excedida ({vuelo.cantidad_pasajeros} pax / capacidad {aeronave.capacidad})",
            )
        return True, "Capacidad aprobada"

    def verificar_clima(self, clima_favorable: bool) -> tuple[bool, str]:
        if not clima_favorable:
            return False, "Clima desfavorable"
        return True, "Clima favorable"

    def verificar_pista(self, pista_libre: bool) -> tuple[bool, str]:
        if not pista_libre:
            return False, "Pista ocupada"
        return True, "Pista libre"

    def verificar_combustible(self, combustible_suficiente: bool) -> tuple[bool, str]:
        if not combustible_suficiente:
            return False, "Combustible insuficiente"
        return True, "Combustible OK"

    def autorizar_despegue(
        self,
        vuelo: Vuelo,
        piloto: Piloto,
        aeronave: Aeronave,
        clima_favorable: bool,
        pista_libre: bool,
        combustible_suficiente: bool,
    ) -> tuple[bool, list[str]]:
        print("\n" + "=" * 60)
        print("  VERIFICACIONES DE CONTROL AEREO")
        print("=" * 60)

        motivos_rechazo: list[str] = []

        valido, mensaje = self.verificar_piloto(piloto)
        print(f"  Piloto:       {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_aeronave(aeronave)
        print(f"  Aeronave:     {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_capacidad(vuelo, aeronave)
        print(f"  Capacidad:    {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_clima(clima_favorable)
        print(f"  Clima:        {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_pista(pista_libre)
        print(f"  Pista:        {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_combustible(combustible_suficiente)
        print(f"  Combustible:  {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        if len(motivos_rechazo) == 0:
            vuelo.estado = "Autorizado"
            vuelo.piloto = piloto
            vuelo.aeronave = aeronave
            return True, []

        vuelo.estado = "Denegado"
        return False, motivos_rechazo
