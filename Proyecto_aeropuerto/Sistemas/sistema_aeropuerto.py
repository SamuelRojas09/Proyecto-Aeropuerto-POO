from ..modelos import Pasajero, Documento, Equipaje
from ..validaciones import ValidadorPasajero
from ..Consola import Consola


# Esta clase representa el sistema de control de pasajeros en un aeropuerto.
# Permite registrar pasajeros, validar sus documentos y equipaje.
# Generando un reporte final indicando los pasajeros aprobados y rechazados.
class SistemaAeropuerto:
    # ──────Validación de datos de entrada del usuario────────────────────────
    # Validar nombre (solo letras, espacios, apóstrofes y guiones)
    NOMBRE_REGLA = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s'-]+$"

    # Validar nacionalidad y destino (solo letras y espacios)
    TEXTO_REGLA = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$"

    # Validar tipo de sangre (solo opciones válidas)
    TIPO_SANGRE_REGLA = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    # Validar teléfono (solo números y espacios, puede iniciar con +)
    TELEFONO_REGLA = r"^\+?[0-9\s]+$"

    # Validar correo (solo direcciones de correo válidas)
    CORREO_REGLA = [
        "unal.edu.co",
        "gmail.com",
        "hotmail.com",
        "icloud.com",
        "outlook.com",
        "yahoo.com",
        "protonmail.com",
    ]

    # Validar pasaporte (solo letras y números)
    PASAPORTE_REGLA = r"^[a-zA-Z0-9]+$"

    def __init__(self) -> None:

        self.aprobados: list[
            tuple[Pasajero, Equipaje]
        ] = []  # Lista de pasajeros aprobados
        self.rechazados: list[
            tuple[Pasajero, str]
        ] = []  # Lista de pasajeros rechazados

        self.consola = Consola()
        self.validador = ValidadorPasajero()

    def registrar_pasajero(self) -> None:
        while True:
            cantidad = self.consola._leer_entero(
                "¿Cuántos pasajeros desea registrar?: "
            )
            if cantidad >= 0:
                break
            print("Número invalido, digite nuevamente un número no negativo, por favor")
        if cantidad > 0:
            # Sirve para registrar la información de los pasajeros, dependiendo de la cantidad que el usuario ingrese
            # Se ejecutará un ciclo que solicitará los datos de cada pasajero.
            for _ in range(cantidad):
                print("\n" + "=" * 60)
                print(
                    f"REGISTRO DE PASAJERO N° {len(self.aprobados) + len(self.rechazados) + 1}"
                )
                print("=" * 60)

                nombre = self.consola._validacion("Nombre: ", self.NOMBRE_REGLA)
                while True:
                    edad = self.consola._leer_entero("Edad: ")
                    if edad >= 0:
                        break
                    print("Error, la edad no puede ser negativa.")

                nacionalidad = self.consola._validacion(
                    "Nacionalidad: ", self.TEXTO_REGLA
                )
                tipo_sangre = self.consola._validacion(
                    "Tipo de sangre: ", self.TIPO_SANGRE_REGLA
                )
                telefono = self.consola._validacion("Teléfono: ", self.TELEFONO_REGLA)

                correo = self.consola._leer_texto("Correo: ")
                # Verifica si el correo ingresado cumple con las condiciones de validación.
                while True:
                    # Se eliminan los espacios en blanco al inicio y al final del correo ingresado
                    # Se pasa todo a minuscula usando lower()
                    correo_limpio = correo.strip().lower()
                    count_arroba = correo_limpio.count(
                        "@"
                    )  # Se cuenta la cantidad de veces que aparece el símbolo "@" en el correo ingresado por el usuario.

                    # No cumple si el correo está vacío, contiene espacios o tiene más de un símbolo "@".
                    if (
                        (correo_limpio == "")
                        or (" " in correo_limpio)
                        or (count_arroba != 1)
                    ):
                        print("Error, digite correctamente su correo, por favor")
                        correo = self.consola._leer_texto("Correo: ")
                        continue

                    # Se divide el correo en dos partes: la parte del usuario y el dominio, utilizando el símbolo "@" como separador.
                    parte_usuario, dominio = correo_limpio.split("@", 1)
                    # No cumple si la parte del usuario está vacía.
                    if parte_usuario == "":
                        print("Error, digite correctamente su correo, por favor")
                        correo = self.consola._leer_texto("Correo: ")
                        continue

                    # No cumple si el dominio no está en la lista de dominios permitidos.
                    if dominio not in self.CORREO_REGLA:
                        print("Error, digite correctamente su correo, por favor")
                        correo = self.consola._leer_texto("Correo: ")
                    else:
                        correo = correo_limpio
                        break

                destino = self.consola._validacion("Destino: ", self.TEXTO_REGLA)

                print("\nDOCUMENTOS")

                numero_pasaporte = self.consola._validacion(
                    "Pasaporte: ", self.PASAPORTE_REGLA
                )
                pasaporte_vigente = self.consola._leer_booleano(
                    "¿Pasaporte vigente? (s/n): "
                )
                tiene_visa = self.consola._leer_booleano("¿Tiene visa? (s/n): ")
                visa_vigente = self.consola._leer_booleano("¿Visa vigente? (s/n): ")
                check_in_realizado = self.consola._leer_booleano(
                    "¿Check-in realizado? (s/n): "
                )
                boleto_valido = self.consola._leer_booleano("¿Boleto válido? (s/n): ")

                print("\nEQUIPAJE")

                while True:
                    cantidad_maletas = self.consola._leer_entero(
                        "Cantidad de maletas: "
                    )
                    if cantidad_maletas >= 0:
                        break
                    print("Error, la cantidad de maletas no puede ser negativa.")

                peso_total = 0.0
                largo = 0.0
                ancho = 0.0
                alto = 0.0

                preguntas_objetos_no_permitidos = (
                    ("elementos_peligrosos", "¿Elementos peligrosos? (s/n): "),
                    ("material_inflamable", "¿Material inflamable? (s/n): "),
                    ("armas", "¿Armas? (s/n): "),
                )

                def leer_objetos_no_permitidos() -> dict:
                    return {
                        clave: self.consola._leer_booleano(pregunta)
                        for clave, pregunta in preguntas_objetos_no_permitidos
                    }

                if cantidad_maletas > 0:
                    peso_total = 0.0
                    largo = 0.0
                    ancho = 0.0
                    alto = 0.0
                    maletas = []

                    for i in range(1, cantidad_maletas + 1):
                        print(f"\n  Maleta {i} de {cantidad_maletas}:")
                        peso = self.consola._leer_decimal_positivo("  Peso (kg): ")
                        largo = self.consola._leer_decimal_positivo("  Largo (cm): ")
                        ancho = self.consola._leer_decimal_positivo("  Ancho (cm): ")
                        alto = self.consola._leer_decimal_positivo("  Alto (cm): ")
                        peso_total += peso
                        maletas.append(
                            {"largo": largo, "ancho": ancho, "alto": alto, "peso": peso}
                        )

                objetos_no_permitidos = leer_objetos_no_permitidos()

                # Este bloque de código crea instancias de las clases Pasajero, Documento y Equipaje utilizando los datos ingresados por el usuario.
                # Luego, se llama al método validar_pasajero del validador para verificar si el pasajero cumple con los requisitos necesarios.
                # Dependiendo del resultado de la validación, se agrega el pasajero a la lista de aprobados o rechazados, y se muestra un mensaje correspondiente en la consola.

                pasajero = Pasajero(
                    nombre, edad, nacionalidad, tipo_sangre, telefono, correo, destino
                )

                documento = Documento(
                    numero_pasaporte,
                    pasaporte_vigente,
                    tiene_visa,
                    visa_vigente,
                    check_in_realizado,
                    boleto_valido,
                )

                equipaje = Equipaje(
                    cantidad_maletas,
                    peso_total,
                    largo,
                    ancho,
                    alto,
                    **objetos_no_permitidos,
                    maletas=maletas if cantidad_maletas > 0 else [],
                )

                aprobado, motivo = self.validador.validar_pasajero(
                    pasajero, documento, equipaje
                )

                if aprobado:
                    # Agrega el pasajero a la lista de aprobados
                    self.aprobados.append((pasajero, equipaje))

                    print("\n PASAJERO APROBADO")

                    if equipaje.en_bodega:
                        print("Equipaje enviado a bodega.")
                        print(f"Cargo adicional: ${equipaje.cargo_adicional:,.0f}")

                else:
                    # Agrega el pasajero a la lista de rechazados junto con los motivos del rechazo
                    motivos_formateados = "\n- " + "\n- ".join(motivo)
                    self.rechazados.append((pasajero, motivos_formateados))

                    print("\n PASAJERO RECHAZADO")
                    print("Motivos de rechazo:", motivos_formateados)
        if cantidad == 0:
            print("\nNo hay clientes que registrar")

    def mostrar_reporte(self) -> None:

        print("\n" + "=" * 60)
        print("REPORTE FINAL")
        print("=" * 60)

        if self.aprobados:
            print("\nPASAJEROS APROBADOS")
            # Muestra la lista de pasajeros aprobados junto con el cargo adicional por equipaje, si corresponde.
            for indice, dato in enumerate(self.aprobados, start=1):
                pasajero = dato[0]
                equipaje = dato[1]

                print(
                    f"""{indice}. {pasajero.nombre} - {pasajero.destino} | Cargo: $ {equipaje.cargo_adicional:,.0f}"""
                )
        if self.rechazados:
            print("\n PASAJEROS RECHAZADOS")
            # Muestra la lista de pasajeros rechazados junto con el motivo del rechazo.
            for indice, (pasajero, motivos) in enumerate(self.rechazados, start=1):
                print(
                    f"""{indice}. {pasajero.nombre} - {pasajero.destino} \n Motivos: {motivos}"""
                )
