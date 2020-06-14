import unittest
from datamodel import Route, Package, RoutePoint
from datamodel import io
from math import isclose

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.route = Route()

    def test_route_add(self):
        self.assertLess(len(self.route), 1)
        self.route.add_stop(RoutePoint(1, None))
        self.assertEqual(len(self.route), 1)


    if __name__ == '__main__':
        unittest.main()
