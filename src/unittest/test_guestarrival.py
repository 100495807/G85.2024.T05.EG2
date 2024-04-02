import os.path
import json
from freezegun import freeze_time
import unittest
from UC3MTravel.HotelManager import HotelManager
from UC3MTravel.HotelManagementException import HotelManagementException
from pathlib import Path
import os

JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles"


class TestGuestArrival(unittest.TestCase):

    def setUp(self):
        JSON_PATH = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = JSON_PATH + "reservations.json"
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        HotelManager().room_reservation("5256783371569576", "Lola Montero", "12345678Z", "123456781",
                                        "single",
                                        "13/12/2024", 5)

    # test valido
    @freeze_time("13/12/2024")
    def test1_valido(self):
        data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Z"
        }
        ruta_archivo_json = (str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo_input = os.path.join(ruta_archivo_json, "input_eg2.json")
        ruta_archivo = os.path.join(ruta_archivo_json, "valido.json")

        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        hotel_stay = HotelManager()
        result = hotel_stay.guest_arrival(ruta_archivo_input)
        myrequest = hotel_stay.guest_arrival(ruta_archivo)
        self.assertTrue(len(result) == 64)
        self.assertEqual(result, myrequest)

    # Archivo inexistente
    def test2_no_existe_archivo(self):
        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival("no_existe_archivo.json")
        self.assertEqual(str(context.exception), "El archivo no existe")

    # Prueba para formato JSON inválido
    def test3_invalido_formato_json(self):
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_formato_json.json"

        with open(ruta_archivo, 'w') as file:
            file.write("hsfkcuasduHGWEUFSHJDOISD")

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba archivo vacio
    def test4_json_vacio_sin_llaves(self):
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "json_vacio_sin_llaves.json"

        with open(ruta_archivo, 'w') as file:
            file.write("")

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    def test5_json_vacio_con_llaves(self):
        data = {}
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "json_vacio_con_llaves.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El archivo no tiene formato JSON")

    def test6_invalido_json_estructure_localizer(self):
        data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_localizer.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    def test7_invalido_json_estructure_localizer_nombre(self):
        data = {
            "Invalid_localizer": "04a90f1ce1fb8e6cc213fd4480803141"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_localizer_nombre.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    def test8_invalido_json_estructure_localizer_num(self):
        data = {
            "Invalid_localizer": "04a90f1ce1fb8e6cc213fd6480803141"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_localizer_num.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba estructural JSON
    def test9_invalido_json_estructure_idCard(self):
        data = {
            "IdCard": "12345678Z"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_idCard.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    def test10_invalido_json_estructure_idCard_num(self):
        data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "Invalid_IdCard": "12345678Z"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_idCard_num.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(data, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    def test11_invalido_json_estructure_idCard_num(self):
        datos = {
            "IdCard": "12345679O"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_json_estructure_idCard_num.json"
        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "El archivo no tiene formato JSON")

    # Prueba para localizador inválido que no figura en el archivo reservas
    def test12_invalido_localizer(self):
        datos = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_localizer.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El localizador o el dni introducido no se corresponde con los datos almacenados")

    def test13_invalido_localizer_33(self):
        datos = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_localizer_33.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El localizador o el dni introducido no se corresponde con los datos almacenados")

    def test14_invalido_localizer_31(self):
        datos = {
            "Localizer": "56yf3201d9c43f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_localizer_31.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El localizador o el dni introducido no se corresponde con los datos almacenados")

    def test15_invalido_dni(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Y"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test16_invalido_dni_sin_letra(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni_sin_letra.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test17_invalido_dni_solo_nums(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "123456789"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni_solo_nums.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test18_invalido_dni_corto(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "123456"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni_corto.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test19_invalido_dni_excede_letra(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678AB"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni_excede_letra.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test20_invalido_dni_excede_num(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678A8"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_dni_excede_num.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test21_localizer_corto(self):
        datos = {
            "Localizer": "56yf32f34kfh6b671f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "localizer_corto.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test22_localizer_vacio(self):
        datos = {
            "Localizer": "",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "localizer_vacio.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test23_dni_vacio(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": ""
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "dni_vacio.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test24_hora_equivocada(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Z"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = os.path.join(ruta_archivo_json, "invalid_time.json")

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception), "La fecha de llegada no coincide con la fecha actual")

    def test25_invalido_localizer_x2(self):
        datos = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_localizer_x2.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El archivo no tiene formato JSON")

    def test26_invalido_idCard_x2(self):
        datos = {
            "IdCard": "12345678Z",
            "IdCard": "12345678Z"
        }
        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "invalido_idCard_x2.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "El archivo no tiene formato JSON")

    def test27_localizer_caracteres_invalidos_inicio(self):
        datos = {
            "Localizer": "..56yf32f34kfh6b6f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "localizer_caracteres_invalidos_inicio.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test28_localizer_caracteres_invalidos_mitad(self):
        datos = {
            "Localizer": "56yf32f34k..fh6b6f82e7651",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "localizer_caracteres_invalidos_inicio.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test29_localizer_caracteres_invalidos_fin(self):
        datos = {
            "Localizer": "56yf32f34kfh6b6f82e7651..",
            "IdCard": "47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "localizer_caracteres_invalidos_fin.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos.")

    def test30_dni_caracteres_invalidos_ini(self):
        datos = {
            "Localizer": "56yf32f34kfh6b6f82e7651",
            "IdCard": "..47589661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "dni_caracteres_invalidos_ini.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test31_dni_caracteres_invalidos_mitad(self):
        datos = {
            "Localizer": "56yf32f34kfh6b6f82e7651",
            "IdCard": "4758..9661Q",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "dni_caracteres_invalidos_mitad.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")

    def test32_dni_caracteres_invalidos_fin(self):
        datos = {
            "Localizer": "56yf32f34kfh6b6f82e7651",
            "IdCard": "47589661Q..",
        }

        ruta_archivo_json = (str(Path.home()) +
                             "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/")

        ruta_archivo = ruta_archivo_json + "dni_caracteres_invalidos_fin.json"

        with open(ruta_archivo, 'w') as file:
            json.dump(datos, file)

        with self.assertRaises(HotelManagementException) as context:
            hotel_stay = HotelManager()
            hotel_stay.guest_arrival(ruta_archivo)
        self.assertEqual(str(context.exception),
                         "Los datos del JSON no tienen valores válidos")


"""añadir solo { y otro solo }"""

if __name__ == "__main__":
    unittest.main()
