import unittest
from datamodel import Route
from datamodel import io
from math import isclose

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        data = io.CSVImport()
        self.table = [
            [0, 5, 6, 31],
            [21, 0, 4, 7],
            [4, 5, 0, 13],
            [1, 38, 22, 0]
        ]

    def test_optimize_route_base(self):
        test_cycle1 = Route([3, 1, 4])
        test_cycle2 = Route([6, 1, 14, 10])
        self.assertEqual([0, 4, 3, 1], test_cycle1)
        self.assertEqual([0, 1, 6, 10, 14], test_cycle2)

    def test_optimize_route_duplicates(self):
        test_cycle1 = Route([3, 1, 4, 4, 1])
        self.assertEqual([0, 4, 3, 1], test_cycle1)

    def test_route_distance(self):
        test_route_1 = Route([7, 1, 14, 2, 8])
        distance_1 = test_route_1.total_route_distance()
        test_route_2 = Route([3, 11, 5, 20, 6, 22])
        distance_2 = test_route_2.total_route_distance()
        self.assertAlmostEqual(30.2, distance_1)
        self.assertAlmostEqual(40.2, distance_2)

if __name__ == '__main__':
    unittest.main()
