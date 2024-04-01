import json
import os
from datetime import datetime, timedelta
from HotelManagementException import HotelManagementException
from HotelReservation import HotelReservation
from HotelStay import HotelStay
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

    def room_reservation(self, creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days):

        file_store = JSON_FILES_PATH + "reservations.json"

        reserva = HotelReservation(creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date,
                                   num_days)

        try:
            # Comprobamos si los datos son correctos
            if not self.validatecreditcard(creditcardNumb):
                raise HotelManagementException("Número de tarjeta de crédito inválido")

            if len(nAMeAndSURNAME.split()) < 2 or len(nAMeAndSURNAME) < 10 or len(nAMeAndSURNAME) > 50:
                raise HotelManagementException("La cadena del nombre y apellidos no es válida")

            if not self.validar_dni(IDCARD):
                raise HotelManagementException("DNI inválido")

            if not phonenumber.isdigit() or len(phonenumber) != 9:
                raise HotelManagementException("Número de teléfono inválido")

            if room_type not in ['single', 'double', 'suite']:
                raise HotelManagementException("Tipo de habitación inválido")

            # Verificar si num_days es una cadena vacía
            if isinstance(num_days, str) and not num_days.strip():
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            # Convertir num_days a entero si es una cadena
            try:
                num_days = int(num_days)
            except ValueError:
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            # Validar el rango de num_days
            if not 1 <= num_days <= 10:
                raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

            try:
                # Convertir la cadena en un objeto datetime
                arrival_date_aux = arrival_date
                arrival_date = datetime.strptime(arrival_date, "%d/%m/%Y")

                # Verificar que la fecha sea mayor que la fecha actual
                if arrival_date <= datetime.now():
                    raise HotelManagementException("La fecha de llegada debe ser posterior a la fecha actual")

                # Verificar que el día esté entre 1 y 31 y el mes esté entre 1 y 12
                if not (1 <= arrival_date.day <= 31 and 1 <= arrival_date.month <= 12):
                    raise HotelManagementException("La fecha de llegada contiene un día o mes inválido")
            except ValueError:
                raise HotelManagementException("Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

            # Verificar si el archivo existe y no está vacío
            arrival_date = arrival_date_aux
            if os.path.exists(file_store) and os.path.getsize(file_store) > 0:
                with open(file_store, "r") as file:
                    data = json.load(file)
            else:
                data = {"reservations": []}

            # Verificar si el cliente ya tiene una reserva
            for reservation in data["reservations"]:
                if reservation["id_card"] == IDCARD:
                    raise HotelManagementException("El cliente ya tiene una reserva")

            # Agregar el localizador a los datos de la reserva
            reservation_data = {
                "credit_card": creditcardNumb,
                "name_surname": nAMeAndSURNAME,
                "id_card": IDCARD,
                "phone_number": phonenumber,
                "room_type": room_type,
                "arrival_date": arrival_date,
                "num_days": num_days,
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

    def guest_arrival(self, input_file):
        '''// El archivo de entrada es una cadena con la ruta del archivo
            descrita en HM-FR-02-I1
        // Devuelve un String en hexadecimal que representa el código de
            la habitación (clave que será necesaria para jhuHM-FR-02-O1)
        // En caso de error, devuelve un HotelManagementException
            representa HM-FR-02-O3'''

        try:

            with open(input_file, 'r') as file_input:
                try:
                    entrada = json.load(file_input)

                except json.JSONDecodeError:
                    raise HotelManagementException("El archivo no tiene formato JSON")

                if len(entrada) != 2 or "Localizer" not in entrada or "IdCard" not in entrada:
                    raise HotelManagementException("El archivo no tiene formato JSON")

                try:
                    localizer_input = entrada["Localizer"]
                    dni_input = entrada["IdCard"]
                except json.JSONDecodeError:
                    raise HotelManagementException("El JSON no tiene la estructura esperada")

                dni = HotelManager()
                if not dni.validar_dni(dni_input):
                    raise HotelManagementException("Los datos del JSON no tienen valores válidos")

            if not isinstance(localizer_input, str) or len(localizer_input) != 32:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")

            if not isinstance(dni_input, str) or len(dni_input) != 9:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")

            jsonFilesDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'JsonFiles'))
            if not os.path.exists(jsonFilesDir):
                os.makedirs(jsonFilesDir)

            # Comprobamos si el fichero tiene contenido, en caso contrario lo creamos
            file_path = os.path.join(jsonFilesDir, "reservations.json")

            with open(file_path, 'r') as file:
                data = json.load(file)
                numDays = False

                # Verificar que el localizador está almacenado en el archivo de reservas (simulado)
                # y que coincide con los datos en el archivo

                for reservation in data["reservations"]:
                    if localizer_input == reservation["localizer"] and dni_input == reservation["id_card"]:
                        numDays = reservation["num_days"]
                        roomType = reservation["room_type"]
                        arrivalDay = reservation["arrival_date"]

                        fecha_operable = datetime.strptime(arrivalDay, "%d/%m/%Y")
                        n_days = int(reservation["num_days"])
                        departure_day_operable = fecha_operable + timedelta(days=n_days)
                        departure_day = departure_day_operable.strftime("%d/%m/%Y")
                        break
                    else:
                        raise HotelManagementException(
                            "El localizador y el dni introducido no se corresponde con los datos almacenados")

                if not numDays:
                    raise HotelManagementException("Los datos del JSON no tienen valores válidos")

                try:
                    estancia = HotelStay(dni_input, localizer_input, numDays, roomType)
                    room_key = estancia.room_key

                except:
                    raise HotelManagementException("Error en el procesamiento interno al obtener la clave")

                # Verificar que la fecha de llegada coincide con la fecha actual (sin tener en cuenta las horas y
                # minutos)

                # Convertir la fecha de llegada del archivo JSON a un objeto datetime

                if fecha_operable.date() != estancia.arrival:
                    print(fecha_operable.date(), estancia.arrival)
                    raise HotelManagementException("La fecha de llegada no coincide con la fecha actual")

                # Comprobamos si el fichero tiene contenido, en caso contrario lo creamos
                file_path2 = os.path.join(jsonFilesDir, "estancias.json")

                if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
                    with open(file_path2, "r") as file:
                        data = json.load(file)
                else:
                    data = {"estancias": []}

                # Creamos los datos que va a tener el archivo del check-in,
                # e incorporamos el room_key para la función 3

                datos_estancia = {
                    "alg": "SHA-256",
                    "typ": roomType,
                    "localizer": localizer_input,
                    "arrival": arrivalDay,
                    "departure": departure_day,
                    "room_key": room_key
                    }
                data["estancias"].append(datos_estancia)

                # Almacenar los datos actualizados en el archivo JSON
                with open(file_path2, "w") as file_out:
                    json.dump(data, file_out, indent=1)

        except FileNotFoundError:
            raise HotelManagementException("El archivo no existe")

        except HotelManagementException as e:
            raise e

        return room_key

    def guest_checkout(self, room_key):
        try:
            # Verificar si el código de habitación es un número hexadecimal válido
            if not isinstance(room_key, str) or len(room_key) != 64 or not all(
                    c in "0123456789abcdefABCDEF" for c in room_key):
                raise HotelManagementException("La cadena no contiene un código de habitación válido")

            # Leer la información de las estancias desde el archivo
            with open("../../../JsonFiles/reservations.json", "r") as file:
                estancias = json.load(file)

            # Verificar si el código de habitación existe en las estancias registradas
            if room_key not in estancias:
                raise HotelManagementException("El código de habitación no estaba registrado")

            # Obtener la fecha de salida prevista de la estancia
            fecha_salida_prevista = datetime.strptime(estancias[room_key]["departure"], "%Y-%m-%dT%H:%M:%S.%fZ")

            # Obtener la fecha y hora actual
            fecha_salida_actual = datetime.now().date()

            # Comprobar si la fecha actual coincide con la fecha de salida prevista
            if fecha_salida_prevista != fecha_salida_actual:
                raise HotelManagementException("La fecha de salida no es válida")

            # Registrar la salida en el archivo de salidas
            with open("salidas.txt", "a") as file:
                file.write(
                    f"Fecha de salida: {fecha_salida_actual.strftime('%Y-%m-%d %H:%M:%S')} UTC, Código de habitación: {room_key}\n")

            return True

        except HotelManagementException as e:
            raise e
        except Exception as e:
            raise HotelManagementException("Error de procesamiento interno al procesar el código: " + str(e))


# Ejemplo de uso:
try:

    localizador = HotelManager().room_reservation("5256783371569576", "Lola Montero", "12345678Z", "123456781",
                                                  "single",
                                                  "13/12/2024", 5)
    print("Localizador de reserva:", localizador)

except HotelManagementException as e:
    print("Error al realizar la reserva:", e)

try:
    file_input = JSON_FILES_PATH + "input_eg2.json"
    # Crear una instancia de HotelStay con datos simulados
    stay = HotelManager().guest_arrival(file_input)

    # Llamar a la función guest_arrival con el archivo de entrada simulado
    print("Clave de habitación generada:", stay)


except HotelManagementException as e:
    print("Error:", e)
