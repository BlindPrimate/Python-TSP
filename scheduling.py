from globals import *
from datamodel import io
from datamodel import Route
from datamodel import RoutePoint
from datamodel import Package
from datamodel import Truck
from datamodel.hashtable import HashTable
import datetime
from sys import maxsize


def build_package_table(package_data):
    hash_table = HashTable(45)

    for row in package_data:
        if row[0]:
            # unpack csv provided list to variables
            id, address, city, state, zip, deadline, mass, special_instuction = row[:8]

            # build package object

            # handle special package instructions  -- naive
            if special_instuction:
                package = Package(id, address, city, state, zip, deadline, AT_HUB, mass)
                package.set_special_status(special_instuction)
            else:
                package = Package(id, address, city, state, zip, deadline, AT_HUB, mass)
            # insert into hash table with provided id for easier retrieval
            hash_table.insert(package, id)
    return hash_table


class Scheduler:
    def __init__(self):
        data = io.CSVImport()
        self.raw_data = build_package_table(data.import_packages())
        self.address_table = data.import_addresses()
        self.distance_table = data.import_distances()
        self.regular_routes = []
        self.special_routes = []
        self.regular_packages = []
        self.special_packages = {
            "truck": [],
            "delayed": [],
            "deliver_with": [],
            "wrong_address": [],
        }
        self.truck_1 = Truck()
        self.truck_2 = Truck()

    def _consolidate_stops(self, route_stops: Route):
        """
        Consolidates any packages going to stops that appear twice in a route.
        :param route_stops:
        :return: list
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

    def _optimize_route(self, route_stops):
        # clear duplicates
        route = self._consolidate_stops(route_stops)

        # always start at hub
        start_delivery_point = RoutePoint(0, None)
        optimized_route = Route()
        optimized_route.add_stop(RoutePoint(0, None))
        origin_point = start_delivery_point

        # continue until all vertices have been added to the route
        while len(optimized_route) <= len(route):
            best_edge = maxsize
            best_delivery_point = RoutePoint(0, None)

            # compare against other delivery points
            for delivery_point in route:
                # ignore delivery points that have already been added to optimized route
                if delivery_point in optimized_route or delivery_point == start_delivery_point:
                    continue
                edge_weight = float(self.distance_table[origin_point.address_id][delivery_point.address_id])
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
        return None

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

    def regular_route_builder(self):
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

    def special_route_builder(self):
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
        package_list = self.raw_data.to_list()
        for package in package_list:
            if package.has_special_status():
                special = package.get_special_status()
                self.special_packages[special].append(package)
                self.special_packages[special].sort(key=lambda x: (x.deadline, x.address))
            else:
                self.regular_packages.append(package)

        # sort packages by deadline time
        self.regular_packages.sort(key=lambda x: (x.deadline, x.address))

    def build_route_schedule(self, route, departure_time=datetime.datetime(2000, 1, 1, hour=9, minute=30, second=0)):
        schedule = []
        current_time = departure_time
        for stop in route:
            stop_str = ""
            current_time = current_time + datetime.timedelta(hours=stop.travel_time)
            if stop.packages:
                for package in stop.packages:
                    stop_str += "{} {} {} {} Delivery Time: {}\n".format(package.id, package.address, package.city, package.zip, current_time)
                schedule.append(stop_str)
        return schedule

