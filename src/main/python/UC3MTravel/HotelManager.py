import json
import os
from datetime import datetime, timedelta
from .HotelManagementException import HotelManagementException
from .HotelReservation import HotelReservation
from .HotelStay import HotelStay
from pathlib import Path
JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/"


class HotelManager:
    def __init__(self):
        pass

    def validatecreditcard(self, x):
        """
        Valida la validez de una tarjeta de crédito utilizando el algoritmo de Luhn.
        Argumentos:
          x: El número de la tarjeta de crédito como cadena.
        Retorno:
          True si la tarjeta de crédito es válida, False si no.
        """

        # Comprobar si la cadena contiene solo dígitos
        if not x.isdigit():
            return False

        # Invertir el número
        reversed_number = x[::-1]

        # Lista para almacenar los dígitos duplicados
        doubled_digits = []

        # Duplicar dígitos pares
        for i, digit in enumerate(reversed_number):
            if i % 2 == 1:
                doubled_digits.append(int(digit) * 2)
            else:
                doubled_digits.append(int(digit))

        # Lista para almacenar los dígitos finales
        final_digits = []

        # Sumar dígitos
        for digit in doubled_digits:
            if digit <= 9:
                final_digits.append(digit)
            else:
                final_digits.append(digit - 9)

        sum_digits = sum(final_digits)

        # Validar el número
        return sum_digits % 10 == 0

    def validar_dni(self, dni):
        """
        Valida un número de DNI español.

        Args:
        - dni (str): Número de DNI a validar.

        Returns:
        - bool: True si el DNI es válido, False si no lo es.
        """
        tabla_letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni = dni.upper()
        if len(dni) != 9:
            return False
        try:
            numero = int(dni[:-1])
        except ValueError:
            return False
        letra = dni[-1]
        if tabla_letras[numero % 23] == letra:
            return True
        else:
            return False

    def room_reservation(self, creditcardNumb, nameAndSurname, idCard, phonenumber, roomType, arrivalDate, numDays):

        '''Gestiona la reserva de habitaciones del hotel.

            creditcardNumb (str): Número de tarjeta de crédito del cliente.
            nameAndSurname (str): Nombre y apellidos del cliente.
            idCard (str): DNI del cliente.
            phonenumber (str): Número de teléfono del cliente.
            roomType (str): Tipo de habitación (single, double, suite).
            arrivalDate (str): Fecha de llegada en formato dd/mm/yyyy.
            numDays (int): Número de días de estancia (entre 1 y 10).

            Devuelve:
                str: Localizador de la reserva en formato hexadecimal.

            Lanza:
                HotelManagementException: Si se produce algún error durante el proceso de reserva.
            '''
        file_store = JSON_FILES_PATH + "reservations.json"

        reserva = HotelReservation(creditcardNumb, nameAndSurname, idCard, phonenumber, roomType, arrivalDate,
                                   numDays)

        try:
            # Comprobamos si los datos son correctos
            if not self.validatecreditcard(creditcardNumb):
                raise HotelManagementException("Número de tarjeta de crédito inválido")

            if len(nameAndSurname.split()) < 2 or len(nameAndSurname) < 10 or len(nameAndSurname) > 50:
                raise HotelManagementException("La cadena del nombre y apellidos no es válida")

            if not self.validar_dni(idCard):
                raise HotelManagementException("DNI inválido")

            if not phonenumber.isdigit() or len(phonenumber) != 9:
                raise HotelManagementException("Número de teléfono inválido")

            if roomType not in ['single', 'double', 'suite']:
                raise HotelManagementException("Tipo de habitación inválido")

            # Verificar si num_days es una cadena vacía
            if isinstance(numDays, str) and not numDays.strip():
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            # Convertir num_days a entero si es una cadena
            try:
                numDays = int(numDays)
            except ValueError:
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            # Validar el rango de num_days
            if not 1 <= numDays <= 10:
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            try:
                # Convertir la cadena en un objeto datetime
                arrival_date_aux = arrivalDate
                arrivalDate = datetime.strptime(arrivalDate, "%d/%m/%Y")

                # Verificar que la fecha sea mayor que la fecha actual
                if arrivalDate <= datetime.now():
                    raise HotelManagementException("La fecha de llegada debe ser posterior a la fecha actual")

                # Verificar que el día esté entre 1 y 31 y el mes esté entre 1 y 12
                if not (1 <= arrivalDate.day <= 31 and 1 <= arrivalDate.month <= 12):
                    raise HotelManagementException("La fecha de llegada contiene un día o mes inválido")
            except ValueError:
                raise HotelManagementException("Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

            # Verificar si el archivo existe y no está vacío
            arrivalDate = arrival_date_aux
            if os.path.exists(file_store) and os.path.getsize(file_store) > 0:
                with open(file_store, "r") as file:
                    data = json.load(file)
            else:
                data = {"reservations": []}

            # Verificar si el cliente ya tiene una reserva
            for reservation in data["reservations"]:
                if reservation["id_card"] == idCard:
                    raise HotelManagementException("El cliente ya tiene una reserva")

            # Agregar el localizador a los datos de la reserva
            reservation_data = {
                "credit_card": creditcardNumb,
                "name_surname": nameAndSurname,
                "id_card": idCard,
                "phone_number": phonenumber,
                "room_type": roomType,
                "arrival_date": arrivalDate,
                "num_days": numDays,
                "localizer": reserva.LOCALIZER  # Agregar el localizador aquí
            }

            # Agregar la nueva reserva a los datos
            data["reservations"].append(reservation_data)

            # Almacenar los datos actualizados en el archivo JSON
            with open(file_store, "w") as file:
                json.dump(data, file, indent=4)

            return reserva.LOCALIZER
        except HotelManagementException as e:
            raise HotelManagementException("Error: " + str(e))

    def guest_arrival(self, inputFile):
        '''// El archivo de entrada es una cadena con la ruta del archivo
            descrita en HM-FR-02-I1
        // Devuelve un String en hexadecimal que representa el código de
            la habitación (clave que será necesaria para jhuHM-FR-02-O1)
        // En caso de error, devuelve un HotelManagementException
            representa HM-FR-02-O3'''

        try:
            # Abrir el archivo de entrada en modo lectura
            with open(inputFile, 'r') as file_input:
                try:
                    # Intentar cargar el contenido del archivo JSON
                    entrada = json.load(file_input)
                except json.JSONDecodeError:
                    # Capturar errores de decodificación JSON
                    raise HotelManagementException("El archivo no tiene formato JSON")

                # Verificar si el archivo JSON tiene los campos necesarios
                if len(entrada) != 2 or "Localizer" not in entrada or "IdCard" not in entrada:
                    raise HotelManagementException("El archivo no tiene formato JSON")

                # Extraer los datos relevantes del JSON
                try:
                    localizer_input = entrada["Localizer"]
                    dni_input = entrada["IdCard"]
                except json.JSONDecodeError:
                    raise HotelManagementException("El JSON no tiene la estructura esperada")

                # Validar el número de identificación del huésped
                dni = HotelManager()
                if not dni.validar_dni(dni_input):
                    raise HotelManagementException("Los datos del JSON no tienen valores válidos")

            # Verificar la longitud y tipo de los datos del JSON
            if not isinstance(localizer_input, str) or len(localizer_input) != 32:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")
            if not isinstance(dni_input, str) or len(dni_input) != 9:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")

            # Obtener la ruta del archivo de reservas
            file_path = JSON_FILES_PATH + "reservations.json"

            # Abrir el archivo de reservas en modo lectura
            with open(file_path, 'r') as file:
                data = json.load(file)
                numDays = False

                # Verificar si el localizador está presente en las reservas y coincide con los datos en el archivo
                for reservation in data["reservations"]:
                    if localizer_input == reservation["localizer"] and dni_input == reservation["id_card"]:
                        numDays = reservation["num_days"]
                        roomType = reservation["room_type"]
                        arrivalDay = reservation["arrival_date"]

                        # Calcular la fecha de salida
                        fecha_operable = datetime.strptime(arrivalDay, "%d/%m/%Y")
                        n_days = int(reservation["num_days"])
                        departure_day_operable = fecha_operable + timedelta(days=n_days)
                        departure_day = departure_day_operable.strftime("%d/%m/%Y")
                        break
                    else:
                        raise HotelManagementException(
                            "El localizador o el DNI introducido no se corresponde con los datos almacenados")

                # Comprobar si se encontraron datos de reserva válidos
                if not numDays:
                    raise HotelManagementException("Los datos del JSON no tienen valores válidos")

                try:
                    # Crear una instancia de HotelStay para la estancia del huésped
                    estancia = HotelStay(dni_input, localizer_input, numDays, roomType)
                    room_key = estancia.room_key
                except:
                    raise HotelManagementException("Error en el procesamiento interno al obtener la clave")

                # Verificar que la fecha de llegada coincide con la fecha actual
                if fecha_operable.date() != estancia.arrival:
                    raise HotelManagementException("La fecha de llegada no coincide con la fecha actual")

                # Comprobar si el archivo de estancias existe y tiene contenido
                file_path2 = JSON_FILES_PATH + "estancias.json"
                if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
                    with open(file_path2, "r") as file:
                        data = json.load(file)
                else:
                    data = {"estancias": []}

                # Crear los datos para el archivo del check-in y añadir la clave de la habitación
                datos_estancia = {
                    "alg": "SHA-256",
                    "typ": roomType,
                    "localizer": localizer_input,
                    "arrival": arrivalDay,
                    "departure": departure_day,
                    "room_key": room_key
                }
                data["estancias"].append(datos_estancia)

                # Guardar los datos actualizados en el archivo JSON
                with open(file_path2, "w") as file_out:
                    json.dump(data, file_out, indent=1)

        except FileNotFoundError:
            raise HotelManagementException("El archivo no existe")
        except HotelManagementException as e:
            raise e

        return room_key

    def guest_checkout(self, roomKey):
        """
        Registra la salida del cliente del hotel.

        Args:
            roomKey (str): Código de habitación en formato SHA256.

        Returns:
            True si la salida se ha realizado correctamente, False si no.

        Raises:
            HotelManagementException: Si se produce algún error durante el proceso.
        """

        try:
            # Verificar la exactitud del código de habitación recibido
            if not isinstance(roomKey, str) or len(roomKey) != 64:
                raise HotelManagementException("El código de habitación no es válido")

            file_path = JSON_FILES_PATH + "estancias.json"

            # Buscar el código de habitación en el archivo de estancias JSON
            if not os.path.exists(file_path) or os.path.getsize(file_path) < 20:
                raise HotelManagementException("El archivo de estancias no existe o está vacío")

            with open(file_path, "r") as file:
                data = json.load(file)
                estancia_encontrada = False

                for estancia in data["estancias"]:
                    if roomKey == estancia["room_key"]:
                        estancia_encontrada = True
                        fecha_salida = estancia["departure"]
                        break

                if not estancia_encontrada:
                    raise HotelManagementException("El código de habitación no está registrado")


            # Verificar la fecha prevista de salida
            fecha_actual = datetime.now().date()
            fecha_actual_str = fecha_actual.strftime("%d/%m/%Y")

            if fecha_actual_str != fecha_salida:
                raise HotelManagementException("La fecha de salida no coincide")


            salida_data = {
                "room_key": roomKey,
                "check_out_date": fecha_actual.strftime("%d/%m/%Y")
            }

            salida_file_path = JSON_FILES_PATH + "check_outs.json"
            if os.path.exists(salida_file_path) and os.path.getsize(salida_file_path) > 0:
                with open(salida_file_path, "r") as file:
                    check_out_data = json.load(file)
            else:
                check_out_data = {"check_outs": []}

            check_out_data["check_outs"].append(salida_data)

            with open(salida_file_path, "w") as file:
                json.dump(check_out_data, file, indent=4)

            return True

        except HotelManagementException as e:
            raise e


