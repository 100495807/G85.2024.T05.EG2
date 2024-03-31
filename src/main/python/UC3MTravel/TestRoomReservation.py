import unittest
import os
from HotelManager import HotelManager
from HotelManagementException import HotelManagementException

class TestHotelManager(unittest.TestCase):

    def setUp(self):

        if os.path.isfile("reservations.json"):
            os.remove("reservations.json")

    def test_room_reservation_valid(self):
        # Caso de prueba para una reserva completa válida
        manager = HotelManager()
        localizer = manager.room_reservation(
            creditcardNumb="5256783371569576",
            nAMeAndSURNAME="Lola Montero",
            IDCARD="12345678Z",
            phonenumber="123456781",
            room_type="single",
            arrival_date="13/12/2024",
            num_days=5
        )

        self.assertEqual(localizer, "04a90f1ce1fb8e6cc213fd6480803141")

        # Verificar que la reserva se agregó al archivo JSON
        with open("reservations.json", "r") as file:
            data = file.read()

        self.assertIn("12345678Z", data)  # Verificar si el DNI está en la reserva

    def test_room_reservation_invalid_credit_card(self):
        # Caso de prueba para una tarjeta de crédito inválida
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="1234567812345678",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_room_reservation_invalid_credit_card2(self):
        # Caso de prueba para una tarjeta de crédito inválida (longitud incorrecta)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="525678337156957",  # 15 dígitos
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_room_reservation_invalid_name_surname(self):
        # Caso de prueba para un nombre y apellidos inválidos (demasiado cortos)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La cadena del nombre y apellidos no es válida")

    def test_room_reservation_invalid_dni(self):
        # Caso de prueba para un DNI inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: DNI inválido")

    def test_room_reservation_invalid_phone_number(self):
        # Caso de prueba para un número de teléfono inválido (longitud incorrecta)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="1234567890",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de teléfono inválido")

    def test_room_reservation_invalid_room_type(self):
        # Caso de prueba para un tipo de habitación inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="shared",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Tipo de habitación inválido")

    def test_room_reservation_invalid_arrival_date(self):
        # Caso de prueba para una fecha de llegada inválida
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="20/08/2022",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La fecha de llegada debe ser posterior a la fecha actual")

    def test_room_reservation_invalid_arrival_date_format(self):
        # Caso de prueba para una fecha de llegada con un formato inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/13/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

    def test_room_reservation_invalid_num_days(self):
        # Caso de prueba para un número de días inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=15
            )

        self.assertEqual(str(e.exception), "Error: Número de noches inválido. Debe estar entre 1 y 10.")

    def test_room_reservation_customer_has_reservation(self):
        # Caso de prueba para un cliente que ya tiene una reserva
        manager = HotelManager()
        manager.room_reservation(
            creditcardNumb="5256783371569576",
            nAMeAndSURNAME="Lola Montero",
            IDCARD="12345678Z",
            phonenumber="123456781",
            room_type="single",
            arrival_date="13/12/2024",
            num_days=5
        )

        with self.assertRaises(HotelManagementException) as e:
            manager.room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: El cliente ya tiene una reserva")

