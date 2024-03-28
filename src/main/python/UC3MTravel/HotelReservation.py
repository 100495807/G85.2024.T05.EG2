import os
import hashlib
import json
import re
from datetime import datetime
from HotelManagementException import HotelManagementException
from HotelManager import HotelManager

class HotelReservation:
    def __init__(self, creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days):
        self.__crEDITcardnumber = creditcardNumb
        self.__NAME_SURNAME = nAMeAndSURNAME
        self.__idcard = IDCARD
        self.__phonenumber = phonenumber
        self.__roomtype = room_type
        self.__ARRIVAL = arrival_date
        self.__num_days = num_days

        manager = HotelManager()

        if not manager.validatecreditcard(creditcardNumb):
            raise HotelManagementException("Número de tarjeta de crédito inválido")

        if len(nAMeAndSURNAME.split()) < 2 or len(nAMeAndSURNAME) < 10 or len(nAMeAndSURNAME) > 50:
            raise HotelManagementException("La cadena del nombre y apellidos no es válida")

        if not re.match(r'^\d{8}[A-Za-z]$', IDCARD):
            raise HotelManagementException("DNI inválido")

        if not phonenumber.isdigit() or len(phonenumber) != 9:
            raise HotelManagementException("Número de teléfono inválido")

        if room_type not in ['single', 'double', 'suite']:
            raise HotelManagementException("Tipo de habitación inválido")

        if not 1 <= num_days <= 10:
            raise HotelManagementException("Número de noches inválido. Debe estar entre 1 y 10.")

        try:
            # Convertir la cadena en un objeto datetime
            arrival_date = datetime.strptime(arrival_date, "%d/%m/%Y")

            # Verificar que la fecha sea mayor que la fecha actual
            if arrival_date <= datetime.now():
                raise HotelManagementException("La fecha de llegada debe ser posterior a la fecha actual")

            # Verificar que el día esté entre 1 y 31 y el mes esté entre 1 y 12
            if not (1 <= arrival_date.day <= 31 and 1 <= arrival_date.month <= 12):
                raise HotelManagementException("La fecha de llegada contiene un día o mes inválido")
        except ValueError:
            raise HotelManagementException("Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")


    def __str__(self):
        json_info = {
            "credit_card": self.__crEDITcardnumber,
            "name_surname": self.__NAME_SURNAME,
            "id_card": self.__idcard,
            "phone_number": self.__phonenumber,
            "room_type": self.__roomtype,
            "arrival_date": self.__ARRIVAL,
            "num_days": self.__num_days,
        }
        return json.dumps(json_info)

    @property
    def LOCALIZER(self):
        return hashlib.md5(self.__str__().encode()).hexdigest()


def room_reservation(creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days):
    try:
        reserva = HotelReservation(creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days)
        localizer = reserva.LOCALIZER
        # Verificar si el archivo existe y no está vacío
        if os.path.exists("reservations.json") and os.path.getsize("reservations.json") > 0:
            with open("reservations.json", "r") as file:
                data = json.load(file)
        else:
            data = {"reservations": []}

        # Verificar si el cliente ya tiene una reserva
        for reservation in data["reservations"]:
            if reservation["id_card"] == IDCARD:
                raise HotelManagementException("El cliente ya tiene una reserva")

        # Agregar el localizador a los datos  de la reserva
        reservation_data = {
            "credit_card": creditcardNumb,
            "name_surname": nAMeAndSURNAME,
            "id_card": IDCARD,
            "phone_number": phonenumber,
            "room_type": room_type,
            "arrival_date": arrival_date,
            "num_days": num_days,
            "localizer": localizer  # Agregar el localizador aquí
        }

        # Agregar la nueva reserva a los datos
        data["reservations"].append(reservation_data)

        # Almacenar los datos actualizados en el archivo JSON
        with open("reservations.json", "w") as file:
            json.dump(data, file, indent=4)


        return localizer
    except HotelManagementException as e:
        raise HotelManagementException("Error: " + str(e))

# Ejemplo de uso:
try:
    localizador = room_reservation("5256783371569576", "Lola Montero", "48160293H", "123456781", "single",
                                                "13/12/2024", 5)
    print("Localizador de reserva:", localizador)

except HotelManagementException as e:
    print("Error al realizar la reserva:", e)

