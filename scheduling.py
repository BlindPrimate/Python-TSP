from globals import *
from datamodel import io
from datamodel import Route
from datamodel import RoutePoint
from datamodel import Package
from datamodel.hashtable import HashTable
from sys import maxsize


def build_package_table(package_data):
    hash_table = HashTable(45)

    for package in package_data:
        if package[0]:
            # unpack csv provided list to variables
            id, address, city, state, zip, deadline, mass, special = package[:8]
            # build package object
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


    def _consolidate_stops(self, route_stops:Route):
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

    def _optimize_route(self, route_stops):
        # clear duplicates
        route = self._consolidate_stops(route_stops)
        # print(route[0])

        # always start at hub
        start_delivery_point = route[0]
        optimized_route = [start_delivery_point]

        # continue until all vertices have been added to the route
        while len(optimized_route) <= len(route):
            best_edge = maxsize
            best_delivery_point = RoutePoint(0, None)

            # compare against other delivery points
            for delivery_point in route:
                # ignore delivery points that have already been added to optimized route
                if delivery_point in optimized_route or delivery_point == start_delivery_point:
                    continue
                edge_weight = float(self.distance_table[start_delivery_point.address_id][delivery_point.address_id])
                if edge_weight < best_edge:
                    best_edge = edge_weight
                    best_delivery_point = delivery_point
                    start_delivery_point = delivery_point

            optimized_route.append(best_delivery_point)
        return Route(optimized_route)

    def translate_address(self, package_address) -> int:
        for index, address in enumerate(self.address_table[1]):
            address = address.strip()
            if address == package_address:
                return index

    def route_generator(self) -> list:
        for truck_load in self._truck_load_generator(10):
            route = Route()
            for package in truck_load:
                # change str of address into index of "Distances" table for easier manipulation
                package_id = self.translate_address(package.address)
                # give the package the Distances index as well for easy retrieval

                route_stop = RoutePoint(package_id, [package])
                route.add_stop(route_stop)
            yield self._optimize_route(route)

    def _truck_load_generator(self, truck_capacity=TRUCK_CAPACITY) -> list:
        sorted_packages = self._sort_packages()
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(sorted_packages):
            print(count + truck_capacity, len(sorted_packages))
            if count + truck_capacity == len(sorted_packages):
                break
            if count + truck_capacity > len(sorted_packages):
                yield sorted_packages[count:]
            else:
                yield sorted_packages[count:count + truck_capacity]
            count += truck_capacity

    def _sort_packages(self):
        package_list = self.raw_data.to_list()
        # sort packages by deadline time
        package_list.sort(key=lambda package: (package.deadline, package.address))
        return package_list

    def build_route_schedule(self, route, departure_time):
        schedule = []
        for stop in route:
            pass
            # if stop.packages:
                # for package in stop.packages:
                #     pass


