import unittest

from prueba import sum
from unittest import TestCase

class TestDeliverProduct(TestCase):
        def setUp(self):
            pass
        def test_hotel_reservation_uk1(self):
            pass


class TestPrueba(TestCase):
    def test_sum(self):
        self.assertEqual(sum(7,5), 12)

if __name__ == "__main__":
    unittest.main()

