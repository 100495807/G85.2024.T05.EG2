''' Class HotelStay (GE2.2) '''

import hashlib
from HotelManagementException import HotelManagementException
import json
from datetime import datetime, timedelta


class HotelStay():
    def __init__(self, idcard, localizer, numdays, roomtype):
        self.__alg = "SHA-256"
        self.__type = roomtype
        self.__idcard = idcard
        self.__localizer = localizer
        self.__arrival = datetime.now().date()
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express numdays in seconds
        self.__departure = self.__arrival + timedelta(days=numdays)
        self.__room_key = self.signature_string()

    def signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + self.__arrival.strftime("%Y-%m-%d") + \
            ",departure:" + self.__departure.strftime("%Y-%m-%d") + "}"

    @property
    def idCard(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @idCard.setter
    def icCard(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    def room_key(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.signature_string().encode()).hexdigest()

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        self.__departure = value
'''
    def guest_arrival(self, input_file):
        // El archivo de entrada es una cadena con la ruta del archivo
            descrita en HM-FR-02-I1
        // Devuelve un String en hexadecimal que representa el código de
            la habitación (clave que será necesaria para HM-FR-02-O1)
        // En caso de error, devuelve un HotelManagementException
            representa HM-FR-02-O3
        try:
            with open(input_file, 'r') as file:
                data = json.load(file)

                # Verificar la estructura del JSON
                if not all(reservation.get(key) for key in ("localizer", "id_card") for reservation in
                           data.get("reservations", [])):
                    raise HotelManagementException("El JSON no tiene la estructura esperada")

                # Verificar que el localizador está almacenado en el archivo de reservas (simulado)
                # y que coincide con los datos en el archivo
                localizers = [reservation["localizer"] for reservation in data["reservations"]]
                if self.__localizer not in localizers:
                    raise HotelManagementException("El localizador no se corresponde con los datos almacenados")

                arrival_dates = [reservation["arrival_date"] for reservation in data["reservations"]
                                 if reservation["localizer"] == self.__localizer]

                if not arrival_dates:
                    raise HotelManagementException("No se encontró la fecha de llegada para el localizador dado")

                # Convertir la fecha de llegada del archivo JSON a un objeto datetime
                arrival_date_json = datetime.strptime(arrival_dates[0], "%d/%m/%Y")

                # Verificar que la fecha de llegada coincide con la fecha actual (sin tener en cuenta las horas y minutos)
                if arrival_date_json.date() != self.__arrival.date():
                    raise HotelManagementException("La fecha de llegada no coincide con la fecha actual")

                return self.ROOM_KEY  # Devolver la clave en formato hexadecimal

        except FileNotFoundError:
            raise HotelManagementException("No se encuentra el archivo de datos")
        except json.JSONDecodeError:
            raise HotelManagementException("El archivo no tiene formato JSON")
        except HotelManagementException as e:
            raise e
'''



