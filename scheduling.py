from globals import *
from datamodel import io
from datamodel import Route
from datamodel import RoutePoint


class Scheduler:

    def __init__(self, package_data):
        self.raw_data = package_data
        self.address_table = io.CSVImport().import_addresses()

    def translate_address(self, package_address) -> int:
        for index, address in enumerate(self.address_table[1]):
            address = address.strip()
            if address == package_address:
                return index

    def route_generator(self) -> list:
        for truck_load in self._truck_load_generator(10):
            route_stops = []
            for package in truck_load:
                # change str of address into index of "Distances" table for easier manipulation
                package_id = self.translate_address(package.address)
                # give the package the Distances index as well for easy retrieval

                route_stop = RoutePoint(package_id, package)
                route_stops.append(route_stop)
            yield Route(route_stops)


    def build_schedule(self, route):
        print(route)

    def _truck_load_generator(self, truck_capacity=TRUCK_CAPACITY) -> list:
        sorted_packages = self._sort_packages()
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(sorted_packages):
            if count + truck_capacity > len(sorted_packages):
                yield sorted_packages[count:]
            else:
                yield sorted_packages[count:count + truck_capacity]
            count += truck_capacity

    def _sort_packages(self):
        package_list = self.raw_data.to_list()
        # sort packages by deadline time
        package_list.sort(key=lambda package: (package.deadline, package.id))
        return package_list



