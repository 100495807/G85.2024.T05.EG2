import unittest
from datetime import datetime, timezone
from datetime import datetime, timedelta
from unittest.mock import patch
from UC3MTravel.HotelManager import HotelManager
from pathlib import Path
from UC3MTravel.HotelManagementException import HotelManagementException

class TestRF3(unittest.TestCase):
    def test_valid_room_key_format(self):
        # La habitación tiene un formato válido
        room_key = "0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcdef"
        self.assertTrue(HotelManager.guest_checkout(room_key))

        # La habitación tiene un formato inválido (longitud incorrecta)
        room_key = "0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcd"
        self.assertFalse(HotelManager.guest_checkout(room_key))

        # La habitación tiene un formato inválido (caracteres no hexadecimales)
        room_key = "0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcg"
        self.assertFalse(HotelManager.guest_checkout(room_key))

    @patch("hotel_manager.json.load")
    def test_checkout_with_valid_room_key_and_date(self, mock_load):
        # Definir el contenido simulado del archivo de estancias
        mock_load.return_value = {
            "0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcdef": {
                "departure": (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        }

        # Realizar el checkout
        result = self.manager.guest_checkout("0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcdef")

        # Verificar que el resultado sea True
        self.assertTrue(result)

    @patch("hotelmanager.json.load")
    def test_checkout_with_valid_room_key_and_invalid_date(self, mock_load):
        # Definir el contenido simulado del archivo de estancias
        mock_load.return_value = {
            "0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcdef": {
                "departure": (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        }

        # Realizar el checkout
        result = self.manager.guest_checkout("0123456789abcdefABCDEF0123456789abcdefABCDEF0123456789abcdef")

        # Verificar que el resultado sea False
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()