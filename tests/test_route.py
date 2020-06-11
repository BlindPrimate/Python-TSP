import unittest
from datamodel import Route
from datamodel import io

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

if __name__ == '__main__':
    unittest.main()
