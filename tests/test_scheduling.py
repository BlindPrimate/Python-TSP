import unittest
import datetime
from datamodel import RoutePoint
from datamodel import Package
from datamodel import Route
from scheduling import Scheduler
from globals import DELIVERED
from globals import END_OF_DAY


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler(2)

    def build_route(self, stops):
        route = Route()
        for i in stops:
            stop = RoutePoint(i, [Package(1, "2000 main", "Podunk", "Wisconsin", 55555, "EOD", 17, "DELIVERED")])
            route.add_stop(stop)
        return self.scheduler._optimize_route(route)

    def test_optimize_route_base(self):
        test_cycle1 = self.build_route([3, 1, 4])
        test_cycle2 = self.build_route([6, 1, 14, 10])
        self.assertEqual([0, 4, 3, 1, 0], test_cycle1.get_address_indexes())
        self.assertEqual([0, 14, 1, 6, 10, 0], test_cycle2.get_address_indexes())

    def test_optimize_route_duplicates(self):
        test_cycle1 = self.build_route([3, 1, 4, 4, 1])
        self.assertEqual([0, 4, 3, 1, 0], test_cycle1.get_address_indexes())

    def test_route_distance(self):
        test_route_1 = self.build_route([7, 1, 14, 2, 8])
        distance_1 = test_route_1.total_route_distance()
        test_route_2 = self.build_route([3, 11, 5, 20, 6, 22])
        distance_2 = test_route_2.total_route_distance()
        self.assertAlmostEqual(24.4, distance_1)
        self.assertAlmostEqual(34.9, distance_2)

    def test_total_route_time(self):
        test_route_1 = self.build_route([3, 11, 5, 20, 6, 22])
        time_1 = test_route_1.total_route_time()
        self.assertAlmostEqual(1.94, time_1, 2)

    def test_all_packages_delivered(self):
        self.scheduler.simulate_day()
        for i in self.scheduler.package_hash:
            self.assertEqual(i.status, DELIVERED)

    def test_all_packages_delivered_on_time(self):
        self.scheduler.simulate_day()
        for i in self.scheduler.package_hash:
            self.assertLessEqual(i.delivered, END_OF_DAY)

    def test_special_case_specific_truck(self):
        self.scheduler.simulate_day()
        special_packages = [3, 18, 36, 38]
        for id in special_packages:
            package = self.scheduler.package_hash.find(id)
            self.assertEqual(2, package.delivered_by_truck.id)

    def test_special_case_same_truck_same_route(self):
        self.scheduler.simulate_day()
        special_packages = [13, 14, 15, 16, 19, 20]
        first_package = self.scheduler.package_hash.find(special_packages[0])
        count = 0
        for id in special_packages:
            package = self.scheduler.package_hash.find(id)
            if package.delivered_by_truck.id == first_package.delivered_by_truck.id and \
                    package.delivery_route == first_package.delivery_route:
                count += 1
        self.assertEqual(len(special_packages), count)


    def test_special_case_cannot_leave_before_x(self):
        self.scheduler.simulate_day()
        special_packages = [6, 25, 28, 32]
        special_time = datetime.datetime(2000, 1, 1, 9, 5, 0)  # 9:05am
        for id in special_packages:
            package = self.scheduler.package_hash.find(id)
            self.assertGreater(package.delivered, special_time)



if __name__ == '__main__':
    unittest.main()
