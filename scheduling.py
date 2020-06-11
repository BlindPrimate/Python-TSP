from globals import *
from datamodel import io


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
            stop_indexes = []
            route_stops = [self.translate_address(package.address) for package in truck_load]
            yield route_stops

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
        package_list.sort(key=lambda package: package.deadline)
        return package_list



