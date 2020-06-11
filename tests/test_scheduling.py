import unittest
from scheduling import Scheduler
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
        self.full_distance_data = data.import_distances()
        self.scheduler = Scheduler(data.import_packages())

    def test_cycle_finder(self):
        test_cycle1 = [3, 1, 4]
        test1 = self.scheduler.cycle_finder(self.full_distance_data, test_cycle1)
        test_cycle2 = [6, 1, 14, 10]
        test2 = self.scheduler.cycle_finder(self.full_distance_data, test_cycle2)
        self.assertEqual([0, 4, 3, 1], test1)
        self.assertEqual([0, 1, 6, 10, 14], test2)


if __name__ == '__main__':
    unittest.main()
