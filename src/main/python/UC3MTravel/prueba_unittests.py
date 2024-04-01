import unittest
import json
from HotelManager import HotelManager
from HotelManagementException import HotelManagementException

class TestGuestArrival(unittest.TestCase):

    # Prueba para datos válidos
    def test1_valid_input(self):
        input_file = "valid_input.json"
        test_data = {
            "Localizer": "04a90f1ce1fb8e6cc213fd6480803141",
            "IdCard": "12345678Z"
        }
        with open(input_file, 'w') as file:
            json.dump(test_data, file)

        stay = HotelManager()
        result = stay.guest_arrival(input_file)
        self.assertTrue(len(result) == 64)


    # Archivo inexistente
    def test2_missing_file(self):
        with self.assertRaises(HotelManagementException) as e:
            stay = HotelManager()
            stay.guest_arrival("nonexistent_file.json")
        self.assertEqual(str(e.exception), "El archivo no existe")

    # Prueba para formato JSON inválido
    def test3_invalid_json_format(self):
        input_file = "invalid_json.json"
        with open(input_file, 'w') as file:
            file.write("invalid_json_data")

        with self.assertRaises(HotelManagementException) as e:
            stay = HotelManager()
            stay.guest_arrival(input_file)
        self.assertEqual(str(e.exception), "El archivo no tiene formato JSON")

    # Prueba estructural JSON
    def test4_invalid_json_structure(self):
        input_file = "invalid_structure.json"
        test_data = {
            "InvalidKey": "abcdef1234567890abcdef1234567890"
        }
        with open(input_file, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as e:
            stay = HotelManager()
            stay.guest_arrival(input_file)
        self.assertEqual(str(e.exception), "El archivo no tiene formato JSON")

    # Prueba para localizador no válido
    def test5_invalid_localizer(self):
        input_file = "invalid_localizer.json"
        test_data = {
            "Localizer": "localizador_inventado",
            "IdCard": "12345678Z",
        }
        with open(input_file, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as e:
            stay = HotelManager()
            stay.guest_arrival(input_file)
        self.assertEqual(str(e.exception), "Los datos del JSON no tienen valores válidos.")

    # Prueba para DNI inválido
    def test6_invalid_DNI(self):
        input_file = "invalid_DNI.json"
        test_data = {
            "Localizer": "c96704b8ad7b9c5e8168a5b282eb99a4",
            "IdCard": "057275G",

        }
        with open(input_file, 'w') as file:
            json.dump(test_data, file)

        with self.assertRaises(HotelManagementException) as e:
            stay = HotelManager()
            stay.guest_arrival(input_file)
        self.assertEqual(str(e.exception), "Los datos del JSON no tienen valores válidos")




if __name__ == "__main__":
    unittest.main()
