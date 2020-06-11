from globals import *
from datamodel import Route
from datamodel import io


class Scheduler:

    def __init__(self, package_data):
        self.raw_data = package_data
        self.address_table = io.CSVImport().import_addresses()

    def translate_address(self, package_address):
        for index, address in enumerate(self.address_table[1]):
            address = address.strip()
            if address == package_address:
                return index

    def route_generator(self):
        for truck_load in self._truck_load_generator():
            stop_indexes = []
            route_stops = [self.translate_address(package.address) for package in truck_load]
            yield Route(route_stops)

    def _truck_load_generator(self):
        sorted_packages = self._sort_packages()
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(sorted_packages):
            if count + TRUCK_CAPACITY > len(sorted_packages):
                yield sorted_packages[count:]
            else:
                yield sorted_packages[count:count + TRUCK_CAPACITY]
            count += TRUCK_CAPACITY

    def _sort_packages(self):
        package_list = self.raw_data.to_list()
        # sort packages by deadline time
        package_list.sort(key=lambda package: package.deadline)
        return package_list



