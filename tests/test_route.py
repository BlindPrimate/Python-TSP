import unittest
from datamodel import Route, Package, RoutePoint
from datamodel import io
from math import isclose

class MyTestCase(unittest.TestCase):

    def build_route(self, stops):
        route = []
        for i in stops:
            stop = RoutePoint(i, Package(1, "2000 main", "Podunk", "Wisconsin", 55555, "EOD", 17, "DELIVERED"))
            route.append(stop)
        return Route(route)


    def test_optimize_route_base(self):
        test_cycle1 = self.build_route([3, 1, 4])
        test_cycle2 = self.build_route([6, 1, 14, 10])
        self.assertEqual([0, 4, 3, 1], test_cycle1.get_address_indexes())
        self.assertEqual([0, 1, 6, 10, 14], test_cycle2.get_address_indexes())

    def test_optimize_route_duplicates(self):
        test_cycle1 = self.build_route([3, 1, 4, 4, 1])
        self.assertEqual([0, 4, 3, 1], test_cycle1.get_address_indexes())

    def test_route_distance(self):
        test_route_1 = self.build_route([7, 1, 14, 2, 8])
        distance_1 = test_route_1.total_route_distance()
        test_route_2 = self.build_route([3, 11, 5, 20, 6, 22])
        distance_2 = test_route_2.total_route_distance()
        self.assertAlmostEqual(30.2, distance_1)
        self.assertAlmostEqual(40.2, distance_2)

    if __name__ == '__main__':
        unittest.main()
