import unittest
from datamodel import Route, Package, RoutePoint
from datamodel import io
from math import isclose

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.route = Route()
        self.route_2 = Route()

    def test_route_add(self):
        self.assertLess(len(self.route), 1)
        self.route.add_stop(RoutePoint(1, None))
        self.assertEqual(len(self.route), 1)

    def test_route_equality(self):
        self.route.add_stop(RoutePoint(0, None))
        self.route_2.add_stop(RoutePoint(0, None))
        self.assertEqual(self.route, self.route_2)

    if __name__ == '__main__':
        unittest.main()
