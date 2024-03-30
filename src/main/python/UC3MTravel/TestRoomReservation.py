import unittest
import os
import json
from pathlib import Path
from src.main.python.UC3MTravel import HotelReservation
from src.main.python.UC3MTravel.HotelManagementException import HotelManagementException
from HotelManager import HotelManager

class TestRoomReservation(unittest.TestCase):
   def setUp(self):
        if os.path.isfile("fichero_estancias.json"):
            os.remove("fichero_estancias.json")
        if os.path.isfile("reservations.json"):
            os.remove("reservations.json")
        if os.path.isfile("fichero_reservas.json"):
            os.remove("fichero_reservas.json")

   def test_room_reservation_complete_valid(self):

        value = HotelManager.room_reservation(credit_card="5256783371569576",
                                 name_surname="Juan Perez",
                                 id_card="47589661Q",
                                 phone_number="619786871",
                                 room_type="single",
                                 arrival_date="22/08/2024",
                                 num_days=5)

        self.assertEqual(value,"ffec46238eaf205b88fa4a75800c0831")


        if os.path.isfile(""):
            with open("reservations.json", "r", encoding="utf-8") as file:
                data = file.read()

            found = False
            target_value = '47589661Q'

            # Encuentra la posición de la clave "id_card" en el archivo JSON
            index_id_card = data.find('"id_card": "{}"'.format(target_value))

            if index_id_card != -1:
                found = True

            self.assertTrue(found)



   def test_room_reservation_invalid_credit_card(self):
        # Número de tarjeta de crédito inválido
        with self.assertRaises(HotelManagementException) as e:
            room_reservation(
                credit_card="1234567812345678",
                name_surname="Juan Perez",
                id_card="47589661Q",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )

        self.assertEqual(e.exception.message, "El número de tarjeta recibido no es válido o no tiene un formato válido")

   def test_room_reservation_invalid_credit_card2(self):
        # Número de tarjeta de crédito inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="525678337156957",#15 digitos
                name_surname="Juan Perez",
                id_card="47589661Q",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )

        self.assertEqual(e.exception.message, "El número de tarjeta recibido no es válido o no tiene un formato válido")





   def test_room_reservation_invalid_name_surname(self):
        # Número de tarjeta de crédito inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan",
                id_card="47589661Q",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )

        self.assertEqual(e.exception.message, "La cadena del nombre y apellidos no es válida")

   def test_room_reservation_invalid_dni(self):
        # DNI inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="12345",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )
        self.assertEqual(e.exception.message, "El DNI no es válido.")


   def test_room_reservation_invalid_phone_number(self):
        # Número de teléfono inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="02759359A",
                phone_number="1234567890",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )
        self.assertEqual(e.exception.message, "El número de teléfono no es válido")


   def test_room_reservation_invalid_room_type(self):
        # Tipo de habitación inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="02759359A",
                phone_number="619786871",
                room_type="shared",
                arrival_date="22/08/2024",
                num_days=5
            )
        self.assertEqual(e.exception.message, "El tipo de habitación no es válido.")


   def test_room_reservation_invalid_arrival_date(self):
        # Fecha de llegada inválida
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="02759359A",
                phone_number="619786871",
                room_type="single",
                arrival_date="20/08/2022",
                num_days=5
            )
        self.assertEqual(e.exception.message, "La fecha de entrada no es válida.")


   def test_room_reservation_invalid_num_days(self):
        # Número de días inválido
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="02759359A",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=15
            )
        self.assertEqual(e.exception.message, "El número de días no es válido.")

   def test_room_reservation_customer_has_reservation(self):
        self.file_path = "reservations.json"
        localizer = HotelManager.room_reservation(
            credit_card="5256783371569576",
            name_surname="Juan Perez",
            id_card="02759359A",
            phone_number="619786871",
            room_type="single",
            arrival_date="22/08/2024",
            num_days=5
        )
        # Cliente ya tiene una reserva
        with self.assertRaises(HotelManagementException) as e:
            HotelManager.room_reservation(
                credit_card="5256783371569576",
                name_surname="Juan Perez",
                id_card="02759359A",
                phone_number="619786871",
                room_type="single",
                arrival_date="22/08/2024",
                num_days=5
            )
        self.assertEqual(e.exception.message, "El cliente ya tiene una reserva")

        if os.path.isfile("reservations.json"):
            with open("reservations.json", "r", encoding="utf-8") as file:
                data = file.read()

            found = False
            target_value = '02759359A'

            # Encuentra la posición de la clave "id_card" en el archivo JSON
            index_id_card = data.find('"id_card": "{}"'.format(target_value))

            if index_id_card != -1:
                found = True

            self.assertTrue(found)