import os
import unittest
from HotelManager import HotelManager
from HotelManagementException import HotelManagementException

class TestHotelManager(unittest.TestCase):

    def setUp(self):
        if os.path.isfile("reservations.json"):
            os.remove("reservations.json")
    def test_TC1(self):
        # Caso de prueba para todos los datos válidos
        locator = HotelManager().room_reservation(
            creditcardNumb="5256783371569576",
            nAMeAndSURNAME="Lola Montero",
            IDCARD="12345678Z",
            phonenumber="123456781",
            room_type="single",
            arrival_date="13/12/2024",
            num_days=5
        )
        self.assertEqual(locator, "04a90f1ce1fb8e6cc213fd6480803141")

        with open("reservations.json", "r") as file:
            data = file.read()

        self.assertIn("12345678Z", data)  # Verificar si el DNI está en la reserva


    def test_TC2(self):
        # Caso de prueba para una tarjeta de crédito inválida (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_TC3(self):
        # Caso de prueba para una tarjeta de crédito inválida (tarjeta de crédito inválida)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="1234567890123450",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_TC4(self):
        # Caso de prueba para una tarjeta de crédito inválida (no todos son números)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="A256783371569570",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_TC5(self):
        # Caso de prueba para una tarjeta de crédito inválida (17 dígitos)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="12345678901234567",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")

    def test_TC6(self):
        # Caso de prueba para una tarjeta de crédito inválida (15 dígitos)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="256783371569570",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de tarjeta de crédito inválido")


    def test_TC7(self):
        # Caso de prueba para un DNI inválido (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: DNI inválido")

    def test_TC8(self):
        # Caso de prueba para un DNI inválido (DNI incorrecto)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678B",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: DNI inválido")

    def test_TC9(self):
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

    def test_TC10(self):
        # Caso de prueba para un DNI inválido (más caracteres)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="123456789BC",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: DNI inválido")

    def test_TC11(self):
        # Caso de prueba para un DNI inválido (menos caracteres)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="1234567",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: DNI inválido")



    def test_TC12(self):
        # Caso de prueba para nombre y apellidos inválidos (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La cadena del nombre y apellidos no es válida")

    def test_TC13(self):
        # Caso de prueba para nombre y apellidos inválidos (una cadena de texto)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="LolaMontero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La cadena del nombre y apellidos no es válida")

    def test_TC14(self):
        # Caso de prueba para nombre y apellidos inválidos (cadena demasiado corta)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lo Mo",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La cadena del nombre y apellidos no es válida")

    def test_TC15(self):
        # Caso de prueba para nombre y apellidos inválidos (cadena demasiado larga)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero Espinosa Rodriguez De todos Los Santos Garcia Atrustegui",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La cadena del nombre y apellidos no es válida")

    def test_TC16(self):
        # Caso de prueba para un número de teléfono inválido (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de teléfono inválido")

    def test_TC17(self):
        # Caso de prueba para un número de teléfono inválido (demasiado largo y con letras)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123A567821",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de teléfono inválido")

    def test_TC18(self):
        # Caso de prueba para un número de teléfono inválido (demasiado corto)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="12346781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Número de teléfono inválido")

    def test_TC19(self):
        # Caso de prueba para un tipo de habitación inválido (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Tipo de habitación inválido")

    def test_TC20(self):
        # Caso de prueba para un tipo de habitación inválido (cadena diferente a opciones)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="pringles",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Tipo de habitación inválido")

    def test_TC21(self):
        # Caso de prueba para un tipo de habitación inválido (repeticion de cadena aceptada)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single single",
                arrival_date="13/12/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Tipo de habitación inválido")


    def test_TC22(self):
        # Caso de prueba para una fecha de llegada inválida (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

    def test_TC23(self):
        # Caso de prueba para una fecha de llegada inválida (no respeta el formato)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/122024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

    def test_TC24(self):
        # Caso de prueba para una fecha de llegada inválida (fecha antigua)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="18/01/2004",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: La fecha de llegada debe ser posterior a la fecha actual")

    def test_TC25(self):
        # Caso de prueba para una fecha de llegada inválida (día y mes inválidos)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="34/0/2004",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

    def test_TC26(self):
        # Caso de prueba para una fecha de llegada inválida (día y mes inválidos)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="0/16/2024",
                num_days=5
            )

        self.assertEqual(str(e.exception), "Error: Formato de fecha de llegada inválido. Debe ser dd/mm/yyyy.")

    def test_TC27(self):
        # Caso de prueba para un número de noches inválido (argumento vacío)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=""
            )

        self.assertEqual(str(e.exception), "Error: Número de noches inválido. Debe estar entre 1 y 10.")

    def test_TC28(self):
        # Caso de prueba para un número de noches inválido (no es un número)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days="L55"
            )

        self.assertEqual(str(e.exception), "Error: Número de noches inválido. Debe estar entre 1 y 10.")

    def test_TC29(self):
        # Caso de prueba para un número de noches inválido (todos los datos válidos, número de noches = 24)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=24
            )

        self.assertEqual(str(e.exception), "Error: Número de noches inválido. Debe estar entre 1 y 10.")

    def test_TC30(self):
        # Caso de prueba para un número de noches inválido (todos los datos válidos, número de noches = 0)
        with self.assertRaises(HotelManagementException) as e:
            HotelManager().room_reservation(
                creditcardNumb="5256783371569576",
                nAMeAndSURNAME="Lola Montero",
                IDCARD="12345678Z",
                phonenumber="123456781",
                room_type="single",
                arrival_date="13/12/2024",
                num_days=0
            )

        self.assertEqual(str(e.exception), "Error: Número de noches inválido. Debe estar entre 1 y 10.")

if __name__ == "__main__":
    unittest.main()