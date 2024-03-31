import json
import os
import re
from datetime import datetime
from HotelManagementException import HotelManagementException
from HotelReservation import HotelReservation
from HotelStay import HotelStay


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

    def ReaddatafromJSOn(self, fi):

        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            c = DATA["CreditCard"]
            p = DATA["phoneNumber"]

        except KeyError as e:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(c):
            raise HotelManagementException("Invalid credit card number")

    def room_reservation(self, creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days):

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
            if os.path.exists("reservations.json") and os.path.getsize("reservations.json") > 0:
                with open("reservations.json", "r") as file:
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
            with open("reservations.json", "w") as file:
                json.dump(data, file, indent=4)

            return reserva.LOCALIZER
        except HotelManagementException as e:
            raise HotelManagementException("Error: " + str(e))

    def guest_arrival(self, input_file):
        '''// El archivo de entrada es una cadena con la ruta del archivo
            descrita en HM-FR-02-I1
        // Devuelve un String en hexadecimal que representa el código de
            la habitación (clave que será necesaria para HM-FR-02-O1)
        // En caso de error, devuelve un HotelManagementException
            representa HM-FR-02-O3'''
        try:
            with open(input_file, 'r') as file_input:
                data_input = json.load(file_input)
                if "Localizer" not in data_input or "IdCard" not in data_input:
                    raise HotelManagementException("El JSON no tiene la estructura esperada")
                localizer_input = data_input["Localizer"]
                dni_input = data_input["IdCard"]

            if not isinstance(localizer_input, str) or len(localizer_input) != 32:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")
            if not isinstance(dni_input, str) or len(dni_input) != 9:
                raise HotelManagementException("Los datos del JSON no tienen valores válidos.")

            with open("reservations.json", 'r') as file:
                data = json.load(file)

                # Verificar que el localizador está almacenado en el archivo de reservas (simulado)
                # y que coincide con los datos en el archivo
                exite_el_localizer = False
                for reservation in data["reservations"]:
                    if localizer_input == reservation["localizer"] and dni_input == reservation["id_card"]:
                        exite_el_localizer = True
                        numDays = reservation["num_days"]
                        roomType = reservation["room_type"]
                        arrivalDate = reservation["arrival_date"]
                        break
                if exite_el_localizer == False:
                    raise HotelManagementException(
                        "El localizador y el dni introducido no se corresponde con los datos almacenados")

                estancia = HotelStay(dni_input, localizer_input, numDays, roomType)

                # Convertir la fecha de llegada del archivo JSON a un objeto datetime
                arrival_date_json = datetime.strptime(arrivalDate, "%d/%m/%Y")
                # Verificar que la fecha de llegada coincide con la fecha actual (sin tener en cuenta las horas y minutos)
                if arrival_date_json.date() != estancia.arrival:
                    print(arrival_date_json.date(), estancia.arrival)
                    raise HotelManagementException("La fecha de llegada no coincide con la fecha actual")

                # Generar el código de habitación utilizando SHA-256
                room_key = estancia.room_key
                if not room_key:
                    raise HotelManagementException("Error de procesamiento interno al obtener la clave.")

                if os.path.exists("estancias.json") and os.path.getsize("estancias.json") > 0:
                    with open("estancias.json", "r") as file:
                        data = json.load(file)
                else:
                    data = {"estancias": []}

                data["estancias"].append(estancia.signature_string())

                # Almacenar los datos actualizados en el archivo JSON
                with open("estancias.json", "w") as file_out:
                    json.dump(data, file_out, indent=1)

        except FileNotFoundError:
            raise HotelManagementException("No se encuentra el archivo de datos")
        except json.JSONDecodeError:
            raise HotelManagementException("El archivo no tiene formato JSON")
        except HotelManagementException as e:
            raise e

        return room_key


# Ejemplo de uso:
try:

    localizador = HotelManager().room_reservation("5256783371569576", "Lola Montero", "12345678Z", "123456781",
                                                  "single",
                                                  "13/12/2024", 5)
    print("Localizador de reserva:", localizador)

except HotelManagementException as e:
    print("Error al realizar la reserva:", e)

try:
    # Crear una instancia de HotelStay con datos simulados
    stay = HotelManager().guest_arrival("input_eg2.json")

    # Llamar a la función guest_arrival con el archivo de entrada simulado
    print("Clave de habitación generada:", stay)


except HotelManagementException as e:
    print("Error:", e)
