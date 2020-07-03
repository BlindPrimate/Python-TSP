from globals import *
from datamodel import io
from datamodel import Route
from datamodel import RoutePoint
from datamodel import Package
from datamodel import Truck
from datamodel.hashtable import HashTable
import datetime
from sys import maxsize
from .truck_load import TruckLoad


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


class Scheduler:
    def __init__(self, num_of_trucks):
        data = io.CSVImport()
        self.package_hash = build_package_table(data.import_packages())
        self.address_table = data.import_addresses()
        self.distance_table = data.import_distances()
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

        truck_loader = TruckLoad(self.package_hash.to_list())

        # build routes
        self.special_packages = truck_loader.special_packages

        self.final_loads = truck_loader.truck_loads

    def _can_fit_in_load(self, load, n_items_to_add=0):
        return len(load) + n_items_to_add <= TRUCK_CAPACITY

    def _add_special_packages_to_load(self, load, truck):
        delayed_packages = self.special_packages["delayed"]
        group_packages = self.special_packages["deliver_with"]
        requested_truck_packages = self.special_packages["truck"]

        if self.special_packages["wrong_address"]:
            wrong_address_package = self.special_packages["wrong_address"][0]
        else:
            wrong_address_package = None

        if truck.id == 2 and self._can_fit_in_load(load, len(requested_truck_packages)):
            load += requested_truck_packages
            self.special_packages["truck"].clear()

        while self._can_fit_in_load(load):

            # packages delivered together
            if group_packages:
                if self._can_fit_in_load(load, len(group_packages)):
                    load += group_packages
                    self.special_packages["deliver_with"].clear()
                else:
                    break
            # package with wrong address
            elif wrong_address_package and \
                    self.current_time >= datetime.datetime(2000, 1, 1, 10, 20, 00):
                wrong_address_package.address = "410 S State St"
                wrong_address_package.city = "Salt Lake City"
                wrong_address_package.state = "UT"
                wrong_address_package.zip = "84111"
                load.append(wrong_address_package)
                self.special_packages["wrong_address"] = None
            elif delayed_packages:
                for package in delayed_packages:
                    if self.current_time >= package.special["delayed"]:
                        load.append(package)
                        delayed_packages.remove(package)
                break
            else:
                break
        return load

    def _build_route(self, packages):
        route = Route()
        route.route_id = self._generate_route_id()
        for package in packages:
            address_index = self._translate_address(package.address)
            package.address_index = address_index
        for stop in self._stop_generator(packages):
            route.add_stop(stop)
        route = self._optimize_route(route)
        return route

    def _get_truck(self, truck_id: int = None):
        """
        Returns truck if not currently in use.

        :param truck_id: ID of specific truck
        :return Truck: if truck available
        """
        for truck in self.trucks:
            if truck_id == truck.id and truck.is_truck_available(self.current_time):
                return truck
            elif truck.is_truck_available(self.current_time):
                return truck
        return None

    def _is_truck_available(self):
        for truck in self.trucks:
            if truck.next_available > self.current_time:
                return True
        return False

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
        while self.current_time < end_time:

            truck = self._get_truck()

            if truck and self.final_loads:
                load = self.final_loads.pop(0)
                load = self._add_special_packages_to_load(load, truck)

                route = self._build_route(load)
                truck.set_route(route)
                self._run_route(truck)

            # check for any last special packages not added to previous routes after day is complete
            if self.special_packages.values():
                truck = self._get_truck(2)
                if truck:
                    overflow_load = self._add_special_packages_to_load([], truck)
                    overflow_route = self._build_route(overflow_load)
                    truck.set_route(overflow_route)
                    self._run_route(truck)

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
        truck.truck_returning_hub(current_time)


    def _stop_generator(self, packages):
        for package in packages:
            stop = RoutePoint(package.address_index, [package])
            yield stop

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

    def _optimize_route(self, route_stops: Route) -> Route:
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




