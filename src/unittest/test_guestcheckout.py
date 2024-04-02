from UC3MTravel.HotelManagementException import HotelManagementException
from UC3MTravel.HotelManager import HotelManager
from pathlib import Path
import unittest
from freezegun import freeze_time

JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G85.2024.T05.EG2/src/JsonFiles/"



class TestGuestCheckout(unittest.TestCase):
    def setUp(self):
        self.manager = HotelManager()  # Crear una instancia de HotelManager

    @freeze_time("18/12/2024")
    def test_guest_checkout_valid(self):
        # Caso de prueba válido
        self.assertTrue(
            self.manager.guest_checkout("aafaff12f5fb742529f6d794d3e251f6387cd8633b5d3d29825afba6564d1581") == True)

    def test_guest_checkout_invalid_room_key(self):
        # Casos de prueba con room_key inválido
        with self.assertRaises(HotelManagementException):
            # No es una cadena
            self.manager.guest_checkout("123")
        with self.assertRaises(HotelManagementException):
            # Longitud incorrecta
            self.manager.guest_checkout("123")

    def test_guest_checkout_not_found(self):
        # Casos de prueba con room_key no encontrado
        with self.assertRaises(HotelManagementException):
            # Room key no existe
            self.manager.guest_checkout("non_existent_room_key")

    def test_guest_checkout_empty_file(self):
        # Caso de prueba con archivo de estancias vacío
        with self.assertRaises(HotelManagementException):
            self.manager.guest_checkout("room_key_not_found_in_empty_file")

    def test_guest_checkout_past_date(self):
        # Caso de prueba con fecha de salida en el pasado
        with self.assertRaises(HotelManagementException):
            self.manager.guest_checkout("room_key_with_past_date")


if __name__ == '__main__':
    unittest.main()
