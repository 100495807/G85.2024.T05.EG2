import os.path
import json
from freezegun import freeze_time

import unittest
from UC3MTravel.HotelManager import HotelManager
from UC3MTravel.HotelManagementException import HotelManagementException
from pathlib import Path
JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles"
import os

class TestGuestArrival(unittest.TestCase):

    def setUp(self):
        JSON_PATH = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = JSON_PATH + "reservations.json"
        if (os.path.exists(file_path)):
            os.remove(file_path)

        HotelManager().room_reservation("5256783371569576", "Lola Montero", "12345678Z", "123456781",
                                                  "single",
                                                  "13/12/2024", 5)
    @freeze_time("13/12/2024")
    def test1_valid_input(self):
        test_data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Z"
        }
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path2 = os.path.join(json_files_dir, "input_eg2.json")
        file_path = os.path.join(json_files_dir, "valid_input.json")

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        stay = HotelManager()
        result = stay.guest_arrival(file_path2)
        myrequest = stay.guest_arrival(file_path)
        self.assertTrue(len(result) == 64)
        self.assertEqual(result, myrequest)

    # Archivo inexistente
    def test2_missing_file(self):
        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival("nonexistent_file.json")
        self.assertEqual(str(context.exception), "El archivo no existe")

    # Prueba para formato JSON inválido
    def test3_invalid_json_format(self):
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_json_format.json"

        with open(file_path, 'w') as file:
            file.write(file_path)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba archivo vacio
    def test4_empty_file(self):
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "empty_file.json"

        with open(file_path, 'w') as file:
            file.write(file_path)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba estructural JSON
    def test5_invalid_json_structure(self):
        test_data = {
            "InvalidKey": "abcdef1234567890abcdef1234567890"
        }
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_structure.json"
        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba para localizador inválido que no figura en el archivo reservas
    def test6_invalid_localizer(self):
        test_data = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El localizador y el dni introducido no se corresponde con los datos almacenados")

    def test6_invalid_localizer_33(self):
        test_data = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer_33.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El localizador y el dni introducido no se corresponde con los datos almacenados")

    def test6_invalid_localizer_31(self):
        test_data = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer_31.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "El localizador y el dni introducido no se corresponde con los datos almacenados")

    def test7_invalid_dni(self):
        test_data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Y"
        }
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_dni.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test8_empty_json(self):
        test_data = {}
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "empty_json.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception),
                         "El archivo no tiene formato JSON")

    def test9_localizer_short(self):
        test_data = {
            "Localizer": "56yf32f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test10_hora_equivocada(self):
        test_data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Z"
        }
        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path2 = os.path.join(json_files_dir, "input_eg2.json")
        file_path = os.path.join(json_files_dir, "invalid_time.json")

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception), "La fecha de llegada no coincide con la fecha actual")

    def test11_localizer_2puntos(self):
        test_data = {
            "Localizer": "56yf32f34kfh6b6..f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test11_falta_separador(self):
        test_data = {
            "Localizer": "56yf32f34kfh6b6..f82e7651",
            "IdCard": "47589661Q",
        }

        json_files_dir = (str(Path.home()) +
                          "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        file_path = json_files_dir + "invalid_localizer.json"

        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as context:
            stay = HotelManager()
            stay.guest_arrival(file_path)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")







if __name__ == "__main__":
    unittest.main()
