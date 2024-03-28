''' Class HotelStay (GE2.2) '''

import os
import hashlib
from HotelManagementException import HotelManagementException
import json
from datetime import datetime, timedelta, timezone


class HotelStay():
    def __init__(self, idcard, localizer, numdays, roomtype):
        self.__alg = "SHA-256"
        self.__type = roomtype
        self.__idcard = idcard
        self.__localizer = localizer
        self.__arrival = datetime.now(timezone.utc)
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express numdays in seconds
        self.__departure = self.__arrival + timedelta(days=numdays)
        self.__room_key = self.__signature_string()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + self.__arrival.strftime("%Y-%m-%d %H:%M:%S") + \
            ",departure:" + self.__departure.strftime("%Y-%m-%d %H:%M:%S") + "}"

    def guest_arrival (self, input_file):
        '''// El archivo de entrada es una cadena con la ruta del archivo
            descrita en HM-FR-02-I1
        // Devuelve un String en hexadecimal que representa el código de
            la habitación (clave que será necesaria para HM-FR-02-O1)
        // En caso de error, devuelve un HotelManagementException
            representa HM-FR-02-O3'''
        try:
            with open(input_file, 'r') as file_input:
                data_input = json.load(file_input)
                localizer_input = data_input["Localizer"]
                dni_input = data_input["IdCard"]

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
                        break
                if exite_el_localizer == False:
                    raise HotelManagementException("El localizador y el dni introducido no se corresponde con los datos almacenados")

                # Generar el código de habitación utilizando SHA-256
                room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

                if os.path.exists("estancias.json") and os.path.getsize("estancias.json") > 0:
                    with open("estancias.json", "r") as file:
                        data = json.load(file)
                else:
                    data = {"estancias": []}

                estancia = HotelStay(dni_input, localizer_input, numDays, roomType)
                data["estancias"].append(estancia.__signature_string())

                # Almacenar los datos actualizados en el archivo JSON
                with open("estancias.json", "w") as file_out:
                    json.dump(data, file_out, indent=1)

                return room_key  # Devolver la clave en formato hexadecimal


        except FileNotFoundError:
            raise HotelManagementException("No se encuentra el archivo de datos")
        except json.JSONDecodeError:
            raise HotelManagementException("El archivo no tiene formato JSON")
        except HotelManagementException as e:
            raise e



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

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        self.__departure = value

try:
    # Crear una instancia de HotelStay con datos simulados
    stay = HotelStay(idcard="48160293H", localizer="42421adc38be029aab0fddeda15e03dd", numdays=5, roomtype="single")

    # Llamar a la función guest_arrival con el archivo de entrada simulado
    clave_habitacion = stay.guest_arrival("input_eg2.json")
    print("Clave de habitación generada:", clave_habitacion)

except HotelManagementException as e:
    print("Error:", e)
except FileNotFoundError:
    print("Error: No se encuentra el archivo de datos 'reservations.json'")
except json.JSONDecodeError:
    print("Error: El archivo 'reservations.json' no tiene formato JSON")

