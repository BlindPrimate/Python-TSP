from globals import *
from datamodel import io
from datamodel import Route
from datamodel import RoutePoint
from datamodel import Package
from datamodel import Truck
from datamodel.hashtable import HashTable
import datetime
from sys import maxsize


# helper functions
def build_package_table(package_data):
    """
    Builds package hash table for easy access of package data.

    Uses provided package data to build a hash table data structure with helper methods
    :param package_data:
    :return:
    """
    hash_table = HashTable(45)

    for row in package_data:
        if row[0]:
            # unpack csv provided list to variables
            id, address, city, state, zip, deadline, mass, special_instruction = row[:8]

            # build package object

            # handle special package instructions  -- naive
            if special_instruction:
                package = Package(id, address, city, state, zip, deadline, mass)
                package.set_special_status(special_instruction)
            else:
                package = Package(id, address, city, state, zip, deadline, mass)
            # insert into hash table with provided id for easier retrieval
            hash_table.insert(package, id)
    return hash_table


class TruckLoadGenerator:
    def __init__(self, packages):
        self.packages = packages
        self.regular_packages = []
        self.priority_packages = []
        self.truck_loads = []

        # give truck some empty space to except special packages on routes
        self.effective_truck_capacity = int(round(TRUCK_CAPACITY - TRUCK_CAPACITY * 0.3))
        self.special_packages = {
            "truck": [],
            "delayed": [],
            "deliver_with": [],
            "wrong_address": [],
        }

        self.packages.sort(key=lambda x: (x.deadline, x.address))
        self._sort_packages()

    def _sort_packages(self):
        address_clusters = {}

        # sort priority, special, and regular packages
        for package in self.packages:
            if package.has_special_status():
                special = package.get_special_status()
                self.special_packages[special].append(package)
            elif package.deadline != END_OF_DAY:
                self.priority_packages.append(package)
            else:
                self.regular_packages.append(package)

        # regular package sort into address clusters
        for package in self.regular_packages:
            if package.address in address_clusters.keys():
                address_clusters[package.address].append(package)
            else:
                address_clusters[package.address] = [package]

        self.truck_loads = self._load_split(self.priority_packages) + self._load_split(self.regular_packages)


    def _load_split(self, packages):
        result = []
        count = 0
        while count <= len(packages):
            # check if previous loads are to full effective truck capacity -- fill if not
            if result:
                for load in result:
                    if len(load) < self.effective_truck_capacity:
                        space_remaining = self.effective_truck_capacity - len(load)
                        while space_remaining:
                            load.append(packages[count])
                            count += 1
                            space_remaining -= 1

            # cut sorted_packages into spans of TRUCK_CAPACITY size
            if count + self.effective_truck_capacity == len(packages):
                break
            if count + self.effective_truck_capacity > len(packages):
                result.append(packages[count:])
                count += self.effective_truck_capacity
            else:
                result.append(packages[count:count + self.effective_truck_capacity])
                count += self.effective_truck_capacity
        return result

class Scheduler:
    def __init__(self, num_of_trucks):
        data = io.CSVImport()
        self.package_hash = build_package_table(data.import_packages())
        self.address_table = data.import_addresses()
        self.distance_table = data.import_distances()
        self.regular_routes = []
        self.special_routes = []
        self.regular_packages = []
        self.trucks = []
        self.total_distance_traveled = 0

        # generate trucks
        for id in range(num_of_trucks):
            self.trucks.append(Truck(id + 1))

        self.special_packages = {
            "truck": [],
            "delayed": [],
            "deliver_with": [],
            "wrong_address": [],
        }

        self.current_time = START_OF_DAY

        # function calls to build routes
        self._regular_route_builder()
        self._special_route_builder()



    def _is_truck_available(self):
        for truck in self.trucks:
            if truck.isAvailable:
                return True
        return False

    def _has_truck_returned(self):
        for truck in self.trucks:
            if truck.nextAvailable > self.current_time:
                return truck
        return None


    def _generate_route_id(self):
        count = 0
        while True:
            count += 1
            yield count

    def simulate_day(self, end_time=END_OF_DAY):
        """
        Simulates a day of deliveries.

        Uses optional parameter for end of day to calculate from beginning to
        day to provided end point or global end of day.  Time advances by a minute per cycle.
        :param end_time:
        :return:
        """

        builder = TruckLoadGenerator(self.package_hash.to_list())
        for i in builder.truck_loads:
            print(len(i))
            print(i)
        while self.current_time < end_time:
            truck = self._has_truck_returned()

            if truck:
                truck.truck_returning_hub()

            if self._is_truck_available():
                truck = self._get_truck()
            else:
                continue

            final_route = Route()
            final_route.route_id = self._generate_route_id()

            while truck and len(final_route) <= TRUCK_CAPACITY:
                if self.special_routes:
                    for route in self.special_routes:
                        # get first package in route
                        first_package = route[1].packages[0]
                        # specific truck
                        if first_package.special["truck"]:
                            desired_truck = self._get_truck(first_package.special["truck"])
                            if desired_truck:
                                truck = desired_truck
                                final_route += route
                        # delayed delivery
                        elif first_package.special["delayed"] and self.current_time >= first_package.special["delayed"]:
                            truck.set_route(route)
                            self.special_routes.remove(route)
                            self._run_route(truck)
                        # packages delivered together
                        elif first_package.special["deliver_with"]:
                            truck.set_route(route)
                            self.special_routes.remove(route)
                            self._run_route(truck)
                            break
                        # package with wrong address
                        elif first_package.special["wrong_address"] and self.current_time >= datetime.datetime(2000, 1,
                                                                                                               1,
                                                                                                               10, 20,
                                                                                                               00):
                            first_package.address = "410 S State"
                            first_package.city = "Salt Lake City"
                            first_package.state = "UT"
                            first_package.zip = "84111"
                            truck.set_route(route)
                            self.special_routes.remove(route)
                            self._run_route(truck)
                            break
                # advance day by one minute
            advance_minute = datetime.timedelta(minutes=1)
            self.current_time += advance_minute


    def _run_route(self, truck):
        truck.truck_departing_hub()
        current_time = self.current_time
        for stop in truck.route:
            current_time += datetime.timedelta(hours=stop.travel_time)
            self.total_distance_traveled += stop.distance_to
            for package in stop.packages:
                package.delivered = current_time
                package.status = DELIVERED
                package.delivered_by_truck = truck
        truck.truck_returning_hub()

    def _get_truck(self, truck_id: int = None):
        """
        Returns truck if not currently in use.

        :param truck_id: ID of specific truck
        :return Truck: if truck available
        """
        for truck in self.trucks:
            if truck_id:
                if truck_id == truck.id and truck.isAvailable:
                    return truck
                else:
                    continue
            elif truck.isAvailable:
                return truck
        return None

    def _consolidate_stops(self, route_stops: Route):
        """
        Consolidates any packages going to stops that appear twice in a route.
        :param route_stops: List of Stops or Route
        :type route_stops: List or Route
        :return: Route
        """
        consolidated = []
        used = []
        for stop in route_stops:
            # if stop has only one package send to consolidated list
            if stop.address_id not in used:
                consolidated.append(stop)
                used.append(stop.address_id)
            # else look for package with identical address and add package to it
            else:
                for consolidated_stop in consolidated:
                    if consolidated_stop.address_id == stop.address_id:
                        consolidated_stop.packages.extend(stop.packages)
        return Route(consolidated)

    def _stop_generator(self, packages):
        for package in packages:
            stop = RoutePoint(package.address_index, [package])
            yield stop

    def _optimize_route(self, route_stops: list) -> Route:
        """
        Optimizes route based on distance between stops.

        :param route_stops:
        :return Route:
        """

        # clear duplicates
        route = self._consolidate_stops(route_stops)

        # always start at hub
        start_delivery_point = RoutePoint(0, None)
        optimized_route = Route()
        # add start point at hub
        optimized_route.add_stop(RoutePoint(0, None))

        origin_point = start_delivery_point

        # continue until all vertices have been added to the route
        while len(optimized_route) <= len(route):
            best_edge = maxsize
            best_delivery_point = RoutePoint(0, None)

            # compare against other delivery stops
            for delivery_point in route:
                # ignore delivery stops that have already been added to optimized route
                if delivery_point in optimized_route or delivery_point == start_delivery_point:
                    continue
                edge_weight = float(self.distance_table[origin_point.address_id][delivery_point.address_id])
                # compare distance between this stop and previous best stop distance
                if edge_weight < best_edge:
                    best_edge = edge_weight
                    best_delivery_point = delivery_point
                    start_delivery_point = delivery_point
            best_delivery_point.set_distance_to(best_edge)
            optimized_route.add_stop(best_delivery_point)
            origin_point = best_delivery_point

        # add a return to hub stop to route
        final_leg = RoutePoint(0, None)
        distance = float(self.distance_table[optimized_route[-1].address_id][0])
        final_leg.set_distance_to(distance)
        optimized_route.add_stop(final_leg)
        return optimized_route

    def _translate_address(self, target_address):
        for index, address in enumerate(self.address_table[1]):
            address = address.strip()
            if address == target_address:
                return index
        raise Exception("Translate address not possible")

    def _truck_load_generator(self, package_list, truck_capacity=TRUCK_CAPACITY):
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(package_list):
            if count + truck_capacity == len(package_list):
                break
            if count + truck_capacity > len(package_list):
                yield package_list[count:]
            else:
                yield package_list[count:count + truck_capacity]
            count += truck_capacity

    def _regular_route_builder(self):
        self._sort_packages()
        # regular routes
        for load in self._truck_load_generator(self.regular_packages):
            route = Route()
            for package in load:
                address_index = self._translate_address(package.address)
                package.address_index = address_index
            for stop in self._stop_generator(load):
                route.add_stop(stop)
            route = self._optimize_route(route)
            self.regular_routes.append(route)

    def _special_route_builder(self):
        self._sort_packages()
        # special routes
        for special_type in self.special_packages.values():
            route = Route()
            for package in special_type:
                address_index = self._translate_address(package.address)
                package.address_index = address_index
            for stop in self._stop_generator(special_type):
                route.add_stop(stop)
            route = self._optimize_route(route)
            self.special_routes.append(route)



    def _sort_packages(self):
        package_list = self.package_hash.to_list()



