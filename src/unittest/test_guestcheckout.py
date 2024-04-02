from UC3MTravel.HotelManagementException import HotelManagementException
from UC3MTravel.HotelManager import HotelManager
from pathlib import Path
import unittest
import os
import json
from freezegun import freeze_time
JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/"


class TestGuestCheckout(unittest.TestCase):

    def setUp(self):
        self.manager = HotelManager()
        JSON_PATH = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = JSON_PATH + "estancias.json"
        if (os.path.exists(file_path)):
            os.remove(file_path)

        file_path2 = JSON_PATH + "check_outs.json"
        if (os.path.exists(file_path2)):
            os.remove(file_path2)

        data = {"estancias": []}
        datos_estancia = {
            "alg": "SHA-256",
            "typ": "single",
            "localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "arrival": "13/12/2024",
            "departure": "18/12/2024",
            "room_key": "aafaff12f5fb742529f6d794d3e251f6387cd8633b5d3d29825afba6564d1581"
        }
        data["estancias"].append(datos_estancia)

        # Almacenar los datos actualizados en el archivo JSON
        with open(file_path, "w") as file_out:
            json.dump(data, file_out, indent=1)

    @freeze_time("12/18/2024")
    def test_guest_checkout_valid(self):
        # Caso de prueba válido
        room_key = "aafaff12f5fb742529f6d794d3e251f6387cd8633b5d3d29825afba6564d1581"
        self.assertTrue(self.manager.guest_checkout(room_key) == True)


    def test_guest_checkout_invalid_room_key(self):
        # Casos de prueba con room_key inválido
        with self.assertRaises(HotelManagementException) as context:
            # No es una cadena
            room_key = 324
            self.manager.guest_checkout(room_key)
        self.assertEqual(context.exception.message, "El código de habitación no es válido")

    def test_guest_checkout_length_room_key(self):
        with self.assertRaises(HotelManagementException) as context:
            # Longitud incorrecta
            room_key = "123"
            self.manager.guest_checkout(room_key)
        self.assertEqual(str(context.exception), "El código de habitación no es válido")

    def test_guest_checkout_not_found(self):
        # Casos de prueba con room_key no encontrado
        with self.assertRaises(HotelManagementException) as context:
            # Room key no existe
            room_key = "skshake7f5fb742529x6z594d3e251f6387cd8633b5d3d29825afba628493724"
            self.manager.guest_checkout(room_key)
        self.assertEqual(str(context.exception), "El código de habitación no está registrado")

    def test_guest_checkout_no_date(self):
        # Caso de prueba con archivo de estancias vacío o no existe
        JSON_PATH = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = JSON_PATH + "estancias.json"
        if (os.path.exists(file_path)):
            os.remove(file_path)
        with self.assertRaises(HotelManagementException) as context:
            self.manager.guest_checkout("28d32fa25abce85a4f01bebd32cf6a7364f532727af401c1561eefec02cf1cz7")
        self.assertEqual(str(context.exception), "El archivo de estancias no existe o está vacío")

    def test_guest_checkout_no_date_2(self):
        # Caso de prueba con archivo de estancias vacío o no existe
        JSON_PATH = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = JSON_PATH + "estancias.json"
        if (os.path.exists(file_path)):
            os.remove(file_path)
        data = None
        with open(file_path, "w") as file_out:
            json.dump(data, file_out, indent=1)

        with self.assertRaises(HotelManagementException) as context:
            self.manager.guest_checkout("28d32fa25abce85a4f01bebd32cf6a7364f532727af401c1561eefec02cf1cz7")
        self.assertEqual(str(context.exception), "El archivo de estancias no existe o está vacío")

    @freeze_time("04/07/2024")
    def test_guest_checkout_past_date(self):
        # Caso de prueba con fecha de salida no coincide
        with self.assertRaises(HotelManagementException) as context:
            self.manager.guest_checkout("aafaff12f5fb742529f6d794d3e251f6387cd8633b5d3d29825afba6564d1581")
        self.assertEqual(str(context.exception), "La fecha de salida no coincide")


