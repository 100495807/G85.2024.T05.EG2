import hashlib
import json
from datetime import datetime, timezone
from HotelManagementException import HotelManagementException

class HotelReservation:
    def __init__(self, IDCARD, creditcardNumb, nAMeAndSURNAME, phonenumber, room_type, numdays):
        self.__crEDITcardnumber = creditcardNumb
        self.__idcard = IDCARD
        justnow = datetime.now(timezone.utc)  # Utilizando datetime.now(timezone.utc) en lugar de datetime.utcnow()
        self.__ARRIVAL = datetime.timestamp(justnow)
        self.__NAME_SURNAME = nAMeAndSURNAME
        self.__phonenumber = phonenumber
        self.__roomtype = room_type
        self.__num_days = numdays

        # Verificar la validez de los datos
        if len(self.__crEDITcardnumber) != 16 or not self.__crEDITcardnumber.isdigit():
            raise HotelManagementException("Número de tarjeta de crédito inválido")
        if not self.__idcard.isdigit() or len(self.__idcard) != 9:
            raise HotelManagementException("DNI inválido")
        if len(self.__NAME_SURNAME.split()) < 2 or len(self.__NAME_SURNAME) < 10 or len(self.__NAME_SURNAME) > 50:
            raise HotelManagementException("Nombre y apellidos inválidos")
        if not self.__phonenumber.isdigit() or len(self.__phonenumber) != 9:
            raise HotelManagementException("Número de teléfono inválido")
        if self.__roomtype not in ['single', 'double', 'suite']:
            raise HotelManagementException("Tipo de habitación inválido")

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__idcard,
                     "name_surname": self.__NAME_SURNAME,
                     "credit_card": self.__crEDITcardnumber,
                     "phone_number:": self.__phonenumber,
                     "arrival_date": self.__ARRIVAL,
                     "num_days": self.__num_days,
                     "room_type": self.__roomtype,
                     }
        return "HotelReservation:" + json_info.__str__()

    @property
    def LOCALIZER(self):
        """Returns the md5 signature"""
        return hashlib.md5(self.__str__().encode()).hexdigest()

    def room_reservation(self, credit_card, name_surname, id_card, phone_number, room_type, num_days):
        try:
            reservation = HotelReservation(id_card, credit_card, name_surname, phone_number, room_type, num_days)
            localizer = reservation.LOCALIZER

            # Almacenar los datos de la reserva en un archivo
            with open("reservations.txt", "a") as file:
                file.write(str(reservation) + "\n")

            return localizer  # Devuelve el localizador
        except HotelManagementException as e:
            raise HotelManagementException("Error: " + str(e))


# Ejemplo de uso:
try:
    hotel_booking = HotelReservation("123456789", "1234567890123456", "Lola Montero", "123456789", "single", 3)
    localizer = hotel_booking.room_reservation("1234567890123456","Lola Montero", "123456789", "123456789", "single", 3)
    print("Localizador de reserva:", localizer)
except HotelManagementException as e:
    print("Error al realizar la reserva:", e)
